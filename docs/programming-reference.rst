app/teams
===============

forms.py
------------------
    class TeamForm(forms.ModelForm)
        Team creation form with a name field.

    class TeamSearchForm(forms.ModelForm)
        Uses the autocomplete library functionality to search through the Team object queryset.

    class JoinRequestForm(forms.ModelForm)
        Form for user to request to join a private team.

    class InviteForm(forms.ModelForm)
        Form for user to invite another user to a team.

models.py
------------------
    class Team(models.Model)
        Stores the team name, date created, team members, and if the team is public or private.

    This file also contains the models for invite requests and join requests.

views.py
------------------
    def join(request)
        User will join the selected team if it exists and if it is public or the user was invited.

    def invite(request, action)
        Takes in one of four possible actions:

        1. send - An invite form was submitted, sending a user a team invite if they are not already on the team and don't already have an unanswered invite to it. An alert of the invite is also passed to the user.

        2. accept - User accepts an existing invite.

        3. decline - User declines an existing invite.

        4. cancel - An invite form was canceled before being submitted, deleting the invite object.

    def join_request(request, action)
        Takes in an action that is either "accept" or "decline".

        This function allows any member of the team to accept or decline the request for a user to join the team.

    class TeamAutoComplete(autocomplete.Select2QuerySetView)
        This class loads the dal autocomplete library to dynamically get the query set of possible users when searching in the team forms.
        
app/users
===============

lib/storage.py
------------------
    Calculates the amount of disk space used by PiCO on the system and remaining free space. This is displayed using Highcharts. This functionality is mainly meant for the server admins and contest organizers.

forms.py
------------------
    class UserForm(UserCreationForm)
        Standard user registration form that requires a username and password. Optional fields are first name, last name, and email address.

    class LoginForm(AuthenticationForm)
        See https://docs.djangoproject.com/en/1.10/topics/auth/default/#django.contrib.auth.forms.AuthenticationForm

    class UserSearchForm(forms.ModelForm)
        Uses the autocomplete library functionality to search through the User object queryset.

models.py
------------------
    class User(AuthUser)
        Can fetch user profile. Also handles setting permissions.

    class UserProfile(models.Model)
        Has a user and theme.
        The theme field stores a URL of the current Bootswatch theme the user has chosen.

views.py
------------------
    Handles User account registration, login, logout, and profile editing.

    def edit(request)
        Allows the editing of username, first name, last name, email, and theme.

        Theme editing brings up another page of all the available Bootswatch options.

    def settings(request)
        Gets the storage spaced used and remaining, then displays it on a separate page using Highcharts.

app/vendor
===============
    Contains all external libraries used:
    
    - bootstrap
    - bootstrap-toggle: converts bootstrap checkboxes into toggles
    - font-awesome: font and CSS toolkit to integrate icons as font
    - highcharts: interactive JS charts and graphs
    - jQuery
    - jquery-formset: dynamically add and remove formsets within a form
    - moment: JS date library for parsing, validating, manipulating, and formatting dates
    - stickytabs: provides pushState (back and forward button support) to Bootstrap tabs

