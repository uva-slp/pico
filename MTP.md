#PiCO - Master Test Plan (v0.9)

Austin Petrie, Derek McMahon, Jason Deng, Jamel Charouel, Nathan Williams, Vivian Liu  
*In collaboration with Aaron Bloomfield and Mark Floryan of the University of Virginia
Spring 2017*


###Tools, Techniques, Methods, and Metrics  
Our project uses the Django framework.  Therefore, we are using Django’s built-in testing functions to create and run our unit test cases.  We are using TravisCI for continuous integration testing and Coveralls for code coverage testing.  During the development process, our client Mark Floryan conducts usability testing by demoing our project.  

After our project has been deployed, it will likely be tested by a small group of individuals as improvements to the system get added.  They will likely use the same software and methods for testing as we have thus far.

###Test Processes  
As the features of our project are developed, unit tests are created to test each component.  When added to the rest of the code base, TravisCI handles integration testing.  Every two weeks, our team meets with Mark Floryan, where he does a demo of our system in front of us for usability testing.  At some point, he will likely conduct a full feature demo with a group of students to simulate an ICPC contest, where he will turn to the students for acceptance testing.

###Tested Parts of the System  
Testing is focused on components of our system pertaining to the main functionality of our system:  
1. Login management  
2. Contest creation and management  
3. Team creation and management  
4. Code submission and execution  
These components are the bulk of what our system is, so they have the most rigorous unit tests and testing cases.  All other components are still tested, but not to the extent of the aforementioned components.

Each component operates using Django, a MVC architectured framework.  Therefore, each component is split into three parts.  For view components, unit tests are created for each view to determine whether or not the proper information is displayed.  Through usability testing, we can also determine if this is done in an aesthetically pleasing and logical manner.  For controller components, many test cases are run to ensure that data is properly communicated from our backend databases to the proper views, as well as to ensure that data being entered from the views by users are properly interpreted and input into our system.  For model components, we test to ensure that they hold proper, valid data.  Usability testing also determines how appropriate our models are towards fulfilling our functional and usability requirements.

###Testers  
Currently, testing will be done by the development team and Mark Floryan (installation and usability testing).  Once the development team graduates, testing responsibilities will be handed off to a small group of individuals, likely students and faculty.  Responsibilities regarding who should test what components will be decided at that time.  It is possible that some or all of the members of the development team will still be able to participate in testing after graduation.

###Tested functionality  
For all components of the project that input data into our database (user, team, contest, and submission management), extensive test cases are created to test for corner case conditions and malformed inputs.  Even if administrators were to try to create malformed model instances as a superuser, our test cases would be able to detect and prevent these erroneous objects from being added to the database.

Many fixtures have been created to generate sample data that create specific environments we want to test in (ie. corner case conditions).  This allows our tests to be very comprehensive without having to create these dangerous conditions on our real server.

###Determining What Tests to Write  
Using Coveralls, we are able to see what portions of our code are covered by our unit tests.  This lets us know which components still require coverage.  Usability testing also gives us a good indication of how users typically interact with different components of the system, giving us a foundation of unit test ideas to implement.  

Django’s testing suite and documentation provides us with all of the necessary information to form appropriate unit tests for each model, view, and controller component of the system.  As new features are developed, proper tests for each component are also generated.

###Test Labeling  
Our unit tests are named in such a way that it is clear what they are testing.  For tests that are more complicated, a comment is added to the unit test to indicate its purpose.  Functional requirements direct unit tests to be created that test the components needed to meet those requirements.  Usability testing directs development focus to work on what the customer deems important to the system and how it should operate.

###Specific Test Plan Outline  
Installation test:  
*Users will follow an installation instruction manual that provides directions for how to install the PiCO system on a previous unconfigured machine.  This includes all of the necessary prerequisite software needed to host our platform.  Ideally, we would be able to also provide an installation script to make this process easier.  
Usability testing:
*PiCO is designed as a contest control platform.  Therefore, usability testing will be driven by the implementation of the contests being held.  As users decide how they would like their contests managed or how users interact with the contests, the structure of the system may change.  
Requirements testing:  
*When all of the functional and usability requirements defined by the customer have been satisfied, then our requirements testing will have been complete.  Of course, this means that all of the components of our system have also been tested for security, usability, functionality, etc.  
