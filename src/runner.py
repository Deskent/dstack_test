import argparse
import subprocess
import sys
from subprocess import CompletedProcess

from .config import logger, LOGS_DIR


class DockerRunner:
    def _parse_arguments(self):
        """Parse command line arguments."""

        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--docker-image',
            type=str,
            required=True,
            action='store',
            help='Docker image to be used',
        )
        parser.add_argument(
            "--bash-command",
            required=True,
            action="store",
            type=str,
            help="Bash command to be executed",
        )
        parser.add_argument(
            "--aws-cloudwatch-group",
            required=False,
            action="store",
            type=str,
            help="AWS CloudWatch group",
        )
        parser.add_argument(
            "--aws-cloudwatch-stream",
            default=None,
            required=False,
            action="store",
            type=str,
            help="AWS CloudWatch stream",
        )
        parser.add_argument(
            "--aws-access-key-id",
            default=None,
            required=False,
            action="store",
            type=str,
            help="AWS CloudWatch access key",
        )
        parser.add_argument(
            "--aws-secret-access-key",
            default=None,
            required=False,
            action="store",
            type=str,
            help="AWS CloudWatch secret access key",
        )
        parser.add_argument(
            "--aws-region",
            default=None,
            required=False,
            action="store",
            type=str,
            help="AWS CloudWatch region",
        )

        return parser.parse_args()

    def _run_docker(
        self,
        command: str,
        stderr,
        stdout,
    ) -> 'CompletedProcess':
        """Run docker with parameters."""

        logger.info(
            f'\n\n\t\tRunning docker command: {command}'
            f'\nError output: {stderr}\nStdout: {stdout}'
        )

        result: 'CompletedProcess' = subprocess.run(
            args=[command],
            shell=True,
            stderr=stderr,
            stdout=stdout,
        )

        return result

    def run(self):
        params: argparse.Namespace = self._parse_arguments()

        logger.info(f'Running docker with parameters: {params}')

        output_logs_file = LOGS_DIR / 'docker.logs'
        output_errors_file = LOGS_DIR / 'docker_errors.logs'
        stderr = open(output_errors_file, 'a', encoding='utf-8')
        stdout = open(output_logs_file, 'a', encoding='utf-8')

        command: str = (
            f'docker run {params.docker_image} {params.bash_command} '
        )

        driver: str | None = None
        if params.aws_cloudwatch_group is not None:
            driver = 'awslogs'
        if params.aws_cloudwatch_stream is not None:
            driver = 'awslogs-stream'

        if all(
            (
                driver,
                params.aws_access_key_id,
                params.aws_secret_access_key,
                params.aws_region,
            )
        ):
            command += (
                f'--log-driver={driver} '
                f'--log-opt awslogs-region={params.aws_region} '
                f'--log-opt awslogs-group={params.aws_cloudwatch_group} '
                f'--log-opt awslogs-create-group=true'
                f'--env AWS_ACCESS_KEY_ID={params.aws_access_key_id} '
                f'--env AWS_SECRET_ACCESS_KEY={params.aws_secret_access_key} '
            )
            stderr = sys.stderr
            stdout = sys.stdout

        return self._run_docker(
            command,
            stderr=stderr,
            stdout=stdout,
        )
