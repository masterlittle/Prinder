import ast
import os
import sys
import click
import yaml
import os

import requests
from github3 import login
from collections import OrderedDict


@click.group()
def cli():
    pass


POST_URL = 'https://slack.com/api/chat.postMessage'

ignore = os.environ.get('IGNORE_WORDS')
IGNORE_WORDS = ignore.split(',') if ignore else []
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL', '#general')

try:
    SLACK_API_TOKEN = 'xoxp-2526871921-12554213046-76262475735-1269aad9eb'
    GITHUB_API_TOKEN = '52729dad542961d741631cd4dcf5aebec95cb4fe'
    ORGANIZATION = 'grofers'
except KeyError as error:
    sys.stderr.write('Please set the environment variable {0}'.format(error))
    sys.exit(1)

INITIAL_MESSAGE = """\
Hi! There's a few open pull requests you should take a \
look at:

"""


def fetch_repository_pulls(repository):
    return [pull for pull in repository.pull_requests()
            if pull.state == 'open']


def is_valid_title(title):
    lowercase_title = title.lower()
    for ignored_word in IGNORE_WORDS:
        if ignored_word.lower() in lowercase_title:
            return False

    return True


def format_pull_requests(pull_requests, owner):
    print(pull_requests)
    print(owner)
    lines = []

    for pull in pull_requests:
        if is_valid_title(pull.title):
            creator = pull.user.login
            line = '*[{0}/{1}]* <{2} : {3} - by {4}>'.format(
                owner.encode('utf-8'), pull.repository.name.encode('utf-8'), pull.html_url.encode('utf-8'),
                pull.title.encode('utf-8'), creator.encode('utf-8'))
            lines.append(line)

    return lines


def fetch_organization_pulls(organization_name, list_of_repos, tags):
    """
    Returns a formatted string list of open pull request messages.
    """
    client = login(token=GITHUB_API_TOKEN)
    organization = client.organization(organization_name)
    lines = []
    pulls = []

    if tags:
        query = '+'.join(["topic:" + tag for tag in tags]) + " user:" + organization_name
        print(query)
        for repositories in [repo for repo in client.search_repositories(query)]:
            pulls = pulls + fetch_repository_pulls(repositories.repository)

    if list_of_repos:
        for repository_name in list_of_repos:
            repository = client.repository(owner=organization_name, repository=repository_name)
            pulls = pulls + fetch_repository_pulls(repository)

    pulls = list(OrderedDict.fromkeys(pulls))
    lines += format_pull_requests(pulls, organization_name)

    # for repository in organization.repositories():
    #     unchecked_pulls = fetch_repository_pulls(repository)
    #     lines += format_pull_requests(unchecked_pulls, organization_name, repository.name)

    return lines


def get_topics(organization_name, repository_name):
    pass
    # URL = 'https://api.github.com/search/repositories'
    # response = requests.get(URL, params={'access_token': GITHUB_API_TOKEN, 'q': 'topic:dse'},
    #                         headers={'Accept': 'application/vnd.github.mercy-preview+json'})
    # answer = response.json()
    # print(answer["name"])


def send_to_slack(text):
    payload = {
        'token': SLACK_API_TOKEN,
        'channel': 'testslack',
        'username': 'Pull Request Reminder',
        'icon_emoji': ':bell:',
        'text': text
    }

    response = requests.post(POST_URL, data=payload)
    answer = response.json()
    if not answer['ok']:
        raise Exception(answer['error'])


def run():
    config = read_config()
    if not config["config"]["authentication"]["slack_api_token"]:
        config["config"]["authentication"]["slack_api_token"] = os.environ['PRINDER_SLACK_API_TOKEN']
    if not config["config"]["authentication"]["github_api_token"]:
        config["config"]["authentication"]["github_api_token"] = os.environ['PRINDER_GITHUB_API_TOKEN']
        # lines = fetch_organization_pulls(ORGANIZATION, list_of_repos, topics)
        # if lines:
        #     text = INITIAL_MESSAGE + '\n'.join(lines)
        #     print(text)
        #     send_to_slack(text)


def read_config():
    with open("prinder_config.yaml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == '__main__':
    run()
