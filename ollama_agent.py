from langchain_community.chat_models import ChatOllama
import config
from langchain.tools import Tool
from embeddings import load_embeddings
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from langchain.agents import create_tool_calling_agent, AgentExecutor, create_json_chat_agent, create_react_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain.agents.output_parsers import ReActJsonSingleInputOutputParser, JSONAgentOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


class CustomParser(ReActJsonSingleInputOutputParser):
    def parse(self, text: str):
        try:
            return super().parse(text)
        except Exception as e:
            raise ValueError('Reply should contain Final Answer or Action with a valid JSON object (with a double quotes).')


def human_input_func(query: str) -> str:
    '''
    This function simulates the human customer support.
    :param query:
    :return: str
    '''
    return f"Please contact us at support@anadea.com"


def get_tools():
    human_tool = Tool(name='human', func=human_input_func, description=config.HUMAN_INPUT_DESCRIPTION)
    faiss_db = load_embeddings(config.FAISS_PATH)
    retriever_tool = create_retriever_tool(faiss_db.as_retriever(search_kwargs={'k': 3}), "FAQ",
                                           config.FAQ_RETRIEVER_DESCRIPTION)
    tools = [retriever_tool, human_tool]

    return tools


def get_llm():
    # use self-hosted ChatOllama
    llm = ChatOllama(model=config.MODEL_NAME)
    return llm


def get_prompt_template():
    chat_template = ChatPromptTemplate.from_messages(
        [
            ('system', config.SYSTEM_PROMPT),
            ('user', config.HUMAN_PROMPT),
        ]
    )

    return chat_template


def get_agent():
    '''
    Construct an AgentExecutor instance using llm, tools and prompt
    :return: AgentExecutor with memory
    '''
    llm = get_llm()
    tools = get_tools()
    prompt = get_prompt_template()
    # prompt = hub.pull('hwchase17/react-json')
    prompt = prompt.partial(
        tools='\n'.join([tool.description for tool in tools]),
        tool_names=', '.join([tool.name for tool in tools])
    )
    llm = llm.bind(stop=['\nFinal Answer'])
    agent = create_react_agent(llm, tools, prompt, output_parser=CustomParser())
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    memory = ChatMessageHistory()
    agent_executor = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: memory,
        input_messages_key='input',
        history_messages_key='chat_history'
    )
    return agent_executor
