# %%

import whisper                 # imported modules
import os
import json

model = whisper.load_model("medium")                                                        # using model medium for transcription

audios = os.listdir("audios")                                                               # listed all audio files in audios folder

for audio in audios:                                                                        # iterating through each audio file
  number = audio.split("_")[1][:-4]                                                         # extracting number and title from file name
  title = audio.split("_")[0]                                                               # extracting title from file name

  result = model.transcribe(audio = f"audios/{audio}", language="en", task="transcribe")    # transcribing audio file

  chunks = []                                                                               # creating an empty list to store chunks
  for segment in result["segments"]:                                                        # since we have segments in result, iterating through each segment
     chunks.append({ "number" :number, "title": title, "start": segment["start"],
                     "end": segment["end"],"text" : segment["text"] })                      # appending chunk with metadata to the list

  chunksWithMetadata = {"chunks" : chunks, "text" : result["text"]}                         # creating a dictionary with chunks and full text


  with open(f"audio_jsons/{audio}.json", "w") as f:                                         # writing the chunks with metadata to a JSON file
      json.dump(chunksWithMetadata, f)                                                      # dumping the dictionary to the JSON file

print("Completed")
