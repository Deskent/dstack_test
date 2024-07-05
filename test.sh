BASH_COMMAND=$'pip install pip -U && pip install tqdm && python -c \"import time\ncounter = 0\nwhile True:\n\tprint(counter)\n\tcounter = counter + 1\n\ttime.sleep(0.1)\"'

python main.py \
  --docker-image python \
  --bash-command "${BASH_COMMAND}"
#   \
#  --aws-cloudwatch-group test-task-group-1 \
#  --aws-cloudwatch-stream test-task-stream-1 \
#  --aws-access-key-id ... \
#  --aws-secret-access-key ... \
#  --aws-region ...
