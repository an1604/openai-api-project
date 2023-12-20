import logging
import os
from app_utils.models import db, Conversations, Message, Requests
from bot_logic.tool_chatbot.chatbot_wrapper import ChatBot
from app_utils.utils import setup_logger
from bot_logic.tool_chatbot.utils import get_bot_configuration
import openai
from flask import Flask, request, g
from flask_cors import CORS
import uuid
import pickle
from dotenv import load_dotenv
import os
import json
from datetime import datetime


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

load_dotenv('.env')

setup_logger()

# DATABASE
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
db.init_app(app)

# OPENAI
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_type = os.getenv('OPENAI_API_TYPE')
openai.api_base = os.getenv('OPENAI_API_BASE')
openai.api_version = os.getenv('OPENAI_API_VERSION')


def deserialize_chatbot(conversation):
    return pickle.loads(conversation.conversation_obj)


def add_conversation_with_pickle(chatbot_obj, uid):
    serialized_chatbot = pickle.dumps(chatbot_obj)
    conversation = Conversations(
        conversation_obj=serialized_chatbot, history=chatbot_obj.conversation, id=uid)
    db.session.add(conversation)
    db.session.commit()


def update_conversation(conversation_id, chatbot):
    conversation = db.session.get(Conversations, conversation_id)
    if not conversation:
        return f"No conversation found with ID {conversation_id}"
    serialized_data = pickle.dumps(chatbot)
    conversation.conversation_obj = serialized_data
    conversation.history = chatbot.conversation
    db.session.commit()
    return

def update_request_id(uid):
    current_request_id = str(uuid.uuid4())
    request = db.session.get(Requests, uid)
    if not request:
        new_request = Requests(conversation_id=uid, request_id=current_request_id)
        db.session.add(new_request)
        db.session.commit()
    else: 
        request.request_id = current_request_id
        db.session.commit()
    return current_request_id

def get_conversation_by_id(conversation_id):
    if not conversation_id:
        app.logger.info("Conversation ID is missing")
        return None
    conversation = db.session.get(Conversations, conversation_id)
    return conversation


def get_daily_conversations_count():
    today = datetime.utcnow().date()
    count = Conversations.query.filter(
        db.func.date(Conversations.created_at) == today
    ).count()
    return count

def save_messages_to_db(uid, user_input):
    new_message = Message(conversation_id=uid, user_input=user_input)
    db.session.add(new_message)
    db.session.commit()
    app.logger.info('Message saved to database')
    return


def continue_conversation(uid, user_input, chatbot_serialized):
    chatbot = deserialize_chatbot(chatbot_serialized)
    ai_response = chatbot.generate_response(user_input)
    update_conversation(uid, chatbot)
    return ai_response


@app.route('/send_local_hebrew_cd', methods=['POST'])
def send_message_local():
    try:
        daily_conversations = get_daily_conversations_count()
        app.logger.info(f"Daily conversations count: {daily_conversations}")
        if daily_conversations > 100:
            app.logger.info("Daily conversation limit reached")
            return "ERROR! Daily conversation limit reached.", 429

        content_type = request.headers.get('Content-Type', '')
        app.logger.info(f'Received request with Content-Type: {content_type}')

        data = json.loads(request.data)

        app.logger.info("\n\n" + "Received data: " + str(data) + "\n\n")

        user_input = data['Body']
        app.logger.info(user_input)

        uid = data['WaId']

        save_messages_to_db(uid, user_input)

        conversation = get_conversation_by_id(uid)

        current_request_id = update_request_id(uid)

        if not conversation:
            app.logger.info("No conversation found. Generating initial message")
            chatbot = ChatBot(**get_bot_configuration())
            ai_response = chatbot.generate_initial_message()
            add_conversation_with_pickle(chatbot, uid)
        else:
            app.logger.info("Conversation found. Getting all unreplied messages")
            new_messages = Message.query.filter_by(conversation_id=uid, processed=False).all()
            full_conversation_text = " ".join(message.user_input for message in new_messages)
            app.logger.info(f"Full conversation text: {full_conversation_text}")
            ai_response = continue_conversation(
                str(uid), full_conversation_text, conversation)
            current_request = Requests.query.filter_by(conversation_id=uid).first()
            if current_request.request_id != current_request_id:
                app.logger.info("Request already updated. Returning 200")
                return "", 200
            for message in new_messages:
                message.processed = True
                db.session.commit()

        msg = "\n\n" + "Sender: " + \
            str(uid) + "\nMessage: " + user_input + \
            "\nResponse: " + ai_response + "\n\n"
        app.logger.info(msg)

        return ai_response

    except Exception as e:
        logging.exception("Error occurred while processing request")
        return str(e), 500


@app.route('/health', methods=['GET'])
def health_check():
    app.logger.info("Health check successful")
    return "DONE CONFIRMED!", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
