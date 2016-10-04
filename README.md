# pccs

# Repo for UVA Programming Contests Capstone Project

## Requirements: Minimum

- Instructor accounts, user levels, and password reset
- Contest creation, setting of programming language options, and contest problems
- Creation of team accounts, and login by the teams
- Proper execution of the problems with error detection if something goes wrong
  - Only using PC^2 format; no validators
  - Execution is handled by the web server
- Ability to judge, both by computer and human
- Scoreboard creation display
- Basic web interface
- The ability of the system to work for many contests: each one has it's own teams and problems (although some will be shared), and an instructor's login will show all past contests (and can pull up data about each)


## Requirements: Desired

- Use of the Kattis format for problem creation
- Ability to use validators for problem judging
- Implementation of many (if not all) of the features currently handled by PC^2
- Fully fledged, easy to use, and nice looking web interface
- Flexible execution system that will allow new execution environments to be easily added
  - Also, the ability to "farm out" the judging to external clients
- Generation of reports, graphs, and statistics
- More advanced ways to have the computer judge and view wrong answers, including intelligent diff comparisons
- Proper following of the [contest control standards](https://clics.ecs.baylor.edu/index.php/Contest_Control_System)
  - It may be that following them all is beyond the scope of the desired requirements; if so, then the system should be flexible enough that aligning the system with those standards is feasible
