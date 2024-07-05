import argparse
import subprocess
from pathlib import Path
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

        return parser.parse_args()

    def _run_docker(
        self,
        command: str,
        output_logs_file: Path,
        output_errors_file: Path,
    ) -> 'CompletedProcess':
        """Run docker with parameters."""

        result: 'CompletedProcess' = subprocess.run(
            args=[command],
            shell=True,
            stderr=open(output_errors_file, 'a', encoding='utf-8'),
            stdout=open(output_logs_file, 'a', encoding='utf-8'),
        )

        return result

    def run(self):
        params: argparse.Namespace = self._parse_arguments()

        logger.info(f'Running docker with parameters: {params}')

        output_logs_file = LOGS_DIR / 'docker.logs'
        output_errors_file = LOGS_DIR / 'docker_errors.logs'

        command: str = (
            f'docker run {params.docker_image} {params.bash_command}'
        )

        return self._run_docker(command, output_logs_file, output_errors_file)
