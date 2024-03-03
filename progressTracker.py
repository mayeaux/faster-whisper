import time

class DurationProgressTracker:
    def __init__(self, total_duration):
        self.total_duration = total_duration
        self.processed_duration = 0
        self.start_time = time.time()

    def update(self, segment_duration):
        self.processed_duration += segment_duration
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        percent_done = (self.processed_duration / self.total_duration) * 100 if self.total_duration > 0 else 100
        estimated_total_time = (elapsed_time / self.processed_duration) * self.total_duration if self.processed_duration > 0 else 0
        time_remaining = estimated_total_time - elapsed_time

        return {
            "progressBar": self._get_progress_bar(percent_done),
            "percentDone": f"{percent_done:.2f}%",
            "timeElapsed": self._format_time(elapsed_time),
            "speed": f"{elapsed_time / (self.processed_duration if self.processed_duration > 0 else 1):.2f}s",
            "percentDoneAsNumber": percent_done,
            "secondsCompleted": self.processed_duration,
            "secondsTotal": self.total_duration,
            "timeRemaining": {
                "string": self._format_time(time_remaining),
                "hoursRemaining": int(time_remaining // 3600),
                "minutesRemaining": int((time_remaining % 3600) // 60),
                "secondsRemaining": int(time_remaining % 60),
            },
            "progress": self.processed_duration
        }

    def _get_progress_bar(self, percent_done):
        bar_length = 20
        filled_length = int(bar_length * percent_done // 100)
        bar = '█' * filled_length + '▏' * (bar_length - filled_length)
        return bar

    def _format_time(self, seconds):
        return time.strftime("%H:%M:%S", time.gmtime(seconds))
