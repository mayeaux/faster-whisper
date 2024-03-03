from faster_whisper import WhisperModel
import time
import json

start_model_load_time = time.time()

model = WhisperModel("small.en", device="cpu", compute_type="float32")

finish_model_load_time = time.time()

model_load_elapsed_time = finish_model_load_time - start_model_load_time

# Print start, end, and elapsed time
print("Start Time:", start_model_load_time)
print("End Time:", finish_model_load_time)
print("Elapsed Time (in seconds):", model_load_elapsed_time)

segments, info = model.transcribe("english.mp4", word_timestamps=True)


# Record the start time
start_time = time.time()

segments = list(segments)

# print(segments)
end_time = time.time()

elapsed_time = end_time - start_time

# Print start, end, and elapsed time
print("Start Time:", start_time)
print("End Time:", end_time)
print("Elapsed Time (in seconds):", elapsed_time)



for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

words_data = []
for segment in segments:
    for word in segment.words:
        word_info = {
            "start": word.start,
            "end": word.end,
            "word": word.word
        }
        words_data.append(word_info)


# Convert to JSON
words_json = json.dumps(words_data, indent=4)




# Print JSON string
# print(words_json)

