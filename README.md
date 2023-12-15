
# Chatbot Setup Guide

Choose one of the two methods below based on your needs:

## A. Production Setup:

### 1. **Database Setup:**

#### Install Docker

#### Start Docker with the Script:

## IMPORTANT
Ask an admin for the azure OPENAI_API_KEY and add it in line 10 of the ./setup_and_run_prod.sh script


  ```bash
  ./setup_and_run.sh --mode prod --host [your_host_here]
  ```

---

## B. Development Setup:

### 1. **Database Setup:**

#### Install Docker

#### Start Only the Database Service:

  ```bash
  ./setup_and_run.sh --mode dev --host [your_host_here]
  ```

### 2. **Backend Setup:**

Navigate to the backend directory:

  ```bash
  cd backend
  ```

#### Install Python

#### Install Pip

#### Install Python-Venv

#### Create your venv

  ```bash
  python3 -m venv venv
```

#### Create your venv

  ```bash
  source venv/bin/activate
  ```

#### Install Required Python Packages:

  ```bash
  pip install -r requirements.txt
  pip install -e bot_logic
  ```

 ## Initialization of the bot logic:
  ```bash
  python3 bot_logic/make_embeddings.py
  ```

#### Run the Backend Application:
  ```bash
  python3 app.py
  ```

### 3. **Frontend Setup:**

Navigate to the frontend directory:

  ```bash
  cd ../frontend
  ```

#### Install Node.js


#### Install NPM Packages:

  ```bash
  npm i
  ```

#### Start the Frontend Application:

  ```bash
  npm start
  ```

---

## C. **Ngrok setup:**

#### Create ngrok free account

https://ngrok.com

#### Authenticate your account in CLI

Token and command to copy&paste can be found in your ngrok dashboard after logging in

#### Run ngrok tunnel

  ```bash
  ngrok http 5000
  ```

#### Copy ngrok tunnel address

![image](https://github.com/insait-io/chatbot/assets/132831936/f8b3ff70-9aeb-4da4-b205-8e14c2741148)


---

## D. **Twilio setup:**

#### Log into Insait Twilio account

#### Choose to edit Whatsapp Senders

In the side bar until the *Develop* tag, click on *Messaging*, then *Whatsapp Senders*

#### Choose Edit Sender for the the preferring number (prod or staging)

![image](https://github.com/insait-io/chatbot/assets/132831936/8bfa979f-7bf0-4be2-adce-8079f5a282c2)

#### Paste your ngrok tunnel to the Webhook URL followed by /send_whatsapp_hebrew_cd endpoint

![image](https://github.com/insait-io/chatbot/assets/132831936/2d8accdc-8514-4e71-ac64-fbd4bc9d9870)

Save your configuration by clicking on *Update Whatsapp Sender*.

#### Your backend should now be connected to the Whatsapp number!
