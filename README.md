# Personalized Daily Quotes Generater by *chatGPT API*

## Overview:

The Motivational Quotes Program is designed to send personalized motivational quotes to subscribed users via email. The program follows a localy executed "Client-Server" model where the client-side involves a Graphical User Interface (GUI) for user interaction and subscription management, and the server-side involves a backend system responsible for generating and sending personalized quotes per email. Both, frontend and backend, use the database as their shared resource.

- all code necessary to run the program can be found in production folder.
- to run program on a personal machine, a chatGPT API subscription (0.01cent per quote), and a yahoo email account is needed.

## Workflow:

1. **User Interaction/ Sign in**:
   - Users interact with the GUI to subscribe to the motivational quotes program, set keywords and preffered email receiving time, and manage their subscription.
   
2. **Data Storage**:
   - User preferences and subscription details are stored locally in a MongoDB database.

3. **Quote Generation**:
   - Based on user preferences stored in the database, the system generates personalized motivational quotes using ChatGPT.

4. **Email Sending**:
   - The backend system schedules email sending based on user preferences.
   - At scheduled times, the system retrieves personalized quotes from the database and sends them to subscribed users via email.
   - This program must be up and running constantly to send emails. Can run in background on Raspberry Pi or any machine within supplied Docker-container structure.

## Considerations:

- **Scalability**: The design allows for scalability by changing to a server-client structure and migrating to the cloud.
- **Security**: A password authentication is not included, but a dummy password is already stored for each user.
- **Testing**: The main 3 modules of this program, userInformation_handling, chatGPT_quote_generator and database_handling are all fully tested. Automated tests can be viewed in "AutomatedTests" folder.

Keywords: Motivational quotes, email Quotes, chatgptAPi, raspberryPi projects, motivation, api, Container, Motivation, inspirational quotes
