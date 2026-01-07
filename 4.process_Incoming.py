# %%
import numpy as np
import requests
import joblib
from sklearn.metrics.pairwise import cosine_similarity


# This function: Takes text list, sends it to an embedding model, gets semantic vectors back
def create_embedding(text_list):
    r = requests.post(
    "http://localhost:11434/api/embed",
    json={                                         # Data being sent to the API in JSON format.
        "model": "bge-m3",                         # bge-m3 converts text into semantic vectors.
        "input": text_list})

    embedding = r.json()["embeddings"]
    return embedding


def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate", json={
        "model" : "mistral",
        "prompt" : prompt,
        "stream" : False,
    })
    return r.json()["response"]


df = joblib.load('embeddings.joblib')

incoming_query = input(
"""
Course name : Introduction to Computer Science and Programming in Python
Source : MIT Open Course Ware 

Please ask a question related to the following Python topics covered in this course:
- Computation
- Branching
- Iteration
- String Manipulation
- Guess and Check
- Approximation
- Bisection
- Functions
- Tuples, Lists
- Aliasing, Mutability, Cloning
- Recursion
- Dictionaries
- Testing, Debugging
- Exceptions, Assertions
- Object-Oriented Programming
- Classes, Inheritance

Examples of good questions:
- What is a while loop?
- Where is inheritance explained?
- How does recursion work in this course?
- What is the difference between lists and tuples?
- When are exceptions discussed?

Questions outside these topics may not be answered, Thank you.

Enter your question:
""")


question_embedding = create_embedding([incoming_query])[0]

similarity = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()
if similarity.max() < 0.2:
    print("I can only answer questions related to this course.")
    exit()

topResults = 5
max_index = similarity.argsort()[::-1][0: topResults]

new_df = df.loc[max_index]

new_df = new_df.copy()
new_df["start"] = new_df["start"].apply(lambda s: f"{int(s//60)}:{int(s%60):02d}")
new_df["end"]   = new_df["end"].apply(lambda s: f"{int(s//60)}:{int(s%60):02d}")

prompt = f'''I am teaching "Introduction to Computer Science and Programming in Python" using MIT Open Course Ware.
Here are the video chunks containing video title, video number, video start time in seconds,
video end time in seconds, the text at that time :

{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}
--------------------------------------------------
"{incoming_query}"
Rules (must follow strictly):
- Use ONLY words and concepts that explicitly appear in the video chunk text.
- The question keyword MUST appear in the lecture text.
- Do NOT infer, summarize beyond the text, or use outside knowledge.
- Do NOT include links or URLs.
- Mention:
  • Lecture number
  • Timestamp in mm:ss
  • Exact topic as stated in the lecture
- Guide the user like:
  "Go to Lecture X around mm:ss"

If the keyword or concept asked in the question does NOT explicitly appear
in the provided video chunk text, reply exactly with:
"Nothing is mentioned as such in this course."
'''

with open ("prompt.txt", "w") as f:
    f.write(prompt)

response = inference(prompt)
print(response)

