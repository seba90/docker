from collections import defaultdict
from controller.utils import str2bool
import pandas as pd

from controller.utils import get_task_type_from_uri
from model.logged_task import URI_TASK_REASONING_TASK, URI_TASK_FAILURE
from model.logged_reasoning_task import URI_PREDICATE


class StatsCreator:
    def __init__(self):
        self.task_information_dict = {}
        self.co_occurrence_task_and_reasoning_task = defaultdict(lambda: defaultdict(int))
        self.co_occurrence_task_and_failure = defaultdict(lambda: defaultdict(int))

    def determine_co_occurrence_task_and_reasoning_task(self, task_dict, reasoning_dict):
        for task_uri in task_dict.keys():
            if task_dict[task_uri].get(URI_TASK_REASONING_TASK):
                for reasoning_task_uri in task_dict[task_uri][URI_TASK_REASONING_TASK]:
                    predicate_name = reasoning_dict[reasoning_task_uri][URI_PREDICATE]
                    self.co_occurrence_task_and_reasoning_task[get_task_type_from_uri(task_uri)][predicate_name] += 1

    def determine_co_occurrence_task_and_failure(self, task_dict):
        for task_uri in task_dict.keys():
            if task_dict[task_uri].get(URI_TASK_FAILURE):
                failure_name = task_dict[task_uri].get(URI_TASK_FAILURE)
                self.co_occurrence_task_and_failure[get_task_type_from_uri(task_uri)][failure_name] += 1

    def update_stats(self, logged_task):
        task_type = get_task_type_from_uri(logged_task.logged_task_uri)

        if self.task_information_dict.get(task_type):
            self.task_information_dict[task_type][0] += 1
        else:
            self.task_information_dict[task_type] = [1, 0]

        if logged_task.task_success is not None and str2bool(logged_task.task_success):
            self.task_information_dict[task_type][1] += 1

    def get_data_frame(self):
        return pd.DataFrame(data=self.task_information_dict)

    def get_task_success_rate(self):
        df = self.get_data_frame()
        return df.iloc[[1]].div(df.iloc[0], axis='columns')