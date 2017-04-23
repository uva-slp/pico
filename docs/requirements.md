# SLP Requirements

# ACM / ICPC

__Nonprofit overview:__ This is a required open source project that will benefit the overall programming contest community, which is composed of students, faculty, and industry representatives throughout the world that are interested in the promotion of competitive programming.

__Contact:__ Mark Floryan, mfloryan@virginia.edu, 434.243.3087

__Website:__ [http://acm.cs.virginia.edu/icpc.php](http://acm.cs.virginia.edu/icpc.php)

__System summary:__ A system to manage the submission and execution of submitted programming contest solutions, as well as the judging thereof.

__Development notes:__ No platform preference.  **THIS IS AN OPEN SOURCE PROJECT.**  Students working on this project will have to agree, via a signed contract at the start, to release their code under an open source license (default is Apache unless the group -- and instructor -- mutually decide otherwise).

__Confidentiality notes:__ The standard [course NDA](http://aaronbloomfield.github.io/slp/uva/legal.html) is expected to have to be signed


## System Description and Features

Programming contests present a number of problems to contestants, who submit solutions, called runs.  Runs are judged by a computer and/or a human.  A scoring metric is applied, and a scoreboard displayed.

There are a number of existing systems that students on this project should familiarize themselves with:

- [PC^2](http://pc2.ecs.csus.edu/): the most widely used system.  Although it is free, it is closed source, and *very* buggy -- to the point of often not being able to properly judge contests.  It has not kept up with the advances in contest judging.
- [Kattis](https://open.kattis.com/): a much more modern system, it runs through a web browser.  However, it only runs on their servers, and it is not open source.  One cannot easily configure their own contests; they have to have the Kattis group configure them for you.  Thus, it is difficult to use in practices.
- [DOMjudge](https://www.domjudge.org/): an open source system, but one that is not widely used.  It does 

Problems are specified in two different formats:

- PC^2 will accept a judging input and a judging output; the program, once compiled, is run with the judging input and compared (using various criteria: default, ignore case, ignore white space, etc.) with the judging output
- Kattis has a different format; see [here](https://github.com/Kattis/problemtools)

There are a number of ways to handle execution of the programs.  The easiest way is to have the web server run the programs once they are submitted (possibly putting them in a queue to prevent them all from executing at the same time).  A better way is to have separate clients connect to the main server, and the clients do the execution on separate machines.  One could "sandbox" the execution, whether it is on separate clients or on the web server.

If a problem has only one answer, then the above will work fine.  If there are multiple correct answers, then a *validator* program will have to be written as well.

UVa has significant experience with programming contests, and somebody can answer many questions that will come up.  Some examples: execution environments, validator examples, problem examples, problems with existing systems, etc.


## Requirements: Minimum

- User accounts and password reset
- Contest creation, setting of programming language options and contest problems
- Creation of teams/participants in a contest
- Proper execution of the problems with error detection if something goes wrong
  - Only using PC^2 format; no validators
  - Execution is handled by the web server
- Ability to judge by human
  - Allow judge to send specific messages to competitors, whether they be custom or based on the error
- Scoreboard display
  - Show all competitors and their scores (optional graphics)
  - Include link to scoreboard on main contest page, doesn't need to be in the way of more important information
- Basic web interface
  - Contests page for when a contestant is participating in a contest
  - Includes simple interface that gives all pertinent information without the need for a contestant to search for anything
  - Change question box color based on submission status (red = wrong, yellow = waiting for judge, green = correct)
  - Display each individual problem, can show input description, output description, sample input, and sample output
  - Landing Page: Show the contest(s) you're a part of at that moment, pasts contests, contests you've created
- The ability of the system to work for many contests: each one has it's own teams and problems (although some will be shared), and an contest creator's login will show all past contests (and can pull up data about each)
- Admin Page
  - Have various settings for contest creation, allow for default settings per admin across contests so that settings don't need to be inputted for every question/contest created by that admin
  - Ability to start/activate a contest
  - Autojudge option, shows judge what failed


## Requirements: Desired

- Use of the Kattis format for problem creation
- Implementation of many (if not all) of the features currently handled by PC^2
- Fully fledged, easy to use, and nice looking web interface
- Window flashes orange in the taskbar when an alert is given to competitors
- Admin Page
  - Copy contest settings for new contest
  - Highlight diff of candidate submission and judge submission for easy readability by judge. Allow options such as ignore whitespace
  - Admin role by contest, not for overall system (e.g. a student can be an admin for a specific contest)
- Flexible execution system that will allow new execution environments to be easily added
- Generation of reports, graphs, and statistics
- More advanced ways to have the computer judge and view wrong answers, including intelligent diff comparisons
- Proper following of the [contest control standards](https://clics.ecs.baylor.edu/index.php/Contest_Control_System)
  - It may be that following them all is beyond the scope of the desired requirements; if so, then the system should be flexible enough that aligning the system with those standards is feasible


## Requirements: Optional

- More flexible grading, so that this type of system could be used in a class, for example. This implies the ability to configure scoring metrics.
- The ability to *theme* the web interface to mimic existing systems, or to create new themes
- Fully sandboxed execution environments
- Ability to use validators for problem judging
