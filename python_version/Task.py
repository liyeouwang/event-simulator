class Task:
    def __init__(self, name="", duration=1, have_done=0, 
                priority=0, request_time=0, detail="No task description"):
        self.name = name # Ex: Video streaming, AI computing
        self.detail = detail
        self.duration = duration
        self.have_done = have_done
        self.priority = priority

        self.request_time = request_time
        self.delivery_time = -1
        return
    
    def __str__(self):
        return self.name #+ ": " + self.detail

    def just_do_it(self, amount):
        # stupid method name
        self.have_done += amount
        return
    
    def is_done(self):
        return (self.duration - self.have_done) <= 0


    def estimated_needed_time(self):
        # can be not precise
        return self.duration - self.have_done

    def deliver(self, time):
        self.delivery_time = time
        return

    def is_delivered(self):
        return self.delivery_time > 0

    def get_waiting_time(self):
        return  self.delivery_time - self.request_time
