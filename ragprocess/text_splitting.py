from langchain_text_splitters import RecursiveCharacterTextSplitter
def textChunks_split(docs):
    try:
        all_splits = []
        total_chunks = 0
        chunk_size = 10000
        chunk_overlap = 50
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=True
        )
        for doc in docs:
            splits = text_splitter.split_text(doc["text"])  # Split each document's text
            all_splits.append({
                "file_name": doc["file_name"],
                "splits": splits
            })
        
        for doc_splits in all_splits:
            total_chunks += len(doc_splits['splits'])
        print('Total chunks :',total_chunks,"\n")
        
        return all_splits
    
    except:
       
       return "error in text splitting"