from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from base_notifier import BaseNotifier


class MailNotifier(BaseNotifier):

    def __init__(self, template, debug):
        super(MailNotifier, self).__init__(template, debug)

    def notify(self, message, **kwargs):

        receivers = kwargs["mail_to"]
        sender = kwargs["sender"]
        host = kwargs["host"]
        port = kwargs["port"]
        subject = kwargs["subject"]

        msg = MIMEMultipart('alternative')
        msg['From'] = sender
        msg['To'] = ','.join(receivers)
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'html'))

        try:
            smtpObj = smtplib.SMTP(host, port)
            smtpObj.sendmail(sender, receivers, msg.as_string())
            smtpObj.quit()
            self.logger.info("Mail sent successfully.")
        except smtplib.SMTPException as error:
            self.logger.error("Unable to send email: {err}".format(err=error))

    def format(self, initial_message, pull_requests, owner):
        args = super(MailNotifier, self).format(initial_message, pull_requests, owner)
        self.logger.info("Formatting the text for mail as required")

        template = self.get_jinja_template()
        return template.render(args)  # this is where to put args to the template renderer
