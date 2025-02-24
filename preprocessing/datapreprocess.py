import os
import re
import nltk
import shutil
import fitz  
import easyocr  
import pandas as pd
from PIL import Image
from keybert import KeyBERT
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from langchain_community.document_loaders import Docx2txtLoader

reader = easyocr.Reader(["en"]) 

def load_text(file_path):
    with open(file_path,'r') as file:
        text = file.read()
    text = clean_file(text)
    return text

def load_docx(file_path):
    doc = Docx2txtLoader(file_path)
    documents = doc.load()
    text = "\n".join([doc.page_content for doc in documents])
    text = clean_file(text)
    return text

def load_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    text = clean_file(text)
    return text

def load_image(file_path):
    result = reader.readtext(file_path, detail=0)  
    text = "\n".join(result)
    text = clean_file(text)
    return text

def load_excel(file_path):
    df = pd.read_excel(file_path)
    text = df.to_string()  # Convert dataframe to string
    return text

def load_csv(file_path):
    df = pd.read_csv(file_path)
    text = df.to_string()
    return text

def clean_file(text):
    text = re.sub(r'[\*\-\•\+\.\|\(\â\€\¢\)]+', ' ', text)
    text = re.sub(r'[:;,.!?]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'|\u2022', '', text)
    text = re.sub(r'(\bPhone\b|\bEmail\b|LinkedIn|Website|Address)', '', text)
    return text

def summarize_keybert(text):
    try:
        kw_model = KeyBERT(model="BAAI/bge-small-en")
        keywords = kw_model.extract_keywords(text, top_n = 200)
        keywords = " ".join([kw[0] for kw in keywords])
        return keywords
    except:
        print("Unable to process text using keybert model")

def summarize_nltk(text):
    try:
        tokens = word_tokenize(text)
        nltk_stopwords = set(stopwords.words('english'))
        #fdist = FreqDist(filtered_tokens)
        #keywords = fdist.most_common()
        text = " ".join([word for word in tokens if word.lower() not in nltk_stopwords])
        return text
    except:
        print("error in nltk processing")

def fetch_jd_file(folder_path, keyword):
    for file in os.listdir(folder_path):
        if keyword.lower() in file.lower():
            selected_files = os.path.join(folder_path, file)
    return selected_files

def load_document(file_path):
    """Load text from various file types."""
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension == '.pdf':
        return load_pdf(file_path)
    elif file_extension == '.txt':
        return load_text(file_path)
    elif file_extension == '.xlsx':
        return load_excel(file_path)
    elif file_extension == '.csv':
        return load_csv(file_path)
    elif file_extension in ['.jpg', '.jpeg', '.png']:
        return load_image(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def process_input_files(input_path):
    """ Process a single file or all files in a folder."""
    docs = []
    if os.path.isfile(input_path): # file as input
        try:
            text = load_document(input_path)
            name, _ = os.path.splitext(os.path.basename(input_path))
            docs.append({"text": text, "file_name": name})
        except ValueError as e:
            print(f"Skipping {input_path}: {e}")
        except Exception as e:
            print(f"Unexpected error processing {input_path}: {e}")
    elif os.path.isdir(input_path): # folder as input
        for filename in os.listdir(input_path):
            file_path = os.path.join(input_path, filename)
            if os.path.isfile(file_path):
                try:
                    text = load_document(file_path)
                    name = filename
                    docs.append({"text": text, "file_name": name})
                except ValueError as e:
                    print(f"Skipping {filename}: {e}")
                except Exception as e:
                    print(f"Unexpected error processing {filename}: {e}")
    else:
        raise ValueError(f"The provided path '{input_path}' is neither a file nor a folder.")

    return docs
