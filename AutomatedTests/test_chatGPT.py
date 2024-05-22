from production.chatGPT_quote_generator import chatGPT

class Test:

    def test_createNewQuote(self):

        chat_gpt_instance = chatGPT()
        dummyarray=["hey"]
        result = chat_gpt_instance.createNewQuote(dummyarray,[])
        assert result != ""

    def test_createNewQuote2(self):

        chat_gpt_instance = chatGPT()
        dummyarray=["hey"]
        result = chat_gpt_instance.createNewQuote(dummyarray,["soccer", "coding"])
        assert result != ""


    def test_createQuoteFirstTime_not_empty(self):

        chat_gpt_instance = chatGPT()

        result = chat_gpt_instance.createQuoteFirstTime()

        assert result != ""
        
    def test_api_key_set(self):
        expected_api_key = "ADDKEYHERE"

        chat_gpt_instance = chatGPT()

        assert chat_gpt_instance.chatGPT_env_acces_key == expected_api_key
     