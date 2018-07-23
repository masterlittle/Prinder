import os
from notifiers.mail_notifier import MailNotifier
from notifiers.slack_notifier import SlackNotifier
import yaml
from logger import get_logger
import click
from pull_reminder import PullReminder
from utils import set_debug_level

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
@click.option('--debug', help='Turn detailed logging on and off', is_flag=True)
def run(config_file, debug):
    config = read_config(config_file)
    get_github_token(config)
    set_debug_level(debug)
    logger.debug("Configuration is: " + str(config))

    pull_reminder = PullReminder(config, debug)

    pulls = pull_reminder.fetch_organization_pulls()

    if pulls:
        logger.info("Sending notifications")
        post_notifications(config, pulls, debug)


def get_github_token(config):
    try:
        if config["github_api_token"] is None:
            config["github_api_token"] = os.environ['PRINDER_GITHUB_API_TOKEN']
    except KeyError as error:
        raise Exception('Please set the environment variable. {0}'.format(error))

def get_slack_token(config):
    try:
        if config["slack_api_token"] is None:
            config["slack_api_token"] = os.environ['PRINDER_SLACK_API_TOKEN']
    except KeyError as error:
        print('Please set the environment variable. {0}'.format(error))
        logger.error('Please set the environment variable. {0}'.format(error))


def post_notifications(config, pulls, debug):
    if config["notification"]["slack"]["enable"]:
        get_slack_token(config)
        if config["slack_api_token"] is None:
            logger.error("Slack notification not sent because slack token was not found.")
            return

        template_location = config["notification"]["slack"]["template_location"]
        if template_location is None:
            template_location = 'slack_template.template'
        notifier = SlackNotifier(template_location, debug)

        text = notifier.format(config["initial_message"], pulls, config["github"]["organization_name"])
        logger.info("Sending message to slack")
        notifier.notify(text, config["notification"]["slack"])

    if config["notification"]["mail"]["enable"]:
        template_location = config["notification"]["mail"]["template_location"]
        if template_location is None:
            template_location = 'mail_template.html'
        notifier = MailNotifier(template_location, debug)

        text = notifier.format(config["initial_message"], pulls, config["github"]["organization_name"])
        logger.info("Sending mail")
        notifier.notify(text, config["notification"]["mail"])


def read_config(config_file_path):
    with open(config_file_path, 'r') as stream:
        try:
            logger.info("Configuration read successfully")
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise Exception("Invalid file. " + str(exc))


if __name__ == '__main__':
    cli()
