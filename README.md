🎓 RAG-Based AI Teaching Assistant

This project implements a Retrieval-Augmented Generation (RAG)–based AI Teaching Assistant that helps students navigate and understand Python concepts taught in MIT OpenCourseWare video lectures.
Instead of guessing answers, the assistant retrieves exact lecture segments with timestamps and generates grounded, context-aware explanations, similar to a real teaching assistant.

---------------------------------------------------------------------------------------------------------------------------------------------
🧠 What This Project Does : 

The assistant answers Python-related questions by:
Searching through MIT lecture transcripts
Retrieving the most relevant lecture segments
Generating answers strictly grounded in course content
Pointing users to the exact lecture and timestamp where a topic is explained
If a question is outside the scope of the course, the system explicitly refuses to answer, preventing hallucinations.

---------------------------------------------------------------------------------------------------------------------------------------------

🔁 RAG Pipeline Overview :

Video Lectures
   ↓
Audio Extraction
   ↓
Speech-to-Text (Whisper)
   ↓
Chunking + Metadata
   ↓
Embeddings (Ollama)
   ↓
Similarity Retrieval
   ↓
LLM-Generated Answer (Grounded)

---------------------------------------------------------------------------------------------------------------------------------------------

📚 Project Content Covered : 

The dataset is built from 10 MIT OpenCourseWare Python lectures, covering below topics :
Computation & Branching
Iteration & String Manipulation
Guess & Check, Approximation, Bisection
Functions, Tuples, Lists
Aliasing, Mutability, Cloning
Recursion
Dictionaries
Testing, Debugging, Exceptions, Assertions
Object-Oriented Programming (Classes, Inheritance)

---------------------------------------------------------------------------------------------------------------------------------------------
⚙️ Step-by-Step Implementation :

Step 1: Video → Audio Conversion

File: 1.mp4ToMp3.ipynb

RAG systems cannot operate directly on raw video, and Whisper requires audio input.
This step:

Converts .mp4 lecture videos into .mp3 audio files
Normalizes filenames for consistency
Ensures deterministic input for downstream processing
Output audio files are stored in an audios/ directory.

---------------------------------------------------------------------------------------------------------------------------------------------
Step 2: Audio → Transcripts (Whisper)

File: 2.mp3ToJson.ipynb

Lecture audio files are processed using the Whisper medium model to generate accurate transcriptions.

Each lecture is:
Transcribed into timestamped text segments
Enriched with lecture-level metadata extracted from filenames
Saved as structured JSON containing:
Full transcript
Chunked text
Start and end timestamps

This JSON becomes the foundation for embedding and retrieval.

---------------------------------------------------------------------------------------------------------------------------------------------
Step 3: Chunk Embedding & Vector Storage

File: 3.PrepJson.ipynb

In this stage:
Each transcript chunk is sent to a local Ollama embedding server
The embedding model converts text into semantic vectors
Each chunk is assigned a unique, deterministic chunk ID
All embeddings are stored for fast similarity search
These embeddings power the retrieval step of the RAG pipeline.

---------------------------------------------------------------------------------------------------------------------------------------------

Step 4: Retrieval-Augmented Question Answering

File: 4.process_incoming.py

This script implements the core RAG system.

Workflow:
User submits a question
The question is embedded using the same embedding model
Cosine similarity is used to find the most relevant lecture chunks
If no relevant content exists, the system refuses to answer

For valid queries:
Relevant lecture segments are selected
Timestamps are converted into readable minutes
A lightweight LLM generates an answer strictly limited to retrieved content
The final response explains the concept and tells the student exactly where to find it in the lecture.

---------------------------------------------------------------------------------------------------------------------------------------------

🛡️ Key Design Principles

No hallucinations – answers are grounded in retrieved lecture content
Deterministic pipeline – consistent filenames, chunk IDs, and embeddings
Explainability – every answer references exact lecture timestamps
Local-first architecture – Whisper and embeddings run locally

---------------------------------------------------------------------------------------------------------------------------------------------

🧰 Tech Stack

Python
Whisper (Speech-to-Text)
Ollama (Embeddings + LLM)
NumPy / Scikit-learn (Similarity Search)
Jupyter Notebooks
JSON-based intermediate storage

---------------------------------------------------------------------------------------------------------------------------------------------

📁 Ignored Files & Artifacts

The project intentionally ignores:
OS & environment files (.DS_Store, __pycache__, venv/)
Temporary caches & logs
Generated embeddings and prompt files
Secrets and environment variables
(See .gitignore for full details.)

---------------------------------------------------------------------------------------------------------------------------------------------

🎯 Use Case

This assistant is ideal for:
Students revising Python concepts
Learners searching lecture content efficiently
Demonstrating a real-world RAG pipeline using unstructured data (video → text)

---------------------------------------------------------------------------------------------------------------------------------------------
🚀 Future Improvements

Web or chat UI
Support for additional courses
Persistent vector database
Multi-query conversational memory
