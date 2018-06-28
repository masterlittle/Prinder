from collections import OrderedDict
from logger import get_logger
from github3 import login

logger = get_logger(__name__)

class PullReminder:
    def __init__(self, configuration):
        self.config = configuration

    @staticmethod
    def fetch_repository_pulls(repository):
        return [pull for pull in repository.pull_requests()
                if pull.state == 'open']

    @staticmethod
    def format_pull_requests(pull_requests, owner):
        lines = []

        logger.info("Formatting the text as required")
        for pull in pull_requests:
            creator = pull.user.login
            line = '\n*[{0}/{1}] * Pull request open by *{2}* \n <{3} | #{4} {5}>\n'.format(
                owner.encode('utf-8'),
                pull.repository.name.encode('utf-8'),
                creator.encode('utf-8'),
                pull.html_url.encode('utf-8'),
                pull.number,
                pull.title.encode('utf-8'))
            lines.append(line)

        return lines

    def fetch_organization_pulls(self):
        """
        Returns a formatted string list of open pull request messages.
        """
        organization_name = self.config["github"]["organization_name"]
        list_of_repos = self.config["github"]["list_of_repos"]
        topics = self.config["github"]["topics"]
        all_repos = self.config["github"]["all_repos"]
        ignore_repos = self.config["github"]["ignore_repos"]

        client = login(token=self.config["github_api_token"])
        organization = client.organization(organization_name)
        lines = []
        pulls = []

        if all_repos:
            logger.info("Fetching pull requests for organization")
            for repository in self.filter_repos(organization.repositories(), ignore_repos):
                pulls = pulls + self.fetch_repository_pulls(repository)
        else:
            if topics:
                query = '+'.join(["topic:" + topic for topic in topics]) + " user:" + organization_name
                logger.info("Fetching pull requests for topics: " + str(topics))
                for repository in self.filter_repos([repo.repository for repo in client.search_repositories(query)],
                                                    ignore_repos):
                    pulls = pulls + self.fetch_repository_pulls(repository)

            if list_of_repos:
                logger.info("Fetching pull requests from list of repositories: " + str(list_of_repos))
                for repository_name in self.filter_repos(list_of_repos, ignore_repos):
                    repository = client.repository(owner=organization_name, repository=repository_name)
                    pulls = pulls + self.fetch_repository_pulls(repository)

        pulls = list(OrderedDict.fromkeys(pulls))
        lines += self.format_pull_requests(pulls, organization_name)

        return lines

    @staticmethod
    def filter_repos(repos, ignore_repos):
        logger.info("Filtering list of repositories")
        final_list_of_repos = filter(lambda x: x.name not in ignore_repos, repos)
        logger.info("Final filtered repository count is " + str(len(final_list_of_repos)))
        return final_list_of_repos