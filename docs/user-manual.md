# PiCO User Manual

## Introduction

PiCO is a system designed to make running coding contests easy and smooth. Features include contest template creation for quick contest reuse, team management and invites, smart submission diffs for easy judging of submissions, and more. This manual is meant to be used to understand how one can create a contest and run it from start to finish with several participants and problems to be solved.

## Site Features

### Login

The site is available [here](http://libra.cs.virginia.edu/pico). If you don't already have an account, you can register by clicking on "Register" to the right of "Login" and filling out the registration form. Be sure to choose a password that is at least 8 characters long and is not too common. Your name will be used for your profile and your email will be used in case you forget your password and need to reset it. The account is automatically activated once you have successfully registered, and you will be logged in automatically after you are registered.

If you already have an account, you can login by entering your username and password and clicking submit at the bottom of the form. If you have forgotten your password, you can click "Forgot password" next to the submit button, type your email associated with the account into the subsequent form, and hit the submit button. You will then receive an email with instructions on how to reset your password. This option is only available when the email has a valid user account associated with it.

### Main Site Page

After you log in you will be taken to the main site page where you can access active, unstarted, and past contests. From this page you can also navigate to the team management page as well as the statistics page, where you can view and join teams and see interesting statistics regarding contests, respectively. At the top right of the page, you can view any alerts that you have (in terms of invites or contest submission changes), as well as navigate to your user profile where you can change your username, password, and other account information. From the main page you can also begin the contest creation process by clicking the 'New Contest' button at the left of the page.

Contests that have already been created will be shown on the main site page and fall under either active contests, unstarted contests, or past contests, depending on their status. Your contest invitations will also be shown here, if you have any. If you do, you may click 'accept' to accept an invitation, and the contest will be placed in your contest table on the main site page. If you decline, you will not be added to the contest.

### Team Management

Click on the "Teams" button on the nav bar on the top of the page to navigate to team management page. To create a new team, click on the "New Team" button on the left and enter the name of the team in the popup window. The name of the team should be unique.

The left of the page shows a list of teams you're currently in, click on the name to view detailed information of that team. You can also view information of teams you're not in by searching the team name in the left search bar. You can view members of that team, and also have the option of joining the team by clicking on the "join" button.
Any members of a team can choose to set the team as "private" or "public" by toggling the button at the top of the team page. If a team is public, any user can join the team without any extra steps. If the team is private, a join request will be created and only when a member of said team accepts the request can the requesting user join the team. A member of the team can also invite other users to join the team by click on "New" next to the "invite" panel on the team page. The user who received the invitation must accept the invitation before actually joining the team.

A team does not have a limit in the number of members that can join. You must be in a team in order to participate in a contest.

### Contest Management

Click on the "Contests" button on the nav bar on the top of the page to navigate to the contest management page. This page is also the home page once you have initially logged in.

### Create a Contest

To create a contest, click on the "New Contest" button on the left of the contest management page, it will redirect you to the contest creation page. You can either create a contest from scratch or load a contest template.

A contest template is a default template that records your preference of contest length, languages, time penalty, admins and participants. It saves you time configuring similar information for contests by filling in the information automatically when you click 'load template' after creating one yourself. To create a contest template, click on "Create Template" button at the top of the page. Be sure to follow the format of "hours:minutes" (e.g. 02:00) for the contest length. Once you've enter the information properly, hit "Create Template" and the template will be saved. No notification will be sent to the user you added as admin/participant in the template.

To load a template, select a template from the drop-down box at the top of contest creation page and hit "Load Template". The information you saved in the template will be loaded automatically. You can still edit these fields if you wish.

When creating a contest, there are many fields you must fill out in order for the system to properly display the contest to both the judges and the participants. The problem description is designed to be a single pdf file that contains the descriptions of all problems in the contest. You must upload a .pdf format file for the program description. Description of input and output of a problem are text fields that guide participants what the format of input and output files should look like. Sample input and output are .txt files that contain example(s) of the test case and expected output. Problem input and solution are the actual test cases that would be used to judge the submission. These two fields won't be visible to participants. Problem input, solution, sample input and output are not required but must be .txt format if you do upload them. Problem input and solution will also allow multiple files. To upload multiple files, after clicking the upload button select all of the files that you want included. At runtime these will all be used as input to the program (or expected output if it is the solution), and are executed in lexicographic order by file name. A good way to make sure they are executed in the order you want is to name all of the input files with the same prefix and then add numbers to the ends of the names in the order that you want them executed.

By default there is one problem in the contest creation page. You can add or remove a problem by click on the "add problem" and "delete problem" button. There is no lower or upper limit of the number of problems in a contest.

If you are the creator of the contest, you have all privileges a judge of the contest has. To add other judges, search for and choose the user next to "Contest admins", the user will show up in the search bar. You can add multiple judges by continue the process, or remove a judge by click on the cross next to their name.

The process of adding participants is similar to that of adding judges, except that you need to search for and choose a team next to "Contest participants", rather than individual users. Invitations for joining the contest will be sent to the teams once you've created the contest. A member of the team needs to accept the invitation before the team is actually added as a participant of the contest.

### Activate/Edit/Delete a Contest

After a contest is created, it will appear in the "Unstarted contest" panel on the contest management page. A judge or creator of the contest can activate, edit, or delete the contest. Note that on the edit contest page, if you want to update a problem you must upload input and solution files again (if left blank, there will be no input or solution files associated with that problem).
Activation of a contest indicates the contest is started. Participants won't be able to view information of the contest before it is activated. Once a contest is activated its timer will begin and the participants will be able to submit solutions to contest problems.

### Participate in a Contest

If the team you're in is invited to a contest, an invitation will shows under the "contest invitations" panel on the contest management page. You could either accept or reject the invitation. Only one member of the team need to accept the invitation before the team is added as participant of the contest. The contests you have participated/ will participate in will show up in the contest management page.

Clicking on the name of an active contest will lead you to the contest detail page. At the top of the page is the time progress bar which shows how many time is left for the contest.

Below the time bar are three buttons: "scoreboard", "problem description", and "view my submission", which lead you to the pages accordingly. Scoreboard shows the ranking of all participants of the contest as well as detailed information such as total score, number of attempts for each problem and current status of the problem (pending, right, or wrong) of each team. The scoreboard is updated and refreshed automatically. "Problem description" shows the content of the pdf file. "View my submission" shows all previous submission of your team and the result of it.
At the bottom of the pages are the problems of the contest. The tab is default folded, with the number of attempts showing, and colored according to the status (grey for no attempt, yellow for submission pending, red for wrong answer, green for correct answer). Click on the tab to bring out detail of the problem such as description of input, description of output, sample input, sample output. To submit an attempt to the problem, click on "choose file" at the bottom of the problem detail panel, choose a file to upload, and hit "submit". The file will be uploaded to server and a judge of the test would be able to view and judge it. Once the submission is judged, a notification window will pop up showing the result of your submission. Click anywhere on the screen to close that window.

### Judging Problem Submissions

If you are a judge of a contest, while on the contest page you can view all submissions that have been made by clicking on the "View all submissions" button in the Judge Panel. In this view you will see two tables: first any submissions that have not yet been judge in the order that they were submitted, and second any submissions that have been judged. You can judge or re-judge a submission in either table by clicking the "Judge" button to the right of a given submission.

This will take you to a page showing you the output of the participant's submitted program. Adjacent to that output is the expected output of a correct program. Differences between the two are highlighted in red and similarities are not highlighted. In the top right of this diff table are buttons labeled "first", "prev", "next", and "last". Clicking "first" will take you to the first difference between the two files, "prev" will take you to the preceding difference from the one you are currently viewing, "next" will take you to the difference after the one you are currently viewing, and "last" will take you to the last difference between the two files.

To the right of these navigation buttons are two radio buttons labeled "Whitespace" and "Empty lines". When "Whitespace" is checked it counts difference in whitespace within non-empty lines as differences between the files, but it ignores them if it is unchecked. Empty lines behaves in an identical manner but regarding completely empty lines. Finally, to judge a submission, at the bottom of the diff table there is a dropdown menu from which a judgement can be chosen. The possible judgements are "Yes", "Wrong Answer", "Output Format Error", "Incomplete Error", "Excessive Output", "Compilation Error", "Run-Time Error", "Time-Limit Exceeded",  and "Other-Contact Staff". The "Submit" button in the bottom right of the diff table can then be clicked to submit the judgement. When a judge judges a submission, users relevant to that submission are given a notification on whatever page they are viewing, so that they are reminded to check the scoreboard to see if they got the submission correct or not, and what type of error they were given if their submission was incorrect.

## Miscellaneous Features

### User Profile

From the main landing page, your user profile by clicking on the user drop down icon in the top right corner of the navbar and then clicking the 'My Profile'. From this page you may change aspects of your account such as your username, password, first and last name, and email.  If another user accesses your profile, they will be able to see basic contact information about you, such as name and email address.

### Statistics

From the main landing page, you can navigate to your statistics page by clicking on the 'Statistics' button on the navbar. From here, you can view interesting statistics such as your most successful team that you have been on, contests you've participated in, and lifetime correct submissions that you've made.  As users participate in more contests, this page will fill up more!
