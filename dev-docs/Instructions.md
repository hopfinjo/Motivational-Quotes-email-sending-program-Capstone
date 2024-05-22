# Instructions to run program not dockerized(If Dockerized, look into InstructionsContainer)
- Ensure you are running a Windows Operating System
- Install Python3
- Install pymongo: run pip install pymongo
- Install mongodb community edition: https://www.mongodb.com/try/download/community
- Install win32com.client pip install pywin32
- Install openai : run pip install openai

- Go to folder that Maximilian-Hopfer/production:
  - run: "python driver_backend_sendEmails.py" to start scheduler that sends emails.
  - run: "python GUI_MotivationalQuotes.py" to start GUI to interact with program.

## Instructions to run automated tests:
- Install pytest + coverage.
- In my installation, I did not add pytest+coverage as a system environment variable, therefore
  to run it I need following command: python -m pytest   or   python -m coverage


- run tests: go to Maximilian-Hopfer/AutomatedTests folder and run:
  - python -m pytest  
  - python -m coverage run -m pytest
  - python -m coverage report


 # Instructions to set up all environment variables and keys:
 - All variables that need to be set up for local environment are marked with a comment saying CHANGEME
 fast forward would be to go to files: ChatGPT + email_handling_SMTP and search for CHANGEME.
 - You need to add a private chatgpt API key, you have to be subscribed. This will be excpetionally cheap. 35 quotes are less than 1 cent.
 - You also need an email account used to send emails. A dummy .yahoo account would suffice. You have to use the in app password for this application.
 - Lastly, when running the GUI in a container, you must set the local ip address.
