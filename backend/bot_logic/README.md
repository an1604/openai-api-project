# Banking Products Chatbot with Tools

## Installation
```bash
pip install -r backend/requirements.txt
pip install -e bot_logic
```

## Environment Variables
```.env
OPENAI_API_KEY=*****
```

## Usage
Make embeddings for the knowledge base. Assumes `knowledgebase.csv` is in the bot_logic directory. Assumes running from backend.
```bash
python3 bot_logic/make_embeddings.py
```

Start Chatbot in UI:
```bash
python3 app.py
```

Start Chatbot in CLI:
```bash
python3 bot_logic/main.py
```
Running the chatbot will create logs in the `chatbot.log` file by default right now.