import smtplib
from email.message import EmailMessage


class email_sending:

    @staticmethod
    def send_email_SMTP(recipient_email_addr, subject, email_body):
        # CHANGEME: Set up your own dummy email address. Yahoo is prefereed, since it allows in app
        # password! Normal access password does not work.
        email_address = 'DailyMotivationDummy@yahoo.com'
        password = 'pvepcynwajypnuyr'
        subject = 'Your Daily Dose of Motivation is HERE!'

        try:
            message = EmailMessage()
            message['From'] = email_address
            message['To'] = recipient_email_addr
            message['Subject'] = subject
            message.set_content(email_body)
            conn = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
            conn.login(email_address, password)
            conn.sendmail(email_address, recipient_email_addr, message.as_string())
            conn.quit()
            print("Email sent successfully!")
        except Exception as e:
            print("Error:", e)


        # libraries used:
        # https://docs.python.org/3/library/email.examples.html
        # https://python.plainenglish.io/how-to-send-email-with-python-705cce2bce38



# Main can be used to check functionality of email sending
# def main():
#     recipient_email_addr = 'testrecipient@test.st'
#     subject = 'Your Daily Dose of Motivation is HERE!'
#     email_body = 'Dear Test,\nThis is a test message.\n\nIf you want to change your quotes and time you receive your quotes, please open GUI and change it'
#     email_sending.send_email_wOutlook(recipient_email_addr, subject, email_body)

# if __name__ == "__main__":
#     main()