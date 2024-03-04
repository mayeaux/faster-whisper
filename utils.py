# import sys
import sys

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

system_encoding = sys.getdefaultencoding()

if system_encoding != "utf-8":

    def make_safe(string):
        return string.encode(system_encoding, errors="replace").decode(system_encoding)
