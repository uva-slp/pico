# Uncovered Code

### contests/lib/execution.py
* Lines 126-127
   ```python
   result = docker_container_code(Popen, sys.argv)
   print(str(result[0]) + ',' + str(result[1]), end='')
   ```
   - These lines are not covered because they have to be run in the docker container. The docker container runs execution.py directly, causing the lines to be hit. They will not work outside of the container because the file system on the docker container is set up in a specific way that is not the same on the PICO system. Dependency injection is also not possible in this situation since the file is run directly, so we cannot mock the objects in the main if statement. However, it is reasonable to assume that these two lines work properly because I have written several tests that kick off the docker container, run the lines, and check the output. Unfortunately, the Coverage3.py cannot recognize code covered inside the docker container. In addition, I have tested the docker_container_code function from line 126 in isolation, ensuring it works properly.
   
### contests/static/js/notification.js
* Line 39
   ``` javascript
   onModalClose($(this).attr('id'));
   ```
   - This line should be called when a bootstrap modal is closed. However, I couldn't get bootstrap modal work in jquery test. It should come with bootstrap by default but the any bootstrap modal operation is not recognized. I also tried to include the bootstrap modal source code as dependency separately but still got no luck. Beside using bootstap modal call, I tried perform a regular click on the screen (becaue that will close the modal) or treated it as a listener for ```'hidden.bs.modal'``` event, but either way I can't get lines in this event covered. So instead I put action I want to perform when the event is triggered inside an ```onModalClose``` function and tested that function individually. Leaving the line calling that function not covered.
