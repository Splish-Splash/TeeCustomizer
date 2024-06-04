import os.path

from utils import get_faq
# from agent import get_agent, get_tools
from ollama_agent import get_agent, get_tools
from embeddings import create_embeddings, load_embeddings
import config
import chainlit as cl


qa_list = get_faq('data/FAQ.txt')

embeddings_path = config.FAISS_PATH
if not os.path.exists(config.FAISS_PATH):
    create_embeddings(qa_list, embeddings_path)
agent = get_agent()
tools = get_tools()
tools_description = '\n'.join([tool.description for tool in tools])
tool_names = ', '.join([tool.name for tool in tools])
with open('data/options.txt', 'r') as f:
    options = f.read()

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("agent", agent)

@cl.on_message
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")
    res = await agent.ainvoke(dict(options=options, input=message.content),
                     config={'configurable': {'session_id': 42}}, callbacks=[cl.AsyncLangchainCallbackHandler()])
    await cl.Message(content=res['output']).send()

# print('I am here')
# while True:
#     answer = agent.invoke(dict(options=options, input=input()),
#                      config={'configurable': {'session_id': 42}})
#
# print('THe final answer', answer)
# while True:
#     agent.invoke(dict(options=options, input=input(), tools=tools_description, tool_names=tool_names,
#                       ),
#                  config={'configurable': {'session_id': 42}})
#     print('end')



