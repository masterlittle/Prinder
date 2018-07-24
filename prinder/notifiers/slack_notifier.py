from base_notifier import BaseNotifier
from slacker import Slacker, Error


class SlackNotifier(BaseNotifier):

    def __init__(self, template, debug):
        super(SlackNotifier, self).__init__(template, debug)

    def notify(self, message, config):
        slack_token = config['slack_api_token']
        channels = config["notify_slack_channels"] or []
        members = config["notify_slack_members"] or []
        user = config["post_as_user"]

        super(SlackNotifier, self).notify(message, config)
        self.logger.debug(message)
        slack = Slacker(slack_token)
        try:
            self.post_to_slack(channels, message, slack, user, '#')
            self.post_to_slack(members, message, slack, user, '@')
        except Error as error:
            self.logger.error(str(error))

    def post_to_slack(self, notification_targets, message, slack, user, target_symbol):
        for target in notification_targets:
            self.logger.info("Sending notification to " + target)
            response = slack.chat.post_message(target_symbol + target,
                                               message,
                                               user,
                                               icon_emoji=':bell',
                                               icon_url=':bell')
            self.logger.debug(response)
            self.__log_notification_response(response, target)

    def format(self, initial_message, pull_requests, owner):
        self.logger.info("Formatting the text for slack as required")
        args = super(SlackNotifier, self).format(initial_message, pull_requests, owner)
        template = self.get_jinja_template()
        return template.render(args)  # this is where to put args to the template renderer

    def __log_notification_response(self, response, recipient):
        if response.successful:
            self.logger.info("Notification sent to " + recipient)
        else:
            self.logger.error(response.error)
