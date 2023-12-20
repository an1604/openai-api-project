import sys
sys.path.append(".")
import os
import openai
import dotenv
import faiss
from tool_chatbot.utils import get_embedding
from tool_chatbot.utils import get_faq

dotenv.load_dotenv()
assert os.getenv(
    "OPENAI_API_KEY"
), "Please set your OPENAI_API_KEY environment variable."
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
# Create FAISS index
index = faiss.IndexFlatL2(1536)

# Get FAQ
faq = get_faq()

# Add vectors to FAISS index
for qa in faq:
    index.add(get_embedding(qa))

# Save the index to a file
faiss.write_index(index, "bot_logic/vector_index.faiss")
