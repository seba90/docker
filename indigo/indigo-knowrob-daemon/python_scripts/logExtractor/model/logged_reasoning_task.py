import rdflib
from constants import URI_PREFIX
from model.timepoint import Timepoint

URI_START_TIME = rdflib.URIRef(URI_PREFIX + 'startTime')
URI_END_TIME = rdflib.URIRef(URI_PREFIX + 'endTime')
URI_PREDICATE = rdflib.URIRef(URI_PREFIX + 'predicate')
URI_TASK_CONTEXT = rdflib.URIRef(URI_PREFIX + 'taskContext')


class LoggedReasoningTask:
    def __init__(self, logged_reasoning_task_uri, property_dict):
        self.logged_task_uri = logged_reasoning_task_uri
        self.start_time = Timepoint(property_dict[URI_START_TIME])
        self.end_time = Timepoint(property_dict[URI_END_TIME])
        self.predicate = property_dict[URI_PREDICATE]
        self.task_context = property_dict[URI_TASK_CONTEXT]

    def __str__(self):
        return 'TASK URI: {}\n' \
               'START TIME: {}\n' \
               'END TIME: {}\n' \
               'PREDICATE: {}\n' \
               'TASK CONTEXT: {}\n'.format(self.logged_task_uri,
                                           self.start_time,
                                           self.end_time,
                                           self.predicate,
                                           self.task_context)
