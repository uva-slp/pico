# Specific Test Plan

## Installation Testing

Our installation test was performed by following our installation instructions on a previously unconfigured machine. They were completed on a VirtualBox 64-bit image of Ubuntu 16.10.  The Advanced Packaging Tool (apt) was used as the package manager for the installation test.  Following the installation, the installation test was successful and passed, as it met all of the functional and usability requirements outlined by our client after the installation.  For future testing, the installation test will be considered passing if it still meets all of the functional and usability requirements on the new system.  

## Security Testing

Many security measures are already taken by using Django’s built-in functions, such as login authentication.  Using Django templates protects against XSS attacks, and Django forms automatically sanitize input against SQL injection attacks.  When registering an account, users are unable to create an account using a password containing fewer than 8 characters.  Users are also unable to use common passwords, such as “password”.  Due to the length requirement of the password, bot-based login attempts are ineffective.  Several unit tests are used to check what permissions certain users have before accessing confidential information.

## Usability Testing

People will be using all of the functionality that the site has to offer.  Four test subjects unaffiliated with the development team nor the client were asked to use the system.  They all stated that the sidebar form of navigation was unnecessary, causing us to switch to a navbar style of site navigation.  For contest creation and judging, some explanation was required, as subjects without any prior knowledge of programming would have had a difficult time understanding what correct programming submissions look like, or what it means to run a programming contest.  Their input was also important in deciding which pieces of information were most important, such as contest time remaining, so that that information would be easily accessible or always visible.

## Compatibility Testing

We will execute the requirements test on the most recent version of the major web browsers (Firefox, Chrome, Internet Explorer, and Safari).  If and only if the requirements test passes on all of these browsers, then the compatibility test will be considered to have passed.

## Requirements Testing

The functional requirements for our system were given to us by our client.  Additionally, several of the optional functionalities were implemented as well and include many usability requirements.  To test these, our system was put through usability testing to determine what functional or usability requirements have not been met yet.  To test this, users will go through every requirement in the requirements list to determine whether or not the system satisfies the requirement.  Code coverage using TravisCI ensured that our code was operating properly as well.
