from pymongo.mongo_client import MongoClient
from logger.logger import logger
from utils import config_reader
import os, shutil

mongo_uri = config_reader.configData()['config']['MONGODB_URL']
client = MongoClient(mongo_uri,connect=False)

try:
    client.admin.command('ping') 
    logger.info("You successfully connected to MongoDB!")
except Exception as e:
    logger.error(e)

mongodb_name = client.resumeparser

selected_resume = mongodb_name['selectedresume']

def resume_details_db(dataset_path, threshold_result, n):
    resume_set_document = {
        "folder_set_path": dataset_path,
        "no_of_resumes": len(threshold_result[:n]),
        "resume_details": [
            {
                "resume_name": result, 
                "confidence": float(score)
            }
            for result, score in threshold_result[:n]
        ]
    }
    selected_resume.update_one(
        {"folder_set_path": dataset_path},
        {"$set": resume_set_document},
        upsert=True
    )

def sync_database_with_results(dataset_path, threshold_result, n):
    if not threshold_result:
        selected_resume.delete_one({"folder_set_path": dataset_path})
        print(f"Removed resume set for path: {dataset_path}")
    else:
        resume_details_db(dataset_path, threshold_result, n)


def threshold_results(dataset_path, threshold_result, threshold, n):
    try:
        output_folder =f'C:/resumeParser/datasets/selected_resumes/top{threshold}%'
        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

        #empty the folder
        for file in os.listdir(output_folder):
            file_path = os.path.join(output_folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        # Save each result file to the output folder
        for file_name, _ in threshold_result[:n]:
            file_name = file_name
            source_path = os.path.join(dataset_path, file_name)  
            destination_path = os.path.join(output_folder, file_name)
            if os.path.exists(source_path):
                shutil.copy(source_path, destination_path)
            else:
                print(f"File {source_path} not found. Skipping.")
              
        sync_database_with_results(output_folder, threshold_result, n)
        
        print(f"\nSaved top {threshold}% of results to {output_folder}.")

    except:
        return "error in saving files"
