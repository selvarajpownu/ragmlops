from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def embedding_chunks_to_vectorStore(all_splits, job_description, total_chunks):
    chunks = []
    metadata = [] 
    for doc in all_splits:
        file_name = doc["file_name"] 
        for split in doc["splits"]:
            chunks.append(split)
            metadata.append({"file_name": file_name})  

    HF_model = HuggingFaceEmbeddings(model_name="C:/Users/selvaraj.x/OneDrive - Mphasis/Desktop/POCs/finetuned-embed-model/")
    
    HF_embeddings = HF_model.embed_documents(chunks)
    text_embedding_pairs = list(zip(chunks, HF_embeddings))
    
    vectorstore = FAISS.from_embeddings(
        text_embeddings=text_embedding_pairs,
        embedding=HF_model, 
        metadatas=metadata
    )
    
    query_embedding_hf = HF_model.embed_query(job_description)
    results = vectorstore.similarity_search_with_score_by_vector(query_embedding_hf, k= total_chunks)

    return results