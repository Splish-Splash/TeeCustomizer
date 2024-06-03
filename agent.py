from langchain.tools.retriever import create_retriever_tool
from langchain.memory import ConversationBufferMemory
from langchain.chains.question_answering import load_qa_chain
from langchain.tools import HumanInputRun
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain import HuggingFacePipeline, PromptTemplate
from langchain.prompts import ChatPromptTemplate
import transformers
import torch
from embeddings import load_embeddings
import config


def human_input_func(query: str) -> str:
    print(f'The query is: {query}')
    result = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == 'q':
            break
        result += line
    return '\n'.join(result)


def get_tools():
    human_tool = HumanInputRun(input_func=human_input_func, description=config.HUMAN_INPUT_DESCRIPTION)
    faiss_db = load_embeddings(config.FAISS_PATH)
    retriever_tool = create_retriever_tool(faiss_db.as_retriever(), "FAQ", config.FAQ_RETRIEVER_DESCRIPTION)

    return [human_tool, retriever_tool]


def get_llm():
    pipeline = transformers.pipeline('text-generation', model=config.MODEL_NAME,
                                     model_kwargs={'torch_dtype': torch.bfloat16}, device_map='auto')
    llm = HuggingFacePipeline(pipeline, model_kwargs=config.MODEL_KWARGS)
    return llm


def get_prompt_template():
    chat_template = ChatPromptTemplate.from_messages(
        [
            ('system', config.SYSTEM_PROMPT),
            ('human', '{user_input}')
        ]
    )
    return chat_template


def get_agent():
    llm = get_llm()
    tools = get_tools()
    prompt = get_prompt_template()
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor
