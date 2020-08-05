class Task:
    def __init__(self, name="", duration=1, have_done=0, detail="No task description"):
        self.name = name # Ex: Video streaming, AI computing
        self.detail = detail
        self.duration = duration
        self.have_done = have_done
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