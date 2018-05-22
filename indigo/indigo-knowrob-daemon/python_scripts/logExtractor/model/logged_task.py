import rdflib
from constants import URI_PREFIX
from model.timepoint import Timepoint

URI_START_TIME = rdflib.URIRef(URI_PREFIX + 'startTime')
URI_END_TIME = rdflib.URIRef(URI_PREFIX + 'endTime')
URI_TASK_SUCCESS = rdflib.URIRef(URI_PREFIX + 'taskSuccess')
URI_TASK_CONTEXT = rdflib.URIRef(URI_PREFIX + 'taskContext')
URI_TASK_PREVIOUS_ACTION = rdflib.URIRef(URI_PREFIX + 'previousAction')
URI_TASK_NEXT_ACTION = rdflib.URIRef(URI_PREFIX + 'nextAction')
URI_TASK_SUB_ACTION = rdflib.URIRef(URI_PREFIX + 'subAction')
URI_TASK_REASONING_TASK = rdflib.URIRef(URI_PREFIX + 'reasoningTask')
URI_TASK_SUB_MOTION = rdflib.URIRef(URI_PREFIX + 'subMotion')
URI_TASK_SUB_EVENT = rdflib.URIRef(URI_PREFIX + 'subEvent')
URI_TASK_FAILURE = rdflib.URIRef(URI_PREFIX + 'failure')


class LoggedTask:
    def __init__(self, logged_task_uri, property_dict):
        self.logged_task_uri = logged_task_uri
        self.start_time = Timepoint(property_dict[URI_START_TIME])
        self.end_time = Timepoint(property_dict[URI_END_TIME])
        self.task_success = property_dict.get(URI_TASK_SUCCESS, "True")
        self.task_context = property_dict.get(URI_TASK_CONTEXT)
        self.previous_action = property_dict.get(URI_TASK_PREVIOUS_ACTION, '')
        self.next_action = property_dict.get(URI_TASK_NEXT_ACTION, '')
        self.sub_action_list = property_dict.get(URI_TASK_SUB_ACTION, set())
        self.sub_event_list = property_dict.get(URI_TASK_SUB_EVENT, set())
        self.sub_motion_list = property_dict.get(URI_TASK_SUB_MOTION, set())
        self.reasoning_task_list = property_dict.get(URI_TASK_REASONING_TASK, set())

    def __str__(self):
        return 'TASK URI: {}\n' \
               'PREVIOUS TASK URI: {}\n' \
               'NEXT TASK URI: {}\n' \
               'SUB TASK URI LIST: {}\n' \
               'START TIME: {}\n' \
               'END TIME: {}\n' \
               'TASK SUCCESS: {}\n' \
               'TASK CONTEXT: {}\n'.format(self.logged_task_uri,
                                           self.previous_action,
                                           self.next_action,
                                           self.sub_action_list,
                                           self.start_time,
                                           self.end_time,
                                           self.task_success,
                                           self.task_context)
