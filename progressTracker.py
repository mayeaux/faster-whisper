import time

class DurationProgressTracker:
    def __init__(self, total_duration):
        self.total_duration = total_duration
        self.accumulated_duration = 0.0  # Tracks the accumulated duration processed
        self.last_pos = 0.0  # Tracks the end of the last segment processed
        self.start_time = time.time()

    def update(self, segment_start, segment_end):
        # Calculate the duration since the last segment's end
        duration = segment_end - self.last_pos
        # Update the accumulated duration, ensuring it does not exceed total_duration
        self.accumulated_duration += min(duration, self.total_duration - self.accumulated_duration)
        self.last_pos = segment_end  # Update last_pos to the current segment's end

        current_time = time.time()
        elapsed_time = current_time - self.start_time
        percent_done = (self.accumulated_duration / self.total_duration) * 100

        estimated_total_time = (elapsed_time / self.accumulated_duration) * self.total_duration if self.accumulated_duration > 0 else 0
        time_remaining = max(0, estimated_total_time - elapsed_time)  # Prevent negative time remaining

        return {
            "progressBar": "",
            "percentDone": f"{percent_done:.2f}%",
            "timeElapsed": self._format_time(elapsed_time),
            "speed": f"{elapsed_time / max(1, self.accumulated_duration):.2f}s",
            "percentDoneAsNumber": round(percent_done),
            "secondsCompleted": self.accumulated_duration,
            "secondsTotal": self.total_duration,
            "timeRemaining": {
                "string": self._format_time(time_remaining),
                "hoursRemaining": int(time_remaining // 3600),
                "minutesRemaining": int((time_remaining % 3600) // 60),
                "secondsRemaining": int(time_remaining % 60),
            },
            "progress": self.accumulated_duration
        }

    # _get_progress_bar and _format_time methods remain the same
    def _get_progress_bar(self, percent_done):
        bar_length = 20
        filled_length = int(bar_length * percent_done // 100)
        bar = '█' * filled_length + '▏' * (bar_length - filled_length)
        return bar

    def _format_time(self, seconds):
        return time.strftime("%H:%M:%S", time.gmtime(seconds))
