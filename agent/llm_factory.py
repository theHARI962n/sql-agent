import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    provider = os.getenv("MODEL_PROVIDER", "openai")

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )

    elif provider == "groq":
        from langchain_groq import ChatGroq

        return ChatGroq(
            model=os.getenv("GROQ_MODEL", "llama3-8b-8192"),
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY")
        )

    # elif provider == "huggingface":
    #     from langchain_community.llms import HuggingFaceHub

    #     return HuggingFaceHub(
    #         repo_id=os.getenv("HF_MODEL"),
    #         huggingfacehub_api_token=os.getenv("HF_API_KEY")
    #     )

    else:
        raise ValueError("Unsupported MODEL_PROVIDER")