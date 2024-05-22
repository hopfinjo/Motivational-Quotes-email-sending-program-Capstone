import pymongo


class Database_handling:
    """
    Handles all commnunication with locally running MongoDB database. 
    Default MongoDB port is used and can be accessed by: localhost:27017
    Functions are create DB, insert users, update users.
    """
    def __init__(self):
        """
        Initializes Database_handling object.
        This does not create a connection to the database. It solely intitialized the object
         and sets the databse_collection_object to None.
        """
        # use this to access database
        self.database_collection_object = None
        """Object used to communicate with DB. This is the table, where all information is stored from users.
        """

    def connect_to_db_table_and_get_collection(self):
        """Connects to MongoDB table.

        Returns:
            MongoDB_collection_(table): If the table does not exist, it will be created when inserting first element.

        Raises:
            ConnectionFailure in case it cannot connect to db.
        """
        try:
            maxServSelDelay = 2
            myclient = pymongo.MongoClient(

                # CHANGEME. 172.20.16.1 must be changed to local ethernet IP address. localhost does not suffice
                "mongodb://172.20.16.1:27017", serverSelectionTimeoutMS=maxServSelDelay)

            # to check if connection is working and trigger exception if needed
            myclient.server_info()
            mydb = myclient["QuotesDB"]
            user_information_collection = mydb["user_information_table"]
            self.database_collection_object = user_information_collection
            return user_information_collection

        except pymongo.errors.ConnectionFailure as e:
            print(e)
            print("There was an error in connecting to a local database! Please check if db is up and running and URl is correct.")
            print("Please restart the program and try again.")
            exit()

        # following Stackoverflow blog was used to check if connection to db is working:
        # https://stackoverflow.com/questions/30539183/how-do-you-check-if-the-client-for-a-mongodb-instance-is-valid

    def store_new_user_in_DB(self, user_data):
        """
        Stores user registration information into database.
        If database table did not exist before, at inserting 1 element it will be created.
        """
        # store information in database
        self.database_collection_object.insert_one(user_data)
        print("You are now succesfully registered/stored in db")

    @staticmethod
    def create_data_object_for_DB(user_first_name, user_email, user_pw, user_current_quote, user_already_sent_quotes, user_preferred_emailTime, keywords):
        """Creates data object to be inserted into database. Does not insert the object.

        Args:
            user_first_name (String): name
            user_email (String): email_address 
            user_pw (String): dummy password. always "1234"
            user_current_quote (String): Quote
            user_already_sent_quotes (List[String]): 15 lastly used quotes

        Returns:
            JSON Object: Ready to be inserted into DB
        """
        user_data = {
            "first_name": user_first_name,
            "user_email": user_email,
            "user_pw": user_pw,  # The password is a placeholder for now.
            "quote": user_current_quote,
            "user_preferred_emailTime" : user_preferred_emailTime,
            # to avoid re-sending quotes. store last 30
            "already_used_quotes": user_already_sent_quotes,
            "keywords": keywords
        }
        return user_data
    
    def update_user(self, user_email, new_quote, new_already_sent_quotes):
        """Updates a users data. Used when new quote is generated.

        Args:
            user_email (String): email addr = username 
            new_quote (String): Quote
            new_already_sent_quotes (List[String]): 15 lastly used quotes
        """
        search_query = {"user_email": user_email}
        new_values = {"$set": {
            "quote": new_quote,
            "already_used_quotes": new_already_sent_quotes
        }}
        self.database_collection_object.update_one(search_query, new_values)
        #print("Users already sent quotes updated successfully!")
        
    def update_users_prefered_emailTime(self, user_email, preffered_email_time):
        """
        Updates time that user gets email each day.

        Args:
            user_email (String): user email address.
            preffered_email_time (Time - String): preffered email time.
        """
        search_query = {"user_email": user_email}
        new_values = {"$set": {
            "user_preferred_emailTime": preffered_email_time
        }}
        self.database_collection_object.update_one(search_query, new_values)
        #print("users preffered email time is updated")
        
    def delete_user_from_database(self, user_email):
        """
        Delets a user from the database.

        Args:
            user_email (String): user email address.
        Returns:
            _type_: _description_
        """
        search_query = {"user_email": user_email}
        return self.database_collection_object.delete_one(search_query)
    

        
        
    def update_keywords(self,user_email, new_key_words):
        """
        Updates a users keywords, which are used to generate personalized quotes.

        Args:
            user_email (String): _description_
            new_key_words (List[str]): _description_
        """
        
        search_query = {"user_email": user_email}
        new_values = {"$set": {
            "keywords": new_key_words
        }}
        self.database_collection_object.update_one(search_query, new_values)
        print("Succesfully updated keywords")


    def get_user_name(self, user_email):
        """
        Gets a user name given a user email.

        Args:
            user_email (String): user email

        Returns:
            String: first name of user
        """
        search_query = {"user_email": user_email}
        user_object = self.database_collection_object.find_one(search_query)
        return user_object["first_name"]
    
    
    def get_user_keywords(self, user_email):
        search_query = {"user_email": user_email}
        user_object = self.database_collection_object.find_one(search_query)
        current_keywords = user_object["keywords"]
        return current_keywords


    def get_users_prefered_emailTime(self, user_email):
        
        search_query = {"user_email": user_email}
        user_object = self.database_collection_object.find_one(search_query)
        user_preferred_emailTime = user_object["user_preferred_emailTime"]
        return user_preferred_emailTime
    

