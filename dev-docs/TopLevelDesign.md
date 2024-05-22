# Top-Level Design - Motivational Quotes Program

## Overview:

The Motivational Quotes Program is designed to deliver personalized motivational quotes to subscribed users via email. The program follows a "Client-Server" model where the client-side involves a Graphical User Interface (GUI) for user interaction and subscription management, and the server-side involves a backend system responsible for generating and sending personalized emails. Both, frontend and backend, use the database as their shared resource.

### Components:

1. **User Interface (GUI)**
   - **Description**: This provides a place for users to subscribe, manage preferences, and interact with the program.
   - **Implementation**: Uses Tkinter.

2. **Backend System**
   - **Description**: The backend system is responsible for generating personalized motivational quotes based on user data stored in the db and sending them via email at scheduled times.
   - **Implementation**:
     - Accesses MongoDB for user information and preferences.
     - Utilizes OpenAI's API to generate motivational quotes.
     - Utilizes SMTP to send emails.
     - Python scheduler to send emails on time.

3. **User Information Handling**
   - **Description**: This module handles the storage and retrieval of user information from the local database.
   - **Implementation**: Implements functions to interact with the MongoDB database, including storing user preferences, retrieving subscriber lists, and updating user information.

4. **Quote Generation**
   - **Description**: Module responsible for generating motivational quotes and handling all interactions with ChatGPT.
   - **Implementation**: Interacts with OpenAI's ChatGPT module to generate personalized quotes according to user interests and preferences.

5. **Email Sending**
   - **Description**: This module is responsible for sending emails to subscribed users at scheduled times.
   - **Implementation**: Uses SMTP server with in app password. Implements a scheduler to trigger email sending based on user preferences.

## Workflow:

1. **User Interaction**:
   - Users interact with the GUI to subscribe to the motivational quotes program, set keywords and preffered times, and manage their subscription.
   
2. **Data Storage**:
   - User preferences and subscription details are stored locally in a MongoDB database.

3. **Quote Generation**:
   - Based on user preferences stored in the database, the system generates personalized motivational quotes using ChatGPT.

4. **Email Sending**:
   - The backend system schedules email sending based on user preferences.
   - At scheduled times, the system retrieves personalized quotes from the database and sends them to subscribed users via email.

## Considerations:

- **Scalability**: The design allows for scalability by eventually changing to a server-client structure and migrating to the cloud.
- **Security**: A password authentication is not included, but a dummy password is already stored for each user.
- **Testing**: The main 3 modules of this program, UserInformationHandling, chatGPTClass and Database_handling are all fully tested. Automated tests can be viewed in "AutomatedTests" folder.
