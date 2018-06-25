import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logger import get_logger
from slacker import Slacker
from slacker import Error

class Notifier:
    def __init__(self):
        self.logger = get_logger(__name__)

    def send_email(self,
                   subject,
                   body,
                   receivers,
                   sender,
                   host='localhost'):
        """
        Utility function to send mail
        :param subject: The subject of the e-mail
        :param body: The message to passed in the mail
        :param receivers: A list of email-ids
        :param sender: An email id of the sender
        :param host: Hostname where the SMTP server is setup. Default is 'localhost'
        """

        msg = MIMEMultipart('alternative')
        msg['From'] = sender
        msg['To'] = ','.join(receivers)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        try:
            smtpObj = smtplib.SMTP(host)
            smtpObj.sendmail(sender, receivers, msg.as_string())
            smtpObj.quit()
        except smtplib.SMTPException as error:
            self.logger.error("Unable to send email: {err}".format(err=error))

    def post_to_slack(self, slack_api_token, message, channel, individual_recipients=[], username='Prinder'):
        slack = Slacker(slack_api_token)
        try:
            for c in channel:
                self.logger.info("Sending notification to " + c)
                response = slack.chat.post_message('#' + c,
                                                   message,
                                                   username,
                                                   icon_emoji=':bell',
                                                   icon_url=':bell')
                self.logger.debug(response)
                self.__log_notification_response(response, c)
            for recipient in individual_recipients:
                self.logger.info("Sending notification to " + recipient)
                response = slack.chat.post_message('@' + recipient,
                                                   message,
                                                   username,
                                                   icon_emoji=':bell:',
                                                   icon_url=':bell:')
                self.logger.debug(response)
                self.__log_notification_response(response, recipient)
        except Error as error:
            self.logger.error(str(error))

    def __log_notification_response(self, response, recipient):
        if response.successful:
            self.logger.info("Notification sent to " + recipient)
        else:
            self.logger.error(response.error)

