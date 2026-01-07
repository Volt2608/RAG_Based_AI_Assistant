# %%
# What We’ll Build in This Project -

# In this project, we’ll build a RAG-based AI Teaching Assistant designed for our Data Science course.
# Using Retrieval-Augmented Generation (RAG), the assistant will be able to fetch relevant information
# from course materials and provide accurate, context-aware answers—just like a real teaching assistant.

# Step 1.
# I wrote a python program that converted all the MP4 files into MP3's since whisper ( a module which we will later
# use in this project that basically helps to convert speech to text ) takes MP3's, and saved all the converted mp3s in
# a folder named "audios", made by using os module. Saved the program under 1.mp4ToMp3.ipynb.


# information ----------------Tools that we used here ----------- Information -----------------

# " FFmpeg "

# FFmpeg is a command-line tool/library that can:
    
# Load audio/video files
# Convert between formats
# Extract audio from video
# Resample audio
# Cut, merge, compress, etc.
# Whisper needs FFmpeg because Whisper cannot directly read .mp3, .mp4, .wav, etc.
# FFmpeg decodes them and hands raw audio to Whisper.

#-----------------------------------------------------------------------------------------------

# " Whisper "     -       OpenAI’s automatic speech-to-text model    
# It listens to audio/video and converts speech into text — super accurately.

# Think of it as:
# “The model that turns voice into subtitles/transcripts.”

# Transcribe audio → text
# Generate subtitles for videos
# Translate speech from one language to English
# Handle noisy audio extremely well
# Understand many languages automatically
# Work fully offline on your computer
#-----------------------------------------------------------------------------------------------

# %%
# As I downloaded 10 videos from YouTube related to Python that has 10 lectures of around 20-30 minutes each.
# now we will convert these videos into mp3's using ffmpeg/ subprocess in python, for which the code is right below :

import subprocess          # Subprocess Allows Python to run external programs (like ffmpeg).

input_file = "/Users/frolt/Git Projects/Data_Science/DS_ML_Projects/RAGbasedAI_assistant/videos/MIT6_0001F16_Lecture_10_300k.mp4"
output_file = "/Users/frolt/Git Projects/Data_Science/DS_ML_Projects/RAGbasedAI_assistant/videos/MIT6_0001F16_Lecture_10_300k.mp3"

subprocess.run(["ffmpeg", "-i", input_file, output_file])        # sb.run - takes a list of command line arguments
# %%
import subprocess       # Allows Python to run external programs (like ffmpeg).
import os              # os module provides functions for interacting with the operating system
import glob

# glob is a module that can search for files using patterns.
# Example pattern: "*.mp4" means “all files ending with .mp4”.

folder = "/Users/frolt/Git Projects/Data_Science/DS_ML_Projects/RAGbasedAI_assistant/videos"

# Get ALL .mp4 files in the folder
mp4_files = glob.glob(os.path.join(folder, "*.mp4"))

for mp4 in mp4_files:
    mp3 = mp4.replace(".mp4", ".mp3")
    print(f"Converting: {mp4} → {mp3}")
    
    subprocess.run(["ffmpeg", "-y", "-i", mp4, mp3])

# %%
import os 
import subprocess                     # Subprocess is a built-in Python module that lets Python run external programs.

folder = "videos"
files = os.listdir(folder)

os.makedirs("audios", exist_ok=True)   # ensures "audios" folder exists so ffmpeg can save output

for file in files:
    print(file)

    if not file.endswith((".mp3", ".mp4")):     # only process mp3/mp4 files
        continue


    # PART 1: Extract lecture number


    if file.startswith("Lecture_"):  

        name_without_ext = file.rsplit(".", 1)[0]      # Lecture_8
        parts_simple = name_without_ext.split("_")     # ["Lecture", "8"]

        if len(parts_simple) < 2:
            print("Skipping (unexpected filename):", file)
            continue

        try:
            lec_num = int(parts_simple[1])     # converts "8" into int 8
        except ValueError:
            print("Skipping (lecture number not numeric):", file)
            continue

    else:
        # original MIT6 filename format: MIT6_0001F16_Lecture_01_300k.mp4
        parts = file.split("_")

        if len(parts) < 4:                     # prevents IndexError when parts[3] doesn't exist
            print("Skipping (unexpected filename):", file)
            continue

        try:
            lec_num = int(parts[3])           # converts "01" → 1 into int
        except ValueError:
            print("Skipping (lecture number not numeric):", file)
            continue


    # PART 2: Rename the file
    

    ext = file.split(".")[-1]                 # extract extension (mp4/mp3)
    new_name = f"Lecture_{lec_num}.{ext}"     # new format filename: Lecture_8.mp4

    old = os.path.join(folder, file)          # full path to old file
    new = os.path.join(folder, new_name)      # full path to new file

    # rename only if the name is not already correct
    if old != new:
        os.rename(old, new)
        print(f"Renamed to → {new_name}")
    else:
        print(f"Already correct name → {new_name}")


    # PART 3: Convert MP4 to MP3 using ffmpeg


    if ext.lower() == "mp4":            # ONLY convert videos (.mp4), not audio (.mp3)
        output_name = f"Lecture_{lec_num}.mp3"                 # make clean mp3 name
        output_path = os.path.join("audios", output_name)      # path: audios/Lecture_8.mp3

        subprocess.run([
            "ffmpeg",
            "-i", new,            # input: the renamed mp4 file
            output_path           # output: mp3 inside audios folder
        ])

        print(f"Converted → {output_name}")
    else:
        print("No conversion needed (already mp3):", new_name)
