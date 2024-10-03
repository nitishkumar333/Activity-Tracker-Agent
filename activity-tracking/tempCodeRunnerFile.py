self.stop_event.set()
        if self.activity_thread is not None:
            self.activity_thread.join()
            self.activity_thread = None  # Clear reference after stopping
        
        if self.activity_Pop_thread is not None:
            self.activity_Pop_thread = None 