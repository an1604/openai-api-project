import smtplib
from email.mime.text import MIMEText


class Mail(object):
    def __init__(self, from_addr, to_addr):
        self.from_addr = from_addr
        self.to_addr = to_addr

    def prepare_message(self, subject, message):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.from_addr
        msg['To'] = self.to_addr

        if self.confirm_mail(message):
            self.send_mail(message)
            print('Message successfully sent!')
        else:
            print('Cannot send the message!')

    def send_mail(self, message):
        if self.confirm_mail(message):
            s = smtplib.SMTP('localhost')
            s.send_message(message)
            s.quit()
            return True
        return False

    def confirm_mail(self, message):
        print('The message is: {}'.format(message))
        agree = input('Do you want to accept the message? (Y for yes, N for no): )')
        return agree.lower() == 'y'
