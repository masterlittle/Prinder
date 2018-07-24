from abc import ABCMeta, abstractmethod
import jinja2
import os

# sys.path.append(r'prinder/utilities.py')
# sys.path.append(r'prinder/logger.py')

from prinder.utilities import set_debug_level, time_delta, segregate_pr_by_repo
from prinder.logger import get_logger


class BaseNotifier:
    __metaclass__ = ABCMeta

    def __init__(self, template, debug):
        super(BaseNotifier, self).__init__()
        self.logger = get_logger(__name__)
        set_debug_level(self.logger, debug)
        self.template = template

    def get_jinja_template(self):
        template_file, template_path = self.__resolve_template_location()
        template_loader = jinja2.FileSystemLoader(searchpath=template_path)
        template_env = jinja2.Environment(loader=template_loader, trim_blocks=True, lstrip_blocks=True)
        template_env.globals['time_delta'] = time_delta
        return template_env.get_template(template_file)

    def __resolve_template_location(self):
        location = self.template.rsplit('/', 1)
        if len(location) == 1:

            template_path = os.path.join(os.path.dirname(__file__), 'templates')
            template_file = self.template
        else:
            template_path = location[0]
            template_file = location[1]
        return template_file, template_path

    @abstractmethod
    def notify(self, message, config):
        pass

    @abstractmethod
    def format(self, initial_message, pull_requests, owner):
        repos_pr = segregate_pr_by_repo(pull_requests)
        args = {
            "initial_message": initial_message,
            "repos_pr": repos_pr,
            "pull_requests": pull_requests,
            "owner": owner
        }
        return args
