# Uncovered Code

### contests/lib/execution.py
    * Lines 126-127
    ```python
    result = docker_container_code(Popen, sys.argv)
    print(str(result[0]) + ',' + str(result[1]), end='')
    ```
    ** These lines are not covered because they have to be run in the docker container. The docker container runs execution.py directly, causing the lines to be hit. They will not work outside of the container because the file system on the docker container is set up in a specific way that is not the same on the PICO system. Dependency injection is also not possible in this situation since the file is run directly, so we cannot mock the objects in the main if statement. However, it is reasonable to assume that these two lines work properly because I have written several tests that kick off the docker container, run the lines, and check the output. Unfortunately, the Coverage3.py cannot recognize code covered inside the docker container. In addition, I have tested the docker_container_code function from line 126 in isolation, ensuring it works properly.