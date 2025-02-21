from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain import hub

def LLM_results(retrieved_text, query):
    #retrieved_text = "\n\n".join(result.page_content for result,score in results)
    prompt = hub.pull("rlm/rag-prompt")
    llm = OllamaLLM(model="hf.co/unsloth/DeepSeek-R1-Distill-Llama-8B-GGUF:Q2_K")
    rag_chain = prompt | llm | StrOutputParser()
    response = rag_chain.invoke({
        "context": retrieved_text,
        "question": query
    })
    print("Generated Response:")
    print(response)
    return response