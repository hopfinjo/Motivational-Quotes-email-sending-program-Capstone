from production.userInformation_handling import UserInformation
from unittest.mock import Mock
import pymongo



class Test:
   
   
   def test_get_registration_information_from_user(self, monkeypatch):   
      monkeypatch.setattr('builtins.input', lambda _: "maxi")
      registerLoginUser_instance = UserInformation()
      result = registerLoginUser_instance.get_registration_information_from_user()
      first_name, password = result
      assert password=="1234" and first_name == "maxi" 

   # https://stackoverflow.com/questions/59986625/how-to-simulate-two-consecutive-console-inputs-with-pytest-monkeypatch
   def test_get_registration_information_from_user_empty_input(self, monkeypatch):
      responses = iter(["", "maxi@me.at"])
      monkeypatch.setattr('builtins.input', lambda _ : next(responses))   
      registerLoginUser_instance = UserInformation()

      result = registerLoginUser_instance.get_registration_information_from_user()
      result_user_first_name, result_user_pw = result
      assert result_user_first_name == "maxi@me.at"
      assert result_user_pw == "1234"

      
      
   def test_get_user_email_with_empty_input(self, monkeypatch):
      answers = iter(["", "example@me.com"])
      monkeypatch.setattr('builtins.input', lambda _ : next(answers))    
      registerLoginUser_instance = UserInformation()  
      user_email = registerLoginUser_instance.get_user_email()
      assert user_email == "example@me.com"
   
     
      
   def test_get_user_email(self, monkeypatch):
      monkeypatch.setattr('builtins.input', lambda _: "maxi@email.com")
      registerLoginUser_instance = UserInformation()
      result = registerLoginUser_instance.get_user_email()
      assert result == "maxi@email.com"

   def test_check_email_invalid(self):
      registerLoginUser_instance = UserInformation()
      result =  registerLoginUser_instance.check_email("invalidEmail")
    
      assert result == False
      
   def test_check_email_valid(self):
      registerLoginUser_instance = UserInformation()
      result =  registerLoginUser_instance.check_email("maxi@edu.duq")
    
      assert result == True
      
      
   def test_check_if_isexisting_user_true(self):
      
      registerLoginUser_instance = UserInformation()
      
      # set user email field, which is accesed by check if existing user
      registerLoginUser_instance.user_email = "Maxi@yahoo.com"

      mock_collection_object = Mock(pymongo.collection.Collection)

      mock_collection_object.find_one.return_value = {"Maxi@yahoo.com"}

      existing_user = registerLoginUser_instance.check_if_isexisting_user( mock_collection_object)

      assert existing_user is True

   def test_check_if_isexisting_user_false(self):
      
      registerLoginUser_instance = UserInformation()
      
      # set user email field, which is accesed by check if existing user
      registerLoginUser_instance.user_email = "Maxi@yahoo.com"

      mock_collection_object = Mock(pymongo.collection.Collection)

      mock_collection_object.find_one.return_value = None

      existing_user = registerLoginUser_instance.check_if_isexisting_user( mock_collection_object)

      assert existing_user is False

      
      
   def test_get_preferred_sending_time_userInput(self, monkeypatch):
      user_info_instance = UserInformation()
      monkeypatch.setattr('builtins.input', lambda _: "07:00")

      user_preffered_time = user_info_instance.get_preferred_sending_time()
      assert user_preffered_time=="07:00"
   
   def test_get_preferred_sending_time_default(self, monkeypatch):
      user_info_instance = UserInformation()
      monkeypatch.setattr('builtins.input', lambda _: "")

      user_preffered_time = user_info_instance.get_preferred_sending_time()
      assert user_preffered_time=="17:00"
      
   def test_get_preferred_sending_time_invalid_input(self, monkeypatch, capfd):
      user_info_instance = UserInformation()
      monkeypatch.setattr('builtins.input', lambda _: "1888")

      user_preffered_time = user_info_instance.get_preferred_sending_time()
      
      out, err = capfd.readouterr()
      
      assert out=="YOU ENTERED AN INVALID TIME, your time is set to 17:00 as default\n"
   
   
   def test_add_current_quote_to_alreadyUsed(self, monkeypatch):
      user_info_instance = UserInformation()
      new_current_quote = "Never give up"
      already_used_quotes=[]

      
      monkeypatch.setattr(user_info_instance,'user_current_Quote',new_current_quote)
      monkeypatch.setattr(user_info_instance,'already_used_quotes',already_used_quotes)

      
      user_info_instance.add_current_quote_to_alreadyUsed(new_current_quote,already_used_quotes)
      
      #assert user_info_instance.user_current_Quote==new_current_quote
      
      assert user_info_instance.already_used_quotes[0] == new_current_quote
      
      
      
   def test_add_current_quote_to_alreadyUsed_with_15_elements(self, monkeypatch):
      user_info_instance = UserInformation()
      already_used_quotes = ["Quote1"]  

      
      for i in range(2, 16):
         already_used_quotes.append("Quote"+str(i))

      new_current_quote = "New Quote"

      monkeypatch.setattr(user_info_instance, 'already_used_quotes', already_used_quotes)

      user_info_instance.add_current_quote_to_alreadyUsed(new_current_quote, already_used_quotes)

      assert user_info_instance.already_used_quotes[1] == already_used_quotes[1]
      # -1 is shortcut to access last element
      assert user_info_instance.already_used_quotes[-1] == new_current_quote

   def test_get_keywords_from_user(self, monkeypatch):
      user_info_instance = UserInformation()
      monkeypatch.setattr('builtins.input', lambda _: "soccer")

      return_string = user_info_instance.get_keywords_from_user()
      assert return_string == ["soccer"]

