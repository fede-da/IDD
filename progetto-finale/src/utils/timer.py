import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = None

    def start(self):
        if self.start_time is not None:
            print("Timer is already running!")
        else:
            self.start_time = time.time()
            print("Timer started.")

    def stop(self):
        if self.start_time is None:
            print("Timer is not running. Please start the timer first.")
        else:
            self.elapsed_time = time.time() - self.start_time
            print(f"Timer stopped. Total time: {self.elapsed_time:.2f} seconds.")
            self.start_time = None

    def get_elapsed_time(self):
        return self.elapsed_time
