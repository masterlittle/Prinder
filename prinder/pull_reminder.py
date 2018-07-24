from collections import OrderedDict
from logger import get_logger
from github3 import login
from utils import set_debug_level

logger = get_logger(__name__)


class PullReminder:
    def __init__(self, configuration, debug=False):
        set_debug_level(logger, debug)
        self.config = configuration

    @staticmethod
    def fetch_repository_pulls(repository):
        logger.debug(repository.name)
        return [pull for pull in repository.pull_requests()
                if pull.state == 'open']

    def fetch_organization_pulls(self):
        """
        Returns a formatted string list of open pull request messages.
        """
        organization_name = self.config["github"]["organization_name"]
        list_of_repos = self.config["github"]["list_of_repos"]
        topics = self.config["github"]["topics"]
        all_repos = self.config["github"]["all_repos"]
        ignore_repos = self.config["github"]["ignore_repos"]
        ignore_labels = self.config["github"]["ignore_labels"]

        client = login(token=self.config["github_api_token"])
        organization = client.organization(organization_name)
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
        return self.filter_labels(pulls, ignore_labels)

    @staticmethod
    def filter_labels(pulls, ignore_labels):

        def has_labels(pull):
            if not pull.labels:
                return True
            else:
                for label in pull.labels:
                    if label['name'] in ignore_labels:
                        return False
                return True

        logger.info("Filtering pull requests based on labels")
        if not ignore_labels:
            return pulls
        else:
            final_list_of_pulls = filter(lambda x: has_labels(x), pulls)
            logger.info("Final filtered pull count is " + str(len(final_list_of_pulls)))
            return final_list_of_pulls

    @staticmethod
    def filter_repos(repos, ignore_repos):
        """
        Filter list of repositories acc. to the list passed
        :param repos: list of repos to check pull request for
        :param ignore_repos: list of repos to ignore
        :return: filtered list of repos
        """
        logger.info("Filtering list of repositories")
        if not ignore_repos:
            return repos
        else:
            final_list_of_repos = filter(lambda x: x.name not in ignore_repos, repos)
            logger.info("Final filtered repository count is " + str(len(final_list_of_repos)))
            return final_list_of_repos
