import pymongo
import pytest
from production.Database_handling import Database_handling
from unittest.mock import Mock

class Test:
    
   def test_connect_to_db_table_and_get_collection_failure(self,monkeypatch):
      def mock_server_info():
         raise pymongo.errors.ConnectionFailure()
      
      monkeypatch.setattr(pymongo.MongoClient, 'server_info', lambda _ : mock_server_info())

      instance_of_class_DB_handling = Database_handling()
      with pytest.raises(SystemExit):
         instance_of_class_DB_handling.connect_to_db_table_and_get_collection()     
                
   def test_connect_to_db_table_and_get_collection_success(self):
      
      mocker = Mock()
      
      instance_of_class_DB_handling = Database_handling()
      
      mocker.patch.object(pymongo.MongoClient, 'server_info')

      collection = instance_of_class_DB_handling.connect_to_db_table_and_get_collection()

      assert isinstance(collection, pymongo.collection.Collection)

      assert collection.database.name == "QuotesDB"
      assert collection.name == "user_information_table"

    
   def test_store_new_user_in_DB(self, capfd):
      mock_collection_object = Mock(pymongo.collection.Collection)
      
      instance_of_class_DB_handling = Database_handling()
      instance_of_class_DB_handling.database_collection_object = mock_collection_object
            
      user_data = {}
      
      instance_of_class_DB_handling.store_new_user_in_DB(user_data)

      out, err = capfd.readouterr()

      assert out.strip() == "You are now succesfully registered/stored in db"
         
   def test_create_data_object_for_DB(self):
      user_first_name = "Maxi"
      user_email = "Maximiser@yahoo.com"
      user_pw = "1234"
      user_current_quote = "Never give up"
      user_already_sent_quotes = [";lkj;l", ";lkj;l", "lkj;l"]
      user_preferred_emailTime = "17:00"
      expected_user_data = {
         "first_name": user_first_name,
         "user_email": user_email,
         "user_pw": user_pw,
         "quote": user_current_quote,
         "user_preferred_emailTime": user_preferred_emailTime,
         "already_used_quotes": user_already_sent_quotes,
         "keywords":[]
         
      }

      actual_user_data = Database_handling.create_data_object_for_DB(user_first_name=user_first_name, user_email= user_email, user_pw=user_pw,user_current_quote=user_current_quote,user_already_sent_quotes=user_already_sent_quotes,user_preferred_emailTime=user_preferred_emailTime,keywords=[] )

      assert actual_user_data == expected_user_data

   def test_update_user(self, monkeypatch):
      user_email = "maxi@gmx.at"
      new_quote = "quotenew"
      new_already_sent_quotes =["oldquote"]
      
      
      mock_collection_object = Mock(pymongo.collection.Collection)
      new_mock_collection_object = Mock(pymongo.collection.Collection)

      instance_of_class_DB_handling = Database_handling()
      instance_of_class_DB_handling.database_collection_object = mock_collection_object
      
      
      monkeypatch.setattr(instance_of_class_DB_handling.database_collection_object, 'update_one', new_mock_collection_object)
      instance_of_class_DB_handling.update_user(user_email=user_email, new_quote=new_quote, new_already_sent_quotes=new_already_sent_quotes)

   # https://stackoverflow.com/questions/3829742/assert-that-a-method-was-called-in-a-python-unit-test
      mock_collection_object.update_one.assert_called_once_with(
         {"user_email": user_email},
         {"$set": {"quote": new_quote, "already_used_quotes": new_already_sent_quotes}}
      )

   def test_update_users_prefered_emailTime(self, monkeypatch):
      user_email = "maxi@gmx.at"
      preferred_email_time = "13:00"

      mock_collection_object = Mock(pymongo.collection.Collection)

      instance_of_class_DB_handling = Database_handling()
      instance_of_class_DB_handling.database_collection_object = mock_collection_object

      new_mock_collection_object = Mock()
      monkeypatch.setattr(instance_of_class_DB_handling.database_collection_object, 'update_one', new_mock_collection_object)

      instance_of_class_DB_handling.update_users_prefered_emailTime(user_email=user_email, preffered_email_time=preferred_email_time)

   # https://stackoverflow.com/questions/3829742/assert-that-a-method-was-called-in-a-python-unit-test
      mock_collection_object.update_one.assert_called_once_with(
         {"user_email": user_email},
         {"$set": {"user_preferred_emailTime": preferred_email_time}}
      )


   def test_get_user_keywords(self):
      user_email = "maxi@gmx.at"
      expected_keywords = ["soccer", "coding"]

      mock_collection_object = Mock()

      instance_of_class_DB_handling = Database_handling()

      instance_of_class_DB_handling.database_collection_object = mock_collection_object

      
      mock_user_object = {"keywords": expected_keywords}
      mock_collection_object.find_one.return_value = mock_user_object

      result = instance_of_class_DB_handling.get_user_keywords(user_email)

      assert mock_collection_object.find_one.call_args == (({"user_email": user_email},), {})
      assert result == expected_keywords
   


   def test_get_user_name(self):

      user_email = "maxi@yahoo.com"
      expected_first_name = "Max"

      mock_collection_object = Mock()

      instance_of_class_DB_handling = Database_handling()

      instance_of_class_DB_handling.database_collection_object = mock_collection_object

      mock_user_object = {"first_name": expected_first_name}
      mock_collection_object.find_one.return_value = mock_user_object

      result = instance_of_class_DB_handling.get_user_name(user_email)

      assert result == expected_first_name


   def test_update_keywords(self, capfd):

      user_email = "max@yahoo.com"
      new_keywords = ["soccer", "coding"]

      mock_collection_object = Mock()

      instance_of_class_DB_handling = Database_handling()

      instance_of_class_DB_handling.database_collection_object = mock_collection_object

      instance_of_class_DB_handling.update_keywords(user_email, new_keywords)

      out, _ = capfd.readouterr()

      mock_collection_object.update_one.assert_called_once_with(
         {"user_email": user_email},
         {"$set": {"keywords": new_keywords}}
      )


      assert out.strip() == "Succesfully updated keywords"


   def test_delete_user_from_database(self):

      user_email = "max@gmx.com"

      mock_collection_object = Mock()

      instance_of_class_DB_handling = Database_handling()

      instance_of_class_DB_handling.database_collection_object = mock_collection_object

      result = instance_of_class_DB_handling.delete_user_from_database(user_email)

      mock_collection_object.delete_one.assert_called_once_with({"user_email": user_email})

      assert result == mock_collection_object.delete_one.return_value


   def test_get_users_prefered_emailTime(self):

      mock_return_value_for_db = {"user_preferred_emailTime": "17:00"}

      mock_collection_object = Mock()
      mock_collection_object.find_one.return_value = mock_return_value_for_db

      instance_of_class_DB_handling = Database_handling()
      instance_of_class_DB_handling.database_collection_object = mock_collection_object

      user_email = "max@gmail.com"
      result = instance_of_class_DB_handling.get_users_prefered_emailTime(user_email)

      assert result == mock_return_value_for_db["user_preferred_emailTime"]

      mock_collection_object.find_one.assert_called_once_with({"user_email": user_email})
