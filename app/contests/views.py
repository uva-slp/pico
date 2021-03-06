from django.http import HttpResponse, HttpResponseForbidden, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from teams.forms import TeamForm, TeamSelectForm
from .forms import CreateContestForm, CreateProblem, UploadCodeForm, ReturnJudgeResultForm, CreateContestTemplateForm, AdminSearchForm, ParticipantSearchForm, AcceptInvitationForm
from dal import autocomplete
from users.forms import UserSearchForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import formset_factory, inlineformset_factory
from django.urls import reverse
from .lib import diff as _diff
from .lib import execution as exe
from .models import Contest, Problem, ProblemInput, ProblemSolution, ContestTemplate
from teams.models import Team
from .models import Participant, Submission, Notification, ContestInvite
from users.models import User
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.http import Http404
from django.template.loader import render_to_string
import os
from django.conf import settings
from subprocess import Popen


@login_required
def index(request):
    """ Render contest index page
    Displays active, unstarted, past contests and contest invitations related to the request user
    :param request: None or POST
    :return: A rendered home page or redirects the user to the home page on a successful form submit
    """
    # Get all active, unstarted, past contests related to the request user
    all_active_contests = Contest.objects.active()
    my_active_contests = []
    for contest in all_active_contests:
        if isCreator(contest, request.user) or isJudge(contest, request.user) or isParticipant(contest, request.user):
            my_active_contests.append(contest)

    all_unstarted_contests = Contest.objects.unstarted()
    my_unstarted_contests = []
    for contest in all_unstarted_contests:
        if isCreator(contest, request.user) or isJudge(contest, request.user) or isParticipant(contest, request.user):
            my_unstarted_contests.append(contest)

    all_past_contests = Contest.objects.past()
    my_past_contests = []
    for contest in all_past_contests:
        if isCreator(contest, request.user) or isJudge(contest, request.user) or isParticipant(contest, request.user):
            my_past_contests.append(contest)

    # Handling invitation acceptance
    if request.method == 'POST':
        cur_invitation = get_object_or_404(ContestInvite, id=request.POST.get("invitationId"))
        if request.POST.get("accept"):
            # Create participant objects for the team
            team = cur_invitation.team
            contest = cur_invitation.contest
            pt = Participant(contest=contest, team=team)
            pt.save()
            cur_invitation.delete()
        elif request.POST.get("decline"):
            cur_invitation.delete()

    all_invitations = ContestInvite.objects.all()
    my_contest_invitations = []
    for invitation in all_invitations:
        if request.user in invitation.team.members.all():
            my_contest_invitations.append(invitation)

    return render(
        request,
        'contests/index.html',
        {
            'active_contests': my_active_contests,
            'unstarted_contests': my_unstarted_contests,
            'past_contests': my_past_contests,
            'contest_invitations': my_contest_invitations
        }
    )


@login_required
def createContest(request):
    """ Create new Contest objects.
    It also displays a Contest Template loading form to allow the user to auto-fill the Contest form with the content of a
    ContestTemplate he has already created.

    On a submit, either a ContestTemplate will be filled into the form or a contest will be created.
    Contest creation involves validating the Contest form and QAFormSet, which stores all the Problem forms,
    then saving the contest to the database, uploading the problem description file to the server, sending invitations to
    each contest participant, and creating each individual Problem

    :param request: None or POST
    :return: A rendered Contest form page or redirects the user to the home page on a successful form submit
    """

    template_user = request.user
    templates = ContestTemplate.objects.filter(creator=template_user)

    QAFormSet = formset_factory(CreateProblem)
    qa_formset = QAFormSet()

    form = CreateContestForm()
    form.fields['problem_description'].required = True
    admin_search_form = AdminSearchForm()
    participant_search_form = ParticipantSearchForm()

    if request.method == 'POST':
        if request.POST['submit'] == "load_template":
            selected_template = request.POST['selected_template']

            if ContestTemplate.objects.filter(pk=selected_template).exists():
                template = ContestTemplate.objects.get(pk=selected_template)
                form = CreateContestForm(initial={
                        'title': template.title, 'languages': template.languages,
                        'contest_length': template.contest_length, 'time_penalty': template.time_penalty,
                        'autojudge_enabled': template.autojudge_enabled, 'autojudge_review': template.autojudge_review,
                        'contest_admins': template.contest_admins.all(), 'contest_participants': template.contest_participants.all()
                    }
                )

                admin_search_form = AdminSearchForm(
                    initial={'contest_admins': template.contest_admins.all()})
                participant_search_form = ParticipantSearchForm(
                    initial={'contest_participants': template.contest_participants.all()})

                data = {
                    'templates': templates,
                    'form': form,
                    'qa_formset': qa_formset,
                    'admin_search_form': admin_search_form,
                    'participant_search_form': participant_search_form
                }

                return render(request, 'contests/create_contest.html', data)

        if request.POST['submit'] == "create_contest":
            #grab information from form
            form = CreateContestForm(request.POST, request.FILES)
            qa_formset = QAFormSet(request.POST, request.FILES)

            if form.is_valid() and qa_formset.is_valid():

                problem_desc = Contest(problem_description=request.FILES['problem_description'], date_created=datetime.now(timezone.utc))

                contest = form.save()
                contest.creator = request.user
                contest.save()

                contest_id = contest.id

                contest_participants = form.cleaned_data.get('contest_participants')

                for participant in contest_participants :
                    # Loop through the given participants when a user creates a contest and send invitation to each team
                    team = Team.objects.filter(name=participant).get()
                    inv = ContestInvite(contest=contest, team=team)
                    inv.save()

                for index, qa_form in enumerate(qa_formset):
                    createNewProblem(request, qa_form, contest_id, index)

                    # Loop through participants text box and create participant objects for a team on each line w/ contest

                return redirect(reverse('home'))

    data = {
        'templates': templates,
        'form': form,
        'qa_formset': qa_formset,
        'admin_search_form': admin_search_form,
        'participant_search_form': participant_search_form
    }

    return render(request, 'contests/create_contest.html', data)


@login_required
def createNewProblem(request, problem_form, contest_id, form_number=None):
    """ Create new Problem objects.
    Each Problem can also have multiple ProblemInputs and ProblemSolutions.

    :param request: None or POST
    :param problem_form: the Problem form stored in the QAFormSet
    :param contest_id: the associated Contest, to be used as a foreign key
    :param form_number: the Problem number
    :return: Problem
    """

    form = problem_form.cleaned_data
    solution = form.get('solution')
    input_desc = form.get('input_description')
    output_desc = form.get('output_description')
    sample_input = form.get('sample_input')
    sample_output = form.get('sample_output')

    p = Problem(
        input_description=input_desc,
        output_description=output_desc, sample_input=sample_input,
        sample_output=sample_output, contest_id=contest_id
    )
    p.save()
    if form_number != None:
        files = request.FILES.getlist('form-'+str(form_number)+'-program_input')
        for f in files:
            pi = ProblemInput(problem=p, program_input=f)
            pi.save()
        files = request.FILES.getlist('form-'+str(form_number)+'-solution')
        for f in files:
            ps = ProblemSolution(problem=p, solution=f)
            ps.save()
    return p


@login_required
def editContest(request, contest_id):
    """ Edit a Contest.
    The Contest form can be edited, individual Problems can be edited or deleted, and new Problems can be created.

    :param request: None or POST
    :param contest_id: the Contest to be edited
    :return: An HttpResponseForbidden for any user who didn't create this Contest or the rendered edit Contest form page
    """

    contest = get_object_or_404(Contest, pk=contest_id)
    if contest.creator != request.user:
        return HttpResponseForbidden()

    form = CreateContestForm(None, None, instance=contest)
    form.fields['problem_description'].required = False

    admin_search_form = AdminSearchForm(initial={'contest_admins': contest.contest_admins.all()})
    participant_search_form = ParticipantSearchForm(initial={'contest_participants': contest.contest_participants.all()})

    problem_form = CreateProblem()

    problems = contest.problem_set.all()
    problems_set = []
    for problem in problems:
        problems_set.append((problem.id, CreateProblem(instance=problem)))

    if request.method == 'POST':
        if request.POST['submit'] == "update_contest":

            form = CreateContestForm(request.POST, request.FILES, instance=contest)

            if form.is_valid():
                problem_desc = Contest(problem_description=request.FILES.get('problem_description', False),
                                       date_created=datetime.now(timezone.utc))
                form.save()

                contest_participants = form.cleaned_data.get('contest_participants')

                for participant in contest_participants:  # Loop through the given participants when a user creates a contest and create participant objects for each
                    if participant not in Contest.objects.values_list('contest_participants', flat=True).filter(pk=contest_id):
                        team = Team.objects.filter(name=participant).get()
                        pt = Participant(contest=contest, team=team)
                        pt.save()

                request.method = None
                request.POST = None
                return editContest(request, contest_id)

        if request.POST['submit'] == "update_problem":
            problem_id = request.POST['problem_id']
            problem = Problem.objects.get(pk=problem_id)
            #Delete existing input and solution files
            problem_inputs = problem.problem_input.all()
            for problem_input in problem_inputs:
                problem_input.delete()
            problem_solutions = problem.problem_solution.all()
            for problem_solution in problem_solutions:
                problem_solution.delete()
            problem_form = CreateProblem(request.POST or None, request.FILES or None, instance=problem)
            #Create new input and solution files
            p = Problem.objects.get(pk=problem_id)
            files = request.FILES.getlist('program_input')
            for f in files:
                pi = ProblemInput(problem=p, program_input=f)
                pi.save()
            files = request.FILES.getlist('solution')
            for f in files:
                ps = ProblemSolution(problem=p, solution=f)
                ps.save()
                
            if problem_form.is_valid():
                problem_form.id = problem_id
                problem_form.save()
            request.method = None
            request.POST = None
            return editContest(request, contest_id)

        if request.POST['submit'] == "delete_problem":
            problem_id = request.POST['problem_id']
            Problem.objects.get(pk=problem_id).delete()

            request.method = None
            request.POST = None
            return editContest(request, contest_id)

        if request.POST['submit'] == "save_new_problem":
            problem_form = CreateProblem(request.POST, request.FILES)
            if problem_form.is_valid():
                p = createNewProblem(request, problem_form, contest_id)
                files = request.FILES.getlist('program_input')
                for f in files:
                    pi = ProblemInput(problem=p, program_input=f)
                    pi.save()
                files = request.FILES.getlist('solution')
                for f in files:
                    ps = ProblemSolution(problem=p, solution=f)
                    ps.save()
            request.method = None
            request.POST = None
            return editContest(request, contest_id)

    data = {
        'form': form,
        'admin_search_form': admin_search_form,
        'participant_search_form': participant_search_form,
        'problem_form': problem_form,
        'problems_set': problems_set,
        'contest_id': contest_id
    }

    return render(request, 'contests/edit_contest.html', data)


@login_required
def deleteContest(request, contest_id):
    """ Delete a Contest.

    :param request: POST
    :param contest_id: the Contest to be deleted
    :return: Redirects the user to the home page
    """

    Contest.objects.get(pk=contest_id).delete()
    return redirect(reverse('home'))


@login_required
def activateContest(request, contest_id):
    """ Activate a Contest.
    Saves the current datetime to the Contest's database entry.

    :param request: POST
    :param contest_id: the Contest to be activated
    :return: Redirects the user to the home page
    """

    time = datetime.now()
    contest = Contest.objects.get(id=contest_id)
    contest.contest_start = time
    contest.save()
    return redirect(reverse('home'))


@login_required
def createTemplate(request):
    """ Create a ContestTemplate.

    :param request: None or POST
    :return: A rendered ContestTemplate form page or redirects the user to the home page on a successful form submit
    """

    form = CreateContestTemplateForm()
    admin_search_form = AdminSearchForm()
    participant_search_form = ParticipantSearchForm()

    if request.method == 'POST':
        form = CreateContestTemplateForm(request.POST)

        if form.is_valid():
            contest_template = form.save()
            contest_template.creator = request.user
            contest_template.save()

            return redirect(reverse('home'))

    data = {
        'form': form,
        'admin_search_form': admin_search_form,
        'participant_search_form': participant_search_form
     }

    return render(request, 'contests/create_template.html', data)


def getTeam(contest_data, user):
    """ Helper method for getting the team of a user participated in a contest
    :param contest_data:a Contest object
    :param user: a User object
    :return: A Team object if the user is in a team which participate in the contest, or None if not.
    """
    user = User.objects.get(id=user.id)
    contest_data = Contest.objects.get(id=contest_data.id)
    contest_participants = contest_data.participant_set.all()
    for participant in contest_participants:
            team = participant.team
            if user in team.members.all():
                    return team
    return None


def isJudge(contest_data, user):
    """ Helper method for checking if a user is judge of the contest
    :param contest_data:a Contest object
    :param user: a User object
    :return: boolean type. True if the user is a judge of the contest, or False if not.
    """
    contest_judges = contest_data.contest_admins.all()
    for judge in contest_judges:
        if user == judge:
            return True
    return False


def isCreator(contest_data, user):
    """ Helper method for checking if a user is the creator of the contest
    :param contest_data:a Contest object
    :param user: a User object
    :return: boolean type. True if the user is the creator of the contest, or False if not.
    """
    if user == contest_data.creator:
        return True
    return False


def isParticipant(contest_data, user):
    """ Helper method for checking if user is participant in the contest
    :param contest_data:a Contest object
    :param user: a User object
    :return: boolean type. True if the user is in a team which participate in the contest, or Fale if not.
    """
    current_team = getTeam(contest_data, user)
    if current_team is None:
        return False
    else:
        return True


@login_required
def displayContest(request, contest_id):
    """ Display the main page for a Contest.
    Only the contest creator, judges of a contest and superusers have access to it before the contest is activated.
    Once active, only the contest creator, judges, superusers and participants of a contest have access to viewing it.

    This page displays the time remaining in the contest, the contest problem description, each contest problem,
    a form to submit solutions to a problem, the status of that problem (unanswered, correct, awaiting judging, or incorrect),
    problem attempts, and a link to the scoreboard.

    The contest creator and judges have a judging panel which allows them to view and judge user submissions. They can also
    activate the contest, edit the contest, and delete the contest.

    A past contest can be viewed beginning 1 minute after it has finished, but no more submissions can ever be made.

    :param request: None or POST
    :param contest_id: the Contest to be viewed
    :return: A rendered Contest page
    """

    # Check if request user has permission to view the page
    contest_data = Contest.objects.get(id=contest_id)
    is_judge = isJudge(contest_data, request.user)
    is_participant = isParticipant(contest_data, request.user)
    is_creator = isCreator(contest_data, request.user)
    current_team = getTeam(contest_data, request.user)
    is_past = contest_data.contest_end() <= timezone.now()

    if not is_judge and not is_participant and not is_creator and not request.user.is_superuser:
        return redirect(reverse('home'))

    # Save contest submission
    if request.method == 'POST':
        form = UploadCodeForm(request.POST, request.FILES)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.original_filename = request.FILES['code_file'].name
            sub.team = current_team

            totalSub = 0
            for problem in contest_data.problem_set.all():
                totalSub += len(problem.submission_set.all())
            sub.run_id = totalSub + 1

            sub.save()

    problems = contest_data.problem_set.all()
    # Handle multiple forms on the same page
    UploadCodeFormSet = formset_factory(UploadCodeForm, extra=len(problems))
    problem_form_pairs = []
    for problem in problems:
        form = UploadCodeForm(initial={'problem': problem})
        problem_form_pairs.append((problem, form))

    contest_participants = contest_data.participant_set.all()

    # Get information of the team's submissions for each problem
    current_team = getTeam(contest_data, request.user)
    submission_attempts = []
    status = []
    color_states = []
    if current_team is not None:
        for p in problems:
            p_submissions = p.submission_set.filter(team__pk=current_team.id)
            # number of attempts
            current_attempts = len(p_submissions)
            submission_attempts.append(current_attempts)
            # status -- ignore the rest
            current_status = "-"
            current_color = "default"
            if current_attempts is not 0:
                got_yes = False
                for s in p_submissions:
                    if s.state == 'YES':
                        got_yes = True
                        break
                if got_yes:
                    current_status = "Yes"
                    current_color = "success"
                else:
                    submissions = list(p_submissions)
                    submissions.sort(key=lambda x: x.timestamp)
                    latest_submission = submissions[-1]
                    if latest_submission.state == 'NEW':
                        current_color = "warning"
                        current_status = "New"
                    elif latest_submission.state == 'NO':
                        current_color = "danger"
                        current_status = "No - " + latest_submission.get_result_display()
            status.append(current_status)
            color_states.append(current_color)

    data = {
        'contest_data': contest_data, 'contest_problems': problems,
        'is_judge': is_judge, 'is_participant': is_participant, 'is_creator': is_creator,
        'current_team': current_team, 'submission_attempts': submission_attempts,
        'submission_status': status, 'color_states': color_states,
        'problem_form_pairs': problem_form_pairs, 'is_past': is_past
    }

    return render(request, 'contests/contest.html', data)


@login_required()
def displayProblemDescription(request, contest_id):
    """ Display the problem description of a Contest.
    Only the contest creator, judges of a contest and superusers have access to it before the contest is activated.
    Once active, only the contest creator, judges, superusers and participants of a contest have access to viewing it.

    This page displays the program description (a pdf file) of a contest.

    :param request: None or POST
    :param contest_id: the Contest of which program description to be viewed
    :return: A rendered pdf display page
    """
    contest_data = Contest.objects.get(id=contest_id)
    is_judge = isJudge(contest_data, request.user)
    is_participant = isParticipant(contest_data, request.user)
    is_creator = isCreator(contest_data, request.user)

    if contest_data.contest_start is not None:
        if not is_judge and not is_participant and not is_creator and not request.user.is_superuser:
            return redirect(reverse('home'))
    else:
        if not is_judge and not is_creator and not request.user.is_superuser:
            return redirect(reverse('home'))

    path = contest_data.problem_description.path
    with open(path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=%s.pdf' %contest_data.problem_description.name
        return response

@login_required
def displayAllSubmissions(request, contest_id):
    """ Display all submissions of all participants in a Contest.
    Only the contest creator, judges of a contest and superusers have access to it.

    This page displays all submissions of all participants in the contest, separated as two panel, new and judged. In
    each panel the submissions are sorted by the time submitted, latest first.

    These two panels will be refreshed every 5 seconds.

    :param request: None or POST
    :param contest_id: the Contest of which submissions to be viewed
    :return: A rendered AllSubmission page
    """
    contest_data = Contest.objects.get(id=contest_id)
    is_judge = isJudge(contest_data, request.user)
    is_creator = isCreator(contest_data, request.user)
    is_past = contest_data.contest_end() <= timezone.now()

    if not is_judge and not is_creator and not request.user.is_superuser:
        return redirect(reverse('home'))

    problems = contest_data.problem_set.all()
    new_submissions = []
    judged_submissions = []
    for p in problems:
        submissions = list(p.submission_set.all())
        for sub in submissions:
            if sub.state == 'NEW':
                new_submissions.append(sub)
            else:
                judged_submissions.append(sub)
    new_submissions.sort(key=lambda x: x.timestamp)
    judged_submissions.sort(key=lambda x: x.timestamp)

    data = {
        'contest_data': contest_data, 'new_submissions': new_submissions,
        'is_judge': is_judge, 'is_creator': is_creator, 'is_past': is_past,
        'judged_submissions': judged_submissions
    }

    return render(request, 'contests/all_submissions.html', data)


@login_required
def displayMySubmissions(request, contest_id, team_id):
    """ Display all submissions of a team in the Contest.
    Only the contest creator, judges of a contest, superusers and members of the team have access to it.

    This page displays all submissions of the team with id of team_id in the contest, sorted by tthe time submitted,
    latest first.

    :param request: None or POST
    :param contest_id: the Contest of which submissions to be viewed
    :return: A rendered ContestSubmission page
    """
    contest_data = Contest.objects.get(id=contest_id)
    team = Team.objects.get(id=team_id)
    is_judge = isJudge(contest_data, request.user)
    is_past = contest_data.contest_end() <= timezone.now()

    if not is_judge and request.user not in team.members.all() and not request.user.is_superuser:
        return redirect(reverse('home'))

    problems = contest_data.problem_set.all()
    submissions = []
    for p in problems:
        submissions += list(p.submission_set.filter(team__pk=team_id))
    submissions.sort(key=lambda x: x.timestamp)

    data = {
        'contest_data': contest_data, 'team': team,
        'contest_submissions': submissions, 'is_past': is_past
    }

    return render(request, 'contests/user_submissions.html', data)


@login_required
def displayJudge(request, contest_id, run_id):
    """ Display judge page of a submission.
    Only the contest creator, judges of a contest and superusers have access to it.

    This page displays a diff table with two column, the left column displays the output of the participant's submission,
    the right column displays the desired output that was uploaded to problem output. The line that are different will
    be marked red. A banner containing 'previous' button and 'next' button will be on top of the page. By clicking on
    the button a user could jump to the previous or next line that is different.

    There is a drop down choice box at the bottom of the page. Judge could choose the result to return and click on
    submit. A notification object will be generated.

    :param request: None or POST
    :param contest_id: the Contest of which submission judge page to be viewed
    :param run_id: run_id of the submission
    :return: A rendered judge page
    """
    contest_data = Contest.objects.get(id=contest_id)
    is_judge = isJudge(contest_data, request.user)
    is_creator = isCreator(contest_data, request.user)
    is_past = contest_data.contest_end() <= timezone.now()

    if not is_judge and not is_creator and not request.user.is_superuser:
            return redirect(reverse('home'))

    problems = contest_data.problem_set.all()
    for p in problems:
            if p.submission_set.filter(run_id=run_id).exists():
                    current_submission = p.submission_set.get(run_id=run_id)
                    if request.method == 'POST':
                            form = ReturnJudgeResultForm(request.POST, instance=current_submission)
                            if form.is_valid():
                                    form.save()
                                    # create a new notification
                                    notification = Notification(submission=current_submission)
                                    notification.save()
                                    return redirect(reverse('contests:contest_judge_submissions',
                                                    kwargs={'contest_id': contest_id}))
                    else:
                            form = ReturnJudgeResultForm(instance=current_submission)
                    allowed_languages = getattr(contest_data, 'languages')
                    problem_inputs = getattr(current_submission, 'problem').problem_input.all()
                    input_files = []
                    for p_i in problem_inputs:
                        input_files.append(getattr(p_i, 'program_input'))
                    fromlines = []
                    if len(input_files):
                        input_files.sort(key=lambda x: x.name)
                        for input_file in input_files:
                            output = exe.execute_code(Popen, getattr(current_submission, 'code_file'), getattr(current_submission, 'original_filename'), input_file, allowed_languages, getattr(getattr(current_submission, 'problem'), 'timeout'))
                            fromlines.extend(output[1].split("\n"))
                    else:
                        output = exe.execute_code(Popen, getattr(current_submission, 'code_file'), getattr(current_submission, 'original_filename'), None, allowed_languages, getattr(getattr(current_submission, 'problem'), 'timeout'))
                        fromlines.extend(output[1].split("\n"))
                    #Use the solution file(s) if it(they) exists. If not, use empty expected output.
                    problem_solutions = getattr(current_submission, 'problem').problem_solution.all()
                    solution_files = []
                    for p_s in problem_solutions:
                        solution_files.append(getattr(p_s, 'solution'))
                    tolines = []
                    if len(solution_files):
                        solution_files.sort(key=lambda x: x.name)
                        for solution_file in solution_files:
                            tolines.extend(solution_file.read().decode().split("\n"))
                    html, numChanges = _diff.HtmlFormatter(fromlines, tolines, False).asTable()
                    return render(request, 'contests/judge.html', {'diff_table': html, 'numChanges': numChanges, 'contest_data': contest_data, 'is_judge': True, 'submission': current_submission, 'form': form})


def scoreboard(request, contest_id):
    #contest_id = request.POST.get('contestId', "0")

    scoreboard_contest = Contest.objects.get(id=contest_id) # Get contest ID from URL
    problems = Problem.objects.all()
    problems = problems.filter(contest=scoreboard_contest) # Filter problems to look at by contest
    problem_number = 0
    for problem in problems:
        problem_number += 1

    contest_time_penalty = int(scoreboard_contest.time_penalty)

    participants = scoreboard_contest.participant_set.all()

    problem_count_array = []
    for i in range(1, problem_number+1):
        problem_count_array.append(i)

    contest_title = scoreboard_contest.title

    problems_status_array = {}
    problem_score_array = {}
    problem_attempts_array = {}

    for participant in participants:
        teamname = participant.team.name

        tempteam = Team.objects.get(name=teamname)

        problem_score_array[teamname] = 0
        problem_attempts_array[teamname] = 0
        templist = []

        for problem in problems: # Iterate through problems and check submissions for right/wrong answer
            tempsubmission = Submission.objects.filter(team = tempteam, problem = problem)
            for object in tempsubmission :
                problem_attempts_array[teamname] += 1

            tempsubmission = Submission.objects.filter(team = tempteam, problem=problem).last()

            #filter submission by problem/team
            if(tempsubmission is None): # no submission given for this problem
                templist.append("3")
                problems_status_array[teamname] = templist
                continue
            elif(tempsubmission.result == 'YES') : # Correct answer
                templist.append("1")
                problems_status_array[teamname] = templist
                problem_score_array[teamname] += 1
            elif(tempsubmission.result == 'WRONG' or tempsubmission.result == 'OFE' or tempsubmission.result == 'IE' or tempsubmission.result == 'EO' or tempsubmission.result == 'CE' or tempsubmission.result == 'RTE' or tempsubmission.result == 'TLE' or tempsubmission.result == 'OTHER'): # Red
                templist.append("0")
                problems_status_array[teamname] = templist
            else:
                templist.append("2")
                problems_status_array[teamname] = templist # Otherwise the submission is pending

    for teamname in problem_attempts_array:
        problem_attempts_array[teamname] = problem_attempts_array[teamname] * contest_time_penalty

    is_past = scoreboard_contest.contest_end() <= timezone.now()

    data = {
        'problem_number' : problem_count_array,
        'contest_title' : contest_title, 'problem_status_array' : problems_status_array,
        'problem_score_array' : problem_score_array, 'contest_data':scoreboard_contest,
        'problem_attempts_array': problem_attempts_array, 'is_past': is_past
    }

    print("attempts")
    print(problem_attempts_array)

    return render(request, 'contests/scoreboard.html', data)


def show_notification(request):
    """ Helper method to show the notification modal

    The method will find the information of all notifications related to the request user's team, put the information in
    a dictionary, and send them to javascript.

    :param request: None or GET
    :return: A JsonResponse with data
    """
    l = []

    all_notifications = Notification.objects.all()
    for noti in all_notifications:
        submission = noti.submission
        team = submission.team
        if request.user in team.members.all():
            # data needed for showing notification

            noti_problem = Problem.objects.get(pk=submission.problem_id)
            problems = Problem.objects.filter(contest_id=noti_problem.contest_id)
            problem_number = 0
            for problem in problems:
                problem_number += 1
                if problem.id == noti_problem.id:
                    break

            # contest title, problem number, run id, and result
            current_data = (submission.problem.contest.title, problem_number,
                            submission.run_id, submission.get_result_display(), noti.id, submission.pk)
            l.append(current_data)

    d = {'data': l}
    return JsonResponse(d)


def close_notification(request):
    """ Helper method to delete the notification object

    The method will get the id of the notification to be deleted from ajax request, and delete the notification object.

    :param request: None or POST
    :return: A HttpResponse
    """
    modal_id = request.POST['id']
    print("modal id: " + modal_id)
    if Notification.objects.filter(id=modal_id).exists():
        current_notification = Notification.objects.get(id=modal_id)
        current_notification.delete()
    return HttpResponse('OK')


def refresh_scoreboard(request):
    contest_id = request.POST.get('contestId', "0")

    contest_data = None

    if contest_id != 0:
        contest_data = Contest.objects.get(id=contest_id)

    contest_time_penalty = int(contest_data.time_penalty)

    problems = contest_data.problem_set.all()

    problem_number = 0
    for problem in problems:
        problem_number += 1

    participants = contest_data.participant_set.all()

    problem_count_array = []
    for i in range(1, problem_number + 1):
        problem_count_array.append(i)

    problems_status_array = {}
    problem_score_array = {}
    problem_attempts_array = {}

    for participant in participants:
        teamname = participant.team.name

        tempteam = Team.objects.get(name=teamname)

        problem_score_array[teamname] = 0
        problem_attempts_array[teamname] = 0
        templist = []

        for p in problems:

            tempsubmission = Submission.objects.filter(team = tempteam, problem = problem)
            for object in tempsubmission :
                problem_attempts_array[teamname] += 1

            tempsubmission = Submission.objects.filter(team = tempteam, problem=p).last()

            #filter submission by problem/team
            if(tempsubmission is None): # no submission given for this problem
                templist.append("3")
                problems_status_array[teamname] = templist
                continue
            elif(tempsubmission.result == 'YES') : # Correct answer
                templist.append("1")
                problems_status_array[teamname] = templist
                problem_score_array[teamname] += 1
            elif(tempsubmission.result == 'WRONG' or tempsubmission.result == 'OFE' or tempsubmission.result == 'IE' or tempsubmission.result == 'EO' or tempsubmission.result == 'CE' or tempsubmission.result == 'RTE' or tempsubmission.result == 'TLE' or tempsubmission.result == 'OTHER'): # Red
                templist.append("0")
                problems_status_array[teamname] = templist
            else:
                templist.append("2")
                problems_status_array[teamname] = templist # Otherwise the submission is pending

    for teamname in problem_attempts_array:
        problem_attempts_array[teamname] = problem_attempts_array[teamname] * contest_time_penalty

    print("time penalty")
    print(contest_time_penalty)

    data = {
        'problem_number': problem_count_array,
        'problem_status_array' : problems_status_array,
        'problem_score_array' : problem_score_array,
        'problem_attempts_array' : problem_attempts_array
    }

    return render(request, 'contests/scoreboard_div.html', data)


def refresh_submission(request):
    """ Helper method to refresh the div in all_submission page.

    The method will get the id of the contest to be refreshed from ajax request, and render the div to be refreshed.

    :param request: None or POST
    :return: A renderd div
    """
    contest_id = request.POST.get('contestId', "0")
    print("contest_id: " + contest_id)

    new_submissions = []
    judged_submissions = []
    contest_data = None

    if contest_id is not "0":
        contest_data = Contest.objects.get(id=contest_id)

        problems = contest_data.problem_set.all()
        for p in problems:
            submissions = list(p.submission_set.all())
            for sub in submissions:
                if sub.state == 'NEW':
                    new_submissions.append(sub)
                else:
                    judged_submissions.append(sub)
        new_submissions.sort(key=lambda x: x.timestamp)
        judged_submissions.sort(key=lambda x: x.timestamp)

    data = {
        'contest_data': contest_data, 'new_submissions': new_submissions,
        'judged_submissions': judged_submissions
    }

    return render(request, 'contests/submission_div.html', data)
