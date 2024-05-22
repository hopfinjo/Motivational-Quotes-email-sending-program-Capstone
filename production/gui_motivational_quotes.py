from production.userInformation_handling import UserInformation
from production.chatGPT_quote_generator import chatGPT
from database_handling import Database_handling
import tkinter as tk
from tkinter import messagebox
import re

class DailyMotivationAppGUI:
    """
    Tkinter GUI that enables user to sign up, login, delete their accounts, add new set of keywords and logout.

    """
    def __init__(self, root):
        """
        Creates objects that handle functionality.
        """
        
        self.user_information = UserInformation()
        """Handles all functionality around a users information
        """
        self.chatGPT = chatGPT()
        """ Handles all functionality around generating quotes from chatGPT.
        """
        self.database_handling = Database_handling()
        """ Handles all functionality around database communication
        """

        self.database_handling.connect_to_db_table_and_get_collection()

        self.root = root
        self.root.title("Welcome to DailyMotivation")
        self.root.geometry('600x350')

        self.create_login_label()

    def create_login_label(self):
        """
        Creates user login window.
        """
        self.email_input_label = tk.Label(self.root, text="Enter your email:")
        self.email_input_label.pack()

        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()

        self.login_button = tk.Button(self.root, text="Log In", command=self.log_in_user)
        self.login_button.pack()



    def create_all_fields(self):
        """
        Creates window once user is logged in.
        """

        keywords = self.database_handling.get_user_keywords(self.user_information.user_email)
        
        if keywords:
            keyword_list = keywords.split()
            print("Len of keyword: ", len(keywords))
            print(keyword_list)
            self.keywords_text = tk.Text(self.root, height=len(keyword_list), width=40)
            
            label_current_keywords = tk.Label(self.root, text="Your current keywords are:")
            label_current_keywords.pack()

            self.keywords_text.pack(padx=10, pady=10)
            for keyword in keyword_list:
                self.keywords_text.insert(tk.END, f"{keyword}\n")
        else:
            self.keywords_text = tk.Text(self.root, height=1, width=40)
            self.keywords_text.pack(padx=10, pady=10)
            self.keywords_text.insert(tk.END, "There are no keywords added yet\n")


        user_preferred_emailTime = self.database_handling.get_users_prefered_emailTime(self.user_information.user_email)
        print("The users preffered email time is: ", user_preferred_emailTime)
        label_user_preffered_emailTime_display = tk.Label(self.root, text="The current time you get your emails is:")
        label_user_preffered_emailTime_display.pack()
        self.user_preffered_emailTime_display = tk.Text(self.root, height = 1, width=5)
        self.user_preffered_emailTime_display.insert(tk.END, user_preferred_emailTime)

        self.user_preffered_emailTime_display.pack()

        # Entry for space-separated keywords
        self.keywords_input_label = tk.Label(self.root, text="Enter space-separated keywords:")
        self.keywords_input_label.pack()

        self.keywords_entry = tk.Entry(self.root)
        self.keywords_entry.pack()

        self.keywords_entry_button = tk.Button(self.root, text="Change-KeyWords", command=lambda: self.update_keywords(self.user_information.user_email, self.keywords_entry.get()))
        self.keywords_entry_button.pack()

        self.time_input_label = tk.Label(self.root, text="Enter time in 24-hour format:")
        self.time_input_label.pack()

        self.time_entry = tk.Entry(self.root)
        self.time_entry.pack()

        self.time_entry_button = tk.Button(self.root, text="Change-Time", command=lambda: self.set_custom_time(self.time_entry.get()))
        self.time_entry_button.pack()

        self.unsubscribe_button = tk.Button(self.root, text="Unsubscribe", fg="red",command=self.unsubscribe)
        self.unsubscribe_button.pack()

        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout_and_restart_window)
        self.logout_button.pack(side=tk.BOTTOM)

    def logout_and_restart_window(self):
        """
        Resets window to start.
        """
        print("Restarting your window")

        # from https://stackoverflow.com/questions/15781802/python-tkinter-clearing-a-frame
        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_login_label()


    def update_keywords(self, user_email, new_keywords):
        """
        Updates preferred keywords for user.
        """
        self.database_handling.update_keywords(user_email, new_keywords)
        print("You successfully set new keywords")
        messagebox.showinfo(message="You have successfully updated your keywords")
        # make all fields new:
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_all_fields()


    def set_custom_time(self, preffered_email_time):
        """
        Updates custom time from user in database.
        """
        regex_pattern = r"^[0-9][0-9]:[0-9][0-9]$"
        if not re.match(regex_pattern, preffered_email_time):
            messagebox.showinfo(message="You entered an invalid time. Enter time in 24:00 format with no spaces and : ")
            return
        self.database_handling.update_users_prefered_emailTime(self.user_information.user_email, preffered_email_time)
        messagebox.showinfo(message="You have successfully updated your preffered sending time")
                # make all fields new:
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_all_fields()

    def unsubscribe(self):
        """ 
        Deletes user information from database.
        """
        print("unsubscribe button is pressed")
        self.database_handling.delete_user_from_database(self.user_information.user_email)
        messagebox.showinfo("We are sorry to see you go")
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.title("Welcome to DailyMotivation")
        self.root.geometry('550x300')

        self.create_login_label()

    def log_in_user(self):
        """ Get user email address. 
        Also validates email address and does not allow invalid email addresses to continue in this application.
        """
        email = self.email_entry.get()
        isValidEmail = self.user_information.check_email(email)

        if isValidEmail:

            # set field so that other functions can access it
            self.user_information.user_email=email

            isExistingUser = self.user_information.check_if_isexisting_user(self.database_handling.database_collection_object)
            self.email_entry.destroy()
            self.email_input_label.destroy()
            self.login_button.destroy()

            if(isExistingUser):
                # get user first name from db and set it to memory
                self.user_information.user_first_name =self.database_handling.get_user_name(email)
                
                welcome_back_label = tk.Label(self.root, text=f"Welcome back {self.user_information.user_first_name}")
                welcome_back_label.pack()
                self.create_all_fields()

            else:
                print("Not an existing user")                            

                # Create an Entry widget for username input
                self.username_input_label = tk.Label(self.root, text="Enter your username:")
                self.username_input_label.pack()

                self.username_entry = tk.Entry(self.root)
                self.username_entry.pack()

                print("Self.username_entry", self.username_entry)

                self.username_entry_button = tk.Button(self.root, text="Enter", command=lambda: self.create_user_inDB(self.username_entry.get()))
                self.username_entry_button.pack()


        else:
            print("Try again")
            messagebox.showerror("Error", "Please enter a valid email address.")

    def create_user_inDB(self, username_entry):
                # must get username from user
                self.user_information.user_first_name = username_entry
            
                first_quote = self.chatGPT.createQuoteFirstTime()
                
                print("Your daily dose of motivation will be send to you at 5pm every afternoon on default. You can change this later")                
                user_preferred_sending_time = "17:00"
            
                # stores user info + 1 generated quote ready to be send to user.
                user_data = self.database_handling.create_data_object_for_DB(
                    user_first_name=self.user_information.user_first_name, user_email=self.user_information.user_email,
                    user_pw="1234", user_current_quote=first_quote, user_already_sent_quotes=[],
                    user_preferred_emailTime=user_preferred_sending_time, keywords=[])
                
                self.database_handling.store_new_user_in_DB(user_data=user_data)

                # call page to input keywords and custom time
                self.login_button.pack_forget()
                welcome_back_label = tk.Label(self.root, text=f"Welcome {username_entry} to this amazing program")
                welcome_back_label.pack()

                self.username_entry.destroy()
                self.username_input_label.destroy()
                self.username_entry_button.destroy()
                self.create_all_fields()
        

def main():    
    root = tk.Tk()
    app = DailyMotivationAppGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()