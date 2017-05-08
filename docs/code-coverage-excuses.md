# Uncovered Code

### contests/lib/execution.py
* Lines 126-127
   ```python
   result = docker_container_code(Popen, sys.argv)
   print(str(result[0]) + ',' + str(result[1]), end='')
   ```
   - These lines are not covered because they have to be run in the docker container. The docker container runs execution.py directly, causing the lines to be hit. They will not work outside of the container because the file system on the docker container is set up in a specific way that is not the same on the PICO system. Dependency injection is also not possible in this situation since the file is run directly, so we cannot mock the objects in the main if statement. However, it is reasonable to assume that these two lines work properly because I have written several tests that kick off the docker container, run the lines, and check the output. Unfortunately, the Coverage3.py cannot recognize code covered inside the docker container. In addition, I have tested the docker_container_code function from line 126 in isolation, ensuring it works properly.

### contests/static/js/timer_bar.js
* Lines 66, 72-73
    ```javascript
    window.alert("You have 1 minute remaining.");
    ```
    ```javascript
    window.alert("The contest is now over! You may view it 1 minute after it has ended.");
    window.location.replace(home_url);
    ```
    - I wasn't able to get these to work with Qunit and from the sources I read online, alerts are difficult to deal with. But I do know that the qunit test does go into the if statements and the alerts themselves even pop up eventually on the qunit.html page. I have also extensively tested that these alerts pop up as intended during a live contest.

### contests/static/js/lock_timer_bar.js
* Lines 15-16
    ```javascript
    timer_bar.fadeIn(400).removeClass('fixed');
    $('html, body').css('height', body_height);
    ```
    - The conditional `distanceFromTop >= height_above_timer` to get to these lines of code works fine in any real situation because the height_above_timer can only be a minimum of 0 on a real webpage, but for some reason on qunit's, the height_above_timer is always -9800. I can't find any reasonable work around that doesn't require obscure and needless changes to the js file itself. Nor can I find any way to get qunit to adjust this height back to a normal non-negative range. I was able to change multiple things to get qunit to test that the code inside the else statement actually works though so I am confident the code works as intended, it just isn't realistic to have a devote qunit test to it though.

### contests/static/js/notification.js
* Line 39
   ``` javascript
   onModalClose($(this).attr('id'));
   ```
   - This line should be called when a bootstrap modal is closed. However, I couldn't get bootstrap modal work in jquery test. It should come with bootstrap by default but the any bootstrap modal operation is not recognized. I also tried to include the bootstrap modal source code as dependency separately but still got no luck. Beside using bootstap modal call, I tried perform a regular click on the screen (becaue that will close the modal) or treated it as a listener for ```'hidden.bs.modal'``` event, but either way I can't get lines in this event covered. So instead I put action I want to perform when the event is triggered inside an ```onModalClose``` function and tested that function individually. Leaving the line calling that function not covered.
