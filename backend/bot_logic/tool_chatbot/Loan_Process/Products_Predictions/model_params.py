import joblib
import os

classifier_path = "/mnt/c/Users/adina/Desktop/תקיית_עבודות/chatbot-shira-fe-fixes/backend/bot_logic/tool_chatbot/Loan_Process/Products_Predictions/decision_tree_classifier.joblib"
sc_path = "/mnt/c/Users/adina/Desktop/תקיית_עבודות/chatbot-shira-fe-fixes/backend/bot_logic/tool_chatbot/Loan_Process/Products_Predictions/sc.pkl"
ct_path = "/mnt/c/Users/adina/Desktop/תקיית_עבודות/chatbot-shira-fe-fixes/backend/bot_logic/tool_chatbot/Loan_Process/Products_Predictions/ct.pkl"

# Load the models and scalers
classifier = joblib.load(classifier_path)
sc = joblib.load(sc_path)
ct = joblib.load(ct_path)
