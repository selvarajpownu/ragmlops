from fastapi import APIRouter
from models.resumeFile import ResumeFile
from preprocessing.datapreprocess import process_input_files, fetch_jd_file, summarize_keybert, summarize_nltk
from ragprocess.text_splitting import textChunks_split
from ragprocess.embed_vectorstore import embedding_chunks_to_vectorStore
from ragprocess.llm_query import LLM_results
from database.connectDB import threshold_results
router = APIRouter()

api_endpoint_entry = "/api/staging"


@router.post(api_endpoint_entry+'/')
async def Post_resume_files(userinput: ResumeFile):
    try:
        dataset_path = userinput.Resume_filepath
        jd_dataset_path = userinput.Jobdesc_filepath
        keyword = userinput.Keyword
        query = userinput.Query
        docs = process_input_files(dataset_path)
        print(f"Processed {len(docs)} documents successfully.\n")
        total_files = len(docs)
        all_splits = textChunks_split(docs) 
        
        total_chunks = 0
        for doc_splits in all_splits:
            total_chunks += len(doc_splits['splits'])

        jd_file = fetch_jd_file(jd_dataset_path, keyword)
        
        jd_text = process_input_files(jd_file)
        for text in jd_text:
            job_description = text["text"]

        results = embedding_chunks_to_vectorStore(all_splits, job_description, total_chunks)
        
        for result,score in results:
            file_name = result.metadata["file_name"] 
            print(f"{file_name} with score {score}")
        
        print(f"\nResume suited of your given job Descriptions")
        thresholds = [50,]
        seen_files = set()
        threshold_result = []
        for threshold in thresholds:
            print(f"\nTop {threshold}% selected resumes\n")
            n = max(1, int((threshold/100)*total_files))
            for result,score in results:
                file_name = result.metadata["file_name"] 
                if file_name not in seen_files:
                    threshold_result.append((file_name, score))
                    seen_files.add(file_name) 
            for file_name, score in threshold_result[:n]:
                print(f"{file_name} with score {score}")
            threshold_results(dataset_path, threshold_result, threshold, n)

        """
        key_extract = []
        for result,_ in results[:2]:
            text = summarize_keybert(result.page_content)
            #text = summarize_nltk(result.page_content)
            key_extract.append(text)
        text = "\n\n".join(key_extract)"""
        
        #response = LLM_results(text, query)

        return {"Response"}
        
    except:
        return {
            "status": 500,
            "Error": "Internal Server Error"
        }
