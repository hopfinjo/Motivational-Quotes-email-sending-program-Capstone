from production.userInformation_handling import UserInformation
from production.chatGPT_quote_generator import chatGPT
from database_handling import Database_handling
from production.email_sending_SMTP import email_sending
import schedule
import time

class MotivationalQuotesProgram:
    """
    Driver to start the motivational quotes program email sending process.
    This will check the database for new users and changed preferred sending times twice a day.
    """

    def __init__(self):
        """Initiates all needed modules. Class has some helper functions (mainly for scheduler), but most of the functionality is
         implemented in main 3 modules: UserInformation, chatGPT and Database handling.
        
        """
        self.user_information = UserInformation()
        """Handles all functionality around a users information
        """
        self.chatGPT = chatGPT()
        """ Handles all functionality around generating quotes from chatGPT."""
        self.database_handling = Database_handling()
        """ Handles all functionality around database communication"""
        

    
    def make_new_Quote_and_send(self, user_email):
        """
        When scheduler triggers program to send new email, this will be executed to generate new email, update user info, and send new quote to user.
        This gets all the user info from the db, and updates it after
        """
        print("Sending and creating new quote is triggered")
        

        user_info_fromDB= self.database_handling.database_collection_object.find_one({'user_email': user_email})
        current_quote = user_info_fromDB["quote"]
        already_used_quotes = user_info_fromDB["already_used_quotes"]
        first_name = user_info_fromDB["first_name"]
        keywords = self.database_handling.get_user_keywords(user_email=user_email)

        # update user's profile
        already_used_quotes = self.user_information.add_current_quote_to_alreadyUsed(oldcurrent=current_quote, already_used_quotes=already_used_quotes)      

        # generate new Quoted
        newQuote = self.chatGPT.createNewQuote(oldquotes=already_used_quotes, keywords=keywords)
        
        # print("the new quote is: " + newQuote)
        # send new quote per email
        email_sending.send_email_SMTP(recipient_email_addr=user_email, subject= f"DAILY MOTIVATION BOOST for {first_name}", email_body=newQuote)
        
        # store new user info in DB.
        self.database_handling.update_user(user_email=user_email, new_quote=newQuote, new_already_sent_quotes=already_used_quotes)
        
        
    def send_email_helper(self, user_email):
        print("In send emailhelper")
        """
        Is needed to store the email address from each user in memory.

        Args:
            user_email (String): user_email
        """
        def send_email():
            self.make_new_Quote_and_send(user_email)
        return send_email
    

        
        
    def load_scheduler(self):
        """
        Loads the scheduler with each user's email address and the task to generate a new motivational quote for them
        """
        schedule.clear()
        all_users_entries = self.database_handling.database_collection_object.find()
            
        for user_json in all_users_entries:
                       
            user_email = user_json["user_email"]
            user_preferred_sending_time = user_json["user_preferred_emailTime"]
            schedule.every().day.at(user_preferred_sending_time).do(lambda: self.make_new_Quote_and_send(user_email))

            #CHANGEME: If wanted for debug and test purposes, program can be run with sending an email every 10 seconds.
            # simply comment line above, and uncomment line below.
            #schedule.every(10).seconds.do(self.send_email_helper(user_email))


    def main(self):
        """
        
        Backend code that sets scheduler and sends out emails.
        Not intended for costumer use. Updates scheduler twice a day.
        Stop code with ctrl + Z
        
        """
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("Current time:", current_time)
        print("If time set within docker container is wrong, please read InstructionsContainer.md file, and run container with specified time zone")
        self.database_handling.connect_to_db_table_and_get_collection()

        print("run me, and I will send emails to all users that are in the db, I check for new users twice a day")
        self.load_scheduler()

        print("Current time:", current_time)
        while True:            
            last_reload_time = time.time()            
            while True:
                current_time = time.time()
                if(current_time - last_reload_time >= 43200):
                    self.load_scheduler()
                    last_reload_time=time.time()
                schedule.run_pending()     
            

if __name__ == "__main__":
    program = MotivationalQuotesProgram()
    program.main()
