class Timepoint:

    def __init__(self, timepoint_uri):
        self.timepoint_uri = timepoint_uri
        self.time = long(str(timepoint_uri.split('#')[1].split('_')[1]))

    def __str__(self):
        return str(self.time)