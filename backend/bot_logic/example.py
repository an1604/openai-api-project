from tool_chatbot.chat_tools import query_knowledgebase
import pdb
pdb.set_trace()
q = 'Why should I take a loan with Leumi?'
answer = query_knowledgebase(q)
print(answer)
