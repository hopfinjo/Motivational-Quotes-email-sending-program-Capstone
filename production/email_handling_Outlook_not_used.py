# This is not used in the project. If wanted, this can be used instead of SMTP.
# this will triger an email to be sent from the local outlook.
# this will only work on windows. If run in container, windows container must be used.

import win32com.client

class email_sending:
    """
    This module handles email triggering from locally installed outlook on machine.
    IMPORTANT: If you do not want to use personal email as a sender for program, 
    you MUST log out of your Outlook Account and log into test-account.
    Credentials are provided in dev-Docs/instructions
    """
    @staticmethod
    def send_email_wOutlook(recipient_email_addr, subject, email_body):
        """
        Triggers email to be send from Outlook

        Args:
            recipient_email_addr (String): email addr for recipient
            subject (String): Generic Subject line
            email_body (Sring): The quote to be send
        """
                
        outlook = win32com.client.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = recipient_email_addr
        mail.Subject =subject
        mail.Body = email_body
        mail.Send()



# code copied from: 
# https://www.codeforests.com/2020/06/05/how-to-send-email-from-outlook/