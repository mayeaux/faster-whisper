from flask import Flask, request, jsonify
from faster_whisper import WhisperModel
import time
import os

app = Flask(__name__)

# Load the model
start_model_load_time = time.time()
model = WhisperModel("tiny.en", device="cpu", compute_type="float32")
finish_model_load_time = time.time()
model_load_elapsed_time = finish_model_load_time - start_model_load_time
print("Model loaded in:", model_load_elapsed_time, "seconds")

def get_file_path(route):
    # Construct the full path to the file
    file_path = os.path.expanduser(f'~/Development/whisper-frontend/public/{route}')

    # Check if the file exists
    if os.path.isfile(file_path):
        return file_path
    else:
        return None

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Get the route from the request
    route = request.json.get('route')

    file_path = get_file_path(route)

    if file_path is None:
        return jsonify({'error': f"File {route} does not exist in ~/Development/whisper-frontend/public/"}), 400

    print(file_path)

    # Transcribe the audio
    start_time = time.time()
    segments, info = model.transcribe(file_path, word_timestamps=True)

    # list(segments) is what actually completes it, somehow
    segments = list(segments)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Transcription completed in:", elapsed_time, "seconds")

    # Convert the segments to JSON
    words_data = []
    for segment in segments:
        for word in segment.words:
            word_info = {
                "start": word.start,
                "end": word.end,
                "word": word.word
            }
            words_data.append(word_info)

    # Extract the 'word' field from each dictionary and join them into a single string
    long_string = ''.join([word_info['word'] for word_info in words_data])

    print(long_string)
    # Return the transcribed audio as JSON
    return jsonify(words_data)

if __name__ == '__main__':
    app.run(port=5000)
