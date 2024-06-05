# TeeCustomizer 👕
This project is about creating chatbot assistant that can answer customer questions about TeeCustomizer - t-shirt customization store.

# Access
You can access this site using [chat interface](https://6fb0-46-172-71-187.ngrok-free.app/)

# Technologies
- Langchain
- Faiss
- RAG
- Ollama (self-hosted AI, possibly can be changed to huggingface)
- Mistral
- Chainlit

# Getting started
In order to run this, you need to:
- install required libraries using `pip install -r requirements.txt`
- install ollama from [here](https://ollama.com/download/windows)
- run app using `chainlit run main.py --port 5000`

# QnA
Q: what tricks would you implement to handle all the cases

A: The only trick is to use LLM Agent that can execute tools, so it will have access both to already written knowledge such as FAQ, as well as ability to communicate with the human support

Q: how would you extend to multilingual support?)

A: some models can answer questions on multiple languages by default, but the performance can degrade. Some basic options is to use language classification model with translator, more complex and better solution might involve developing separate model or finetune existing on a target language. Also we might need to update FAQ and retrieve FAQ in the relevant language as well.

Q: how would you evaluate chatbot performance?

A: user feedback(or A/B testing if we have multiple models), testing dataset, rule-based checking on FAQ questions

Q: what would you do to increase chatbot performance and capabilities?

A: choose better model, prompt engineering, update knowledge base (FAQ), add more tools if needed. If we have user feedback - finetune.
