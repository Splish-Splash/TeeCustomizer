from __future__ import annotations

import os

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import AutoConfig
import config

# one of the best embedding model compared to it's size
# huggingface.co/spaces/mteb/leaderboard


def create_embeddings(docs: list[str], result_path: str | os.PathLike) -> FAISS:
    """
    For a given list of docs, create embedding and vectorstore from it

    :param docs: list of string with information to query by the model
    :param result_path: path to the result file with vectorstore
    """

    embeddings = get_embedding_model()

    # for this task we use FAISS due to a scale of the data
    # for more serious cases I suggest to use vector DBs such as Milvus
    faiss_db = FAISS.from_texts(docs, embeddings)
    faiss_db.save_local(result_path)

    return faiss_db


def load_embeddings(filepath: str | os.PathLike) -> FAISS:
    """
    Load vectorstore from a filepath

    :param filepath:
    :return:
    """

    embeddings = get_embedding_model()
    faiss_db = FAISS.load_local(filepath, embeddings, allow_dangerous_deserialization=True)
    return faiss_db


def get_embedding_model() -> HuggingFaceEmbeddings:
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME,
                                       model_kwargs=dict(trust_remote_code=True))
    return embeddings
