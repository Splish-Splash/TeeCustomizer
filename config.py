FAISS_PATH = 'faiss_db'

MODEL_NAME = 'meta-llama/Meta-Llama-3-8B'
MODEL_KWARGS = dict(
    temperature=0
)
HUMAN_INPUT_DESCRIPTION = '''You can ask a support team for guidance when you think FAQ does not provide an answer to user question
Shortly describe key details from the conversation with user, output it along with the users question for the support team.
'''

FAQ_RETRIEVER_DESCRIPTION = '''This tool provides Q and A answers. For any question, you must use this tool.'''

SYSTEM_PROMPT = '''You're a helpful assistant in a t-shirt shop. 
Your task is to answer user questions and guide them towards the process of ordering a customizable t-shirt.
Here's the options for the coloring and styling of a t-shirt:
{options}
Also, if user asks question about something, use FAQ to give the answer. If FAQ does not contain answer to the question, 
ask a human about this (but input user question along with the key info about the user in a request as well)
'''