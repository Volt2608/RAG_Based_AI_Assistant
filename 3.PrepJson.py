# %%
# since we need to send a list of chunks to an embedding model that runs on a local host, we will send post requests.
# port 11434 - Ollama server for embeddings

# This script converts lecture chunks into embeddings so they can be semantically searched
# and retrieved as part of a RAG system.


import os                   # Will use it to list files inside a folder.
import requests             # Python library for HTTP, to send a POST request
import json                 # To read JSON files
import pandas as pd         # to make dataframe
import joblib               # to store the saved model for reuse, without running it everytime.


# This function: Takes text list, sends it to an embedding model, gets semantic vectors back
def create_embedding(text_list):
    r = requests.post(
    "http://localhost:11434/api/embed",
    json={                                         # Data being sent to the API in JSON format.
        "model": "bge-m3",                         # bge-m3 converts text into semantic vectors.
        "input": text_list})

    embedding = r.json()["embeddings"]            # Parses JSON body into a Python dict or list
    return embedding



# Read all JSON files created in the previous step
jsons = sorted(os.listdir("audio_jsons"), key=lambda x: int(x.split("_")[1].split(".")[0]))          # sorted number wise
my_dicts = []                                                                                        # empty list to store all chunks
chunk_id = 0                                                                                         # chunk id initialized to 0

# Loading every iteration of JSON file using a for loop
# The embedding function expects a list of texts, so I batch all chunk text into a list before sending it to the model.

for eachFile in jsons:
    with open(f"audio_jsons/{eachFile}") as f:
        data = json.load(f)

    print(f"Processing embedding for : {eachFile}")

    # 1. Collect all chunk text
    texts = []
    for chunk in data["chunks"]:
        texts.append(chunk["text"])

    # 2. Call embedding ONCE per file
    embeddings = create_embedding(texts)

    # 3. Store embeddings with chunks
    for i, chunk in enumerate(data["chunks"]):
        my_dicts.append({
            "chunk_id": chunk_id,
            "number": chunk["number"],
            "text": chunk["text"],
            "title": chunk["title"],
            "start": chunk["start"],
            "end": chunk["end"],
            "embedding": embeddings[i]
        })
        chunk_id += 1


    print("Completed embedding processing for all chunks")


df = pd.DataFrame.from_records(my_dicts)
joblib.dump(df , 'embeddings.joblib')

# Line of code explanation:
# create a function, that sends text chunks to a local embedding model and returns their vector representations.

# WHY THIS FUNCTION -
# This function is critical in the RAG pipeline because embeddings allow semantic similarity search,
# which enables accurate retrieval of relevant lecture content before generating answers.

# 2. I explicitly sort the files numerically to avoid filesystem ordering issues.

# 3. The embedding function expects a list of texts, so I batch all chunk text into a list before sending it to the model.

# 4. The output is structured so it can be directly inserted into a vector database or queried during retrieval.