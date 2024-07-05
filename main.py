from src.config import logger
from src.runner import DockerRunner


def main():
    try:
        DockerRunner().run()
    except KeyboardInterrupt:
        pass
    logger.info('Exit')


if __name__ == '__main__':
    main()
