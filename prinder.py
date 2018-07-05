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
@click.option('--config_file', help='Path of config file. eg - /opt/prinder/prinder_config.yaml', default='prinder_config.yaml')
def run(config_file):
    config = read_config(config_file)

    logger.debug("Configuration is: " + str(config))

    get_github_token(config)

    pull_reminder = PullReminder(config)

    pulls = pull_reminder.fetch_organization_pulls()

    if pulls:
        logger.info("Sending notifications")
        post_notifications(config, pulls)


def get_github_token(config):
    try:
        if config["github_api_token"] is None:
            config["github_api_token"] = os.environ['PRINDER_GITHUB_API_TOKEN']
        print(config)
    except KeyError as error:
        logger.error('Please set the environment variable {0}'.format(error))
        sys.exit(1)

def get_slack_token(config):
    try:
        if not config["slack_api_token"]:
            config["slack_api_token"] = os.environ['PRINDER_SLACK_API_TOKEN']
    except KeyError as error:
        logger.error('Please set the environment variable {0}'.format(error))
        sys.exit(1)


def post_notifications(config, pulls):
    notifier = Notifier()

    if config["notification"]["slack"]["enable"]:
        get_slack_token(config)
        text = notifier.format_pull_requests_for_slack(config["initial_message"], pulls, config["github"]["organization_name"])
        logger.info("Sending message to slack")
        notifier.post_to_slack(config["slack_api_token"],
                               text,
                               config["notification"]["slack"]["notify_slack_channels"],
                               config["notification"]["slack"]["notify_slack_members"],
                               config["notification"]["slack"]["post_as_user"])

    if config["notification"]["mail"]["enable"]:
        text = notifier.format_pull_requests_for_mail(config["initial_message"], pulls, config["github"]["organization_name"])
        logger.info("Sending mail")
        notifier.send_email(config["notification"]["mail"]["subject"],
                            text,
                            config["notification"]["mail"]["mail_to"],
                            config["notification"]["mail"]["sender"],
                            config["notification"]["mail"]["host"],
                            config["notification"]["mail"]["port"])


def read_config(config_file_path):
    with open(config_file_path, 'r') as stream:
        try:
            logger.info("Configuration read successfully")
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise Exception("Invalid file. " + str(exc))


if __name__ == '__main__':
    cli()
