# Python 3.11


# Backend Engineer Test Task

## Write a Python program that accepts the following arguments:
### Arguments:

    A name of a Docker image
    A bash command (to run inside the Docker image)
    A name of an AWS CloudWatch group
    A name of an AWS CloudWatch stream
    AWS credentials
    A name of an AWS region

### Example:
    python main.py \
    --docker-image python \
    --bash-command $'pip install pip -U && pip install tqdm && python -c \"import time\ncounter = 0\nwhile True:\n\tprint(counter)\n\tcounter = counter + 1\n\ttime.sleep(0.1)\"' \
    --aws-cloudwatch-group test-task-group-1 \
    --aws-cloudwatch-stream test-task-stream-1 \
    --aws-access-key-id ... \
    --aws-secret-access-key ... \
    --aws-region ...

### Functionality
    The program should create a Docker container using the given Docker image name, and
    the given bash command
    The program should handle the output logs of the container and send them to the given
    AWS CloudWatch group/stream using the given AWS credentials. If the corresponding
    AWS CloudWatch group or stream does not exist, it should create it using the given
    AWS credentials.

### Other requirements
    The program should behave properly regardless of how much or what kind of logs the
    container outputs.
    The program should gracefully handle errors and interruptions.

#### For testing purposes, you can use the following AWS credentials:
    AWS_ACCESS_KEY_ID=SOME_KEY
    AWS_SECRET_ACCESS_KEY=SOME_SECRET_KEY
