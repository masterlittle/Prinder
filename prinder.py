import sys

from notifiers import Notifier
import os
import yaml
from logger import get_logger
import click
from pull_reminder import PullReminder

INITIAL_MESSAGE = """\
Hi! There's a few open pull requests you should take a \
look at:

"""

logger = get_logger(__name__)

@click.group()
def cli():
    pass


@cli.command()
@click.option('--config_file_path', help='Path of config file. eg - /opt/prinder/', default='')
def run(config_file_path):
    config = read_config(config_file_path)

    logger.debug("Configuration is: " + str(config))

    get_api_tokens(config)

    pull_reminder = PullReminder(config)

    lines = pull_reminder.fetch_organization_pulls()

    if lines:
        text = INITIAL_MESSAGE + '\n'.join(lines)
        logger.info("Sending notifications")
        post_notifications(config, text)


def get_api_tokens(config):
    try:
        if not config["slack_api_token"]:
            config["slack_api_token"] = os.environ.get('PRINDER_SLACK_API_TOKEN')
        if not config["github_api_token"]:
            config["github_api_token"] = os.environ.get('PRINDER_GITHUB_API_TOKEN')
    except KeyError as error:
        logger.error('Please set the environment variable {0}'.format(error))
        sys.exit(1)


def post_notifications(config, text):
    notifier = Notifier()

    if config["notification"]["slack"]["enable"]:
        notifier.post_to_slack(config["slack_api_token"],
                               text,
                               config["notification"]["slack"]["notify_slack_channels"],
                               config["notification"]["slack"]["notify_slack_members"],
                               config["notification"]["slack"]["post_as_user"])

    if config["notification"]["mail"]["enable"]:
        notifier.send_email("",
                            text,
                            config["notification"]["mail"]["mail_to"],
                            config["notification"]["mail"]["sender"],
                            config["notification"]["mail"]["host"])


def read_config(config_file_path):
    config_file_name = 'prinder_config.yaml'
    if not config_file_path:
        path = config_file_name
    else:
        path = config_file_path + config_file_name
    with open(path, 'r') as stream:
        try:
            logger.info("Configuration read successfully")
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise Exception("Invalid file. " + str(exc))


if __name__ == '__main__':
    cli()
