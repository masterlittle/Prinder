import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logger import get_logger
from slacker import Slacker
from slacker import Error

logger = get_logger(__name__)


class Notifier:
    def __init__(self):
        pass

    @staticmethod
    def format_pull_requests_for_slack(initial_message, pull_requests, owner):
        lines = []

        logger.info("Formatting the text for slack as required")
        for pull in pull_requests:
            creator = pull.user.login
            line = initial_message + ' \n*[{0}/{1}] * Pull request open by *{2}* \n <{3} | #{4} {5}>\n'.format(
                owner.encode('utf-8'),
                pull.repository.name.encode('utf-8'),
                creator.encode('utf-8'),
                pull.html_url.encode('utf-8'),
                pull.number,
                pull.title.encode('utf-8'))
            lines.append(line)

        return lines

    @staticmethod
    def format_pull_requests_for_mail(initial_message, pull_requests, owner):
        lines = []

        logger.info("Formatting the text for mail as required")
        message = """<html>
                    <head></head>
                    <body>
                    <p>{0}</p>
                    <table>
                    """.format(initial_message)
        for pull in pull_requests:
            creator = pull.user.login
            message += """<tr>"""
            line = '<td>' \
                   '<b>{0}/{1}]</b>' \
                   '</td> ' \
                   '<td>' \
                   'Opened by <b>{2}</b></td>'\
                .format(
                owner.encode('utf-8'),
                pull.repository.name.encode('utf-8'),
                creator.encode('utf-8'))
            message += line

            message += """<td>
            <a href= {0}> # {1} {2} </a>
            </td>""".format(pull.html_url.encode('utf-8'),
                                                                 pull.number,
                                                                 pull.title.encode('utf-8'))
            message += """</tr>"""
            lines.append(line)
        message += """</body></html>"""

        return message

    @staticmethod
    def send_email(subject,
                   body,
                   receivers,
                   sender,
                   host='localhost',
                   port=25):
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
            smtpObj = smtplib.SMTP(host, port)
            smtpObj.sendmail(sender, receivers, msg.as_string())
            smtpObj.quit()
            logger.info("Mail sent successfully.")
        except smtplib.SMTPException as error:
            logger.error("Unable to send email: {err}".format(err=error))

    def post_to_slack(self, slack_api_token, message, channel, individual_recipients=[], username='Prinder'):
        slack = Slacker(slack_api_token)
        try:
            for c in channel:
                logger.info("Sending notification to " + c)
                response = slack.chat.post_message('#' + c,
                                                   message,
                                                   username,
                                                   icon_emoji=':bell',
                                                   icon_url=':bell')
                logger.debug(response)
                self.__log_notification_response(response, c)
            for recipient in individual_recipients:
                logger.info("Sending notification to " + recipient)
                response = slack.chat.post_message('@' + recipient,
                                                   message,
                                                   username,
                                                   icon_emoji=':bell:',
                                                   icon_url=':bell:')
                logger.debug(response)
                self.__log_notification_response(response, recipient)
        except Error as error:
            logger.error(str(error))

    def __log_notification_response(self, response, recipient):
        if response.successful:
            logger.info("Notification sent to " + recipient)
        else:
            logger.error(response.error)
