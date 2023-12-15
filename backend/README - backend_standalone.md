
To run insait financial bot follow these steps:

### 0. **Prerequisite:**
Have an OpenAI API key. Ask an admin for the OpenAI API key if you haven't got one.
Type your OpenAI API key here:

### 1. **Backend Setup:**

#### Install Python
#### Install Pip
#### Install Python-Venv
We will assume the previous 3 are already installed.


#### Create your venv

  ```bash
  python3 -m venv venv
  ```

#### Activate your venv

  ```bash
  source venv/bin/activate
  ```

#### Install Required Python Packages:
 Navigate to the backend directory:

  ```bash
  cd backend
  ```

  ```bash
  pip install -r requirements.txt
  pip install -e bot_logic
  ```

### 2. **Env vars configuration:**

## Create env vars

Replace <OpenAI_API_key> with your key and run the following (Tip: Copy and paste everything, including the brackets):

  ```bash
  (echo "OPENAI_API_TYPE=open_ai" > .env;
  echo "OPENAI_API_VERSION=2020-11-07" >> .env;
  echo "OPENAI_API_BASE=https://api.openai.com/v1" >> .env;
  echo "OPENAI_API_KEY=<your secret key>" >> .env;
  echo "OPENAI_ENGINE=gpt-3.5-turbo" >> .env;
  echo "LOG_TO_FILE_ENABLED=0" >> .env;
  echo "LOGS_PATH=bot_logic/logs" >> .env;
  echo "CURRENT_LANGUAGE=english" >> .env;)
  ```

 ## Initialization of the bot logic:

  ```bash
  python3 bot_logic/make_embeddings.py
  ```

### 2. **Run the App from CLI:**

  ```bash
  python3 bot_logic/main.py
  ```
