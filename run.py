from faster_whisper import WhisperModel
import time
import json
import sys
from writers import get_writer
from progressTracker import DurationProgressTracker
import os
from languages import LANGUAGES
from utils import *
from flask import Flask, request, jsonify
from threading import Thread
from typing import Any


app = Flask(__name__)

start_model_load_time = time.time()

model = WhisperModel("tiny", device="cpu", compute_type="float32")

finish_model_load_time = time.time()

model_load_elapsed_time = finish_model_load_time - start_model_load_time

# Print start, end, and elapsed time
print("Start Time:", start_model_load_time)
print("End Time:", finish_model_load_time)
print("Elapsed Time (in seconds):", model_load_elapsed_time)

# Retrieve the audio path from the command line arguments

# Retrieve the audio path from the command line arguments

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    # Extract uniqueNumber from the request
    # For simplicity, this example assumes the client sends a JSON with 'uniqueNumber'
    data = request.get_json()

    # Get the route from the request
    # route = request.json.get('route')

    # Log: backend just got hit with uniqueNumber: 635294790577
    print(f'backend just got hit with uniqueNumber: {data.get("uniqueNumber", "635294790577")}')

    # Extract the uniqueNumber from the JSON
    uniqueNumber = data.get('uniqueNumber', "635294790577")

    thread = Thread(target=transcribeBasedOnUniqueNumber, args=(uniqueNumber,))
    thread.start()
    # transcribeBasedOnUniqueNumber(uniqueNumber)

    return jsonify({'status': 'processing'}), 200


def transcribeBasedOnUniqueNumber(uniqueNumber: str) -> Any:
    audioPath = os.path.expanduser(f'~/generate-subtitles-server/api-transcriptions/{uniqueNumber}/{uniqueNumber}')

    segments, info = model.transcribe(audioPath, word_timestamps=True)

    language_name = LANGUAGES[info.language].title()

    # print language name like Language Name: English
    print(f"Language Name: {language_name}")

    audioPath = uniqueNumber

    # language_name = LANGUAGES[info.language].title()
    print(
        "Detected language '%s' with probability %f"
        % (info.language, info.language_probability)
    )

    verbose = False

    list_segments = []
    all_text = ""
    duration = info.duration

    tracker = DurationProgressTracker(duration)

    uniqueNumber = audioPath
    processingJsonPath = os.path.expanduser(
        f'~/generate-subtitles-server/api-transcriptions/{uniqueNumber}/processing_data.json')

    # read json
    with open(processingJsonPath) as f:
        data = json.load(f)

    # get the

    print('duration')
    print(duration)
    data['status'] = 'processing'
    data['language'] = language_name
    data['languageCode'] = info.language

    # setup formattedProgress
    data['formattedProgress'] = {
        "percentDoneAsNumber": 0,
        "timeElapsed": "0s",
        "timeRemaining": "?",
        "speed": "?",
    }

    # Write the modified data back to the JSON file
    with open(processingJsonPath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    # return sys.exit(0)

    for segment in segments:
        start, end, text = segment.start, segment.end, segment.text
        segment_duration = segment.end - segment.start

        # Update the tracker with the duration of the current segment
        progress_info = tracker.update(segment.start, segment.end)

        # Update the 'formattedProgress' section with the new data from your tracker
        # This assumes you have a method in your tracker to get the formatted progress info as shown earlier
        # If not, you would manually construct the dictionary based on the tracker's attributes
        data['formattedProgress'] = progress_info
        data['progress'] = progress_info['percentDoneAsNumber']

        with open(processingJsonPath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        # Print the progress info
        print(progress_info)

        print(start)
        print(end)
        print(text)
        # print segment duration like : Segment Duration: 0.00s
        print(f"Segment Duration: {segment_duration:.2f}s")

        all_text += text

        segment_dict = segment._asdict()
        if segment.words:
            segment_dict["words"] = [word._asdict() for word in segment.words]

        list_segments.append(segment_dict)

    result = dict(
        text=all_text,
        segments=list_segments,
        language=info.language,
    )

    print(all_text)
    print(list(list_segments))
    # print(language)

    # output folder
    outputDirectory = os.path.expanduser(f'~/generate-subtitles-server/api-transcriptions/{uniqueNumber}')

    # outputDirectory = '~/Development/whisper-frontend/api-transcriptions/487794891020'

    # expand it
    outputDirectory = os.path.expanduser(outputDirectory)

    writer = get_writer('all', outputDirectory)
    writer(result, audioPath)

    # mark status as 'transcribed'
    data['status'] = 'transcribed'

    # Write the modified data back to the JSON file
    with open(processingJsonPath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    app.run(port=5000)
