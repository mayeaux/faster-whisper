from faster_whisper import WhisperModel
import time
import json
import sys
from writers import get_writer
from progressTracker import DurationProgressTracker
import os

start_model_load_time = time.time()

model = WhisperModel("small.en", device="cpu", compute_type="float32")

finish_model_load_time = time.time()

model_load_elapsed_time = finish_model_load_time - start_model_load_time

# Print start, end, and elapsed time
print("Start Time:", start_model_load_time)
print("End Time:", finish_model_load_time)
print("Elapsed Time (in seconds):", model_load_elapsed_time)

audioPath = "487794891020"

segments, info = model.transcribe(audioPath, word_timestamps=True)


# language_name = LANGUAGES[info.language].title()
print(
    "Detected language '%s' with probability %f"
    % (info.language, info.language_probability)
)

verbose = False

class Options:
    def __init__(self, print_colors=False, beam_size=5, best_of=5, patience=1):
        self.print_colors = print_colors
        self.beam_size = beam_size
        self.best_of = best_of
        self.patience = patience
        # Add more attributes as needed

# Create an options object with default settings
options = Options()

# Now you can set attributes
options.print_colors = False

def format_timestamp(
    seconds: float, always_include_hours: bool = False, decimal_marker: str = "."
):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
    return (
        f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"
    )


system_encoding = sys.getdefaultencoding()

if system_encoding != "utf-8":

    def make_safe(string):
        return string.encode(system_encoding, errors="replace").decode(system_encoding)

def get_colored_text(words):
    k_colors = [
        "\033[38;5;196m",
        "\033[38;5;202m",
        "\033[38;5;208m",
        "\033[38;5;214m",
        "\033[38;5;220m",
        "\033[38;5;226m",
        "\033[38;5;190m",
        "\033[38;5;154m",
        "\033[38;5;118m",
        "\033[38;5;82m",
    ]

    text_words = ""

    n_colors = len(k_colors)
    for word in words:
        p = word.probability
        col = max(0, min(n_colors - 1, (int)(pow(p, 3) * n_colors)))
        end_mark = "\033[0m"
        text_words += f"{k_colors[col]}{word.word}{end_mark}"

    return text_words

list_segments = []
all_text = ""
duration = info.duration

tracker = DurationProgressTracker(duration)

print('duration')
print(duration)
for segment in segments:
    start, end, text = segment.start, segment.end, segment.text
    segment_duration = segment.end - segment.start

    # Update the tracker with the duration of the current segment
    progress_info = tracker.update(segment.start, segment.end)
    # Print the progress info
    print(progress_info)

    print(start)
    print(end)
    print(text)
    # print segment duration like : Segment Duration: 0.00s
    print(f"Segment Duration: {segment_duration:.2f}s")


    all_text += text

    # Print the segment
    if verbose or options.print_colors:
        if options.print_colors and segment.words:
            text = get_colored_text(segment.words)
        else:
            text = segment.text

        line = f"[{format_timestamp(start)} --> {format_timestamp(end)}] {text}"
        print(make_safe(line))

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
outputDirectory = '~/Development/whisper-frontend/api-transcriptions/487794891020'

# expand it
outputDirectory = os.path.expanduser(outputDirectory)


writer = get_writer('all', outputDirectory)
writer(result, audioPath)







# Record the start time
# start_time = time.time()
#
# segments = list(segments)
#
# # print(segments)
# end_time = time.time()
#
# elapsed_time = end_time - start_time
#
# # Print start, end, and elapsed time
# print("Start Time:", start_time)
# print("End Time:", end_time)
# print("Elapsed Time (in seconds):", elapsed_time)
#
#
#
# for segment in segments:
#     print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
#
# words_data = []
# for segment in segments:
#     for word in segment.words:
#         word_info = {
#             "start": word.start,
#             "end": word.end,
#             "word": word.word
#         }
#         words_data.append(word_info)
#
#
# # Convert to JSON
# words_json = json.dumps(words_data, indent=4)




# Print JSON string
# print(words_json)

