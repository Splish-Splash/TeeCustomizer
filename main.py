import os.path

from utils import get_faq
from agent import get_agent
from embeddings import create_embeddings, load_embeddings
import config
qa_list = get_faq('data/FAQ.txt')

agent = get_agent()
embeddings_path = 'embeddings'
if not os.path.exists(config.FAISS_PATH):
    create_embeddings(qa_list, embeddings_path)

with open('data/options.txt', 'r') as f:
    options = f.read()

while True:
    agent.invoke(dict(options=options, user_input=input()))



