from model.logged_task import LoggedTask, URI_TASK_PREVIOUS_ACTION, URI_TASK_NEXT_ACTION, URI_TASK_SUB_ACTION, \
    URI_TASK_SUB_MOTION, URI_TASK_SUB_EVENT
from controller.utils import get_uri_name


class Visualizer:
    def __init__(self, task_dict):
        self.task_dict = task_dict

    def get_start_nodes(self):
        start_node_list = []

        for potential_start_node_name in self.task_dict.keys():
            is_sub_action = False

            for node_name in self.task_dict.keys():
                if (self.task_dict[node_name].get(URI_TASK_SUB_ACTION) \
                        and potential_start_node_name in self.task_dict[node_name][URI_TASK_SUB_ACTION])\
                    or (self.task_dict[node_name].get(URI_TASK_SUB_MOTION) \
                        and potential_start_node_name in self.task_dict[node_name][URI_TASK_SUB_MOTION])\
                    or (self.task_dict[node_name].get(URI_TASK_SUB_EVENT) \
                        and potential_start_node_name in self.task_dict[node_name][URI_TASK_SUB_EVENT]):
                    is_sub_action = True
                    break

            if not is_sub_action:
                start_node_list.append(
                    LoggedTask(potential_start_node_name,
                               self.task_dict[potential_start_node_name])
                )

        return sorted(start_node_list, key=lambda k: k.start_time.time)

    def traverse_task_tree(self, logged_task):
        first_action = ''
        action_list = []
        children_list = []
        merged_sub_lists = logged_task.sub_action_list.union(logged_task.sub_event_list).union(logged_task.sub_motion_list)

        if not merged_sub_lists:
            return {'name': get_uri_name(logged_task.logged_task_uri),
                    'successful': str(logged_task.task_success).capitalize(),
                    'startTime': str(logged_task.start_time),
                    'endTime': str(logged_task.end_time)
                    }

        for sub_action_uri in merged_sub_lists:
            #Find the the task which doesnt have a previous task
            if URI_TASK_PREVIOUS_ACTION not in self.task_dict[sub_action_uri]:
                first_action = sub_action_uri
                break

        action_list.append(first_action)
        temp_action = first_action

        while temp_action:
            if self.task_dict[temp_action].get(URI_TASK_NEXT_ACTION):
                action_list.append(self.task_dict[temp_action][URI_TASK_NEXT_ACTION])
                temp_action = self.task_dict[temp_action][URI_TASK_NEXT_ACTION]
            else:
                temp_action = ''

        for action in action_list:
            child_logged_task = LoggedTask(action, self.task_dict[action])
            children_list.append(self.traverse_task_tree(child_logged_task))

        return {'name': get_uri_name(logged_task.logged_task_uri),
                '_children': children_list,
                'successful': str(logged_task.task_success).capitalize(),
                'startTime': str(logged_task.start_time),
                'endTime': str(logged_task.end_time)
                }

    def transform_task_dict_to_d3_json(self):
        start_node_list = self.get_start_nodes()
        children_list = []

        for start_node in start_node_list:
            children_list.append(self.traverse_task_tree(start_node))

        return {'name': 'Experiment',
                '_children': children_list,
                'successful': 'True'
                }

    def transform_co_occurrence_dict_to_d3_json(self, co_occurrence_task_and_reasoning_task, first_group, second_group):
        nodes_list = []
        links_list = []
        index_counter = -1
        node_name_index_dict = {}

        for task_type in co_occurrence_task_and_reasoning_task.keys():
            index_counter += 1
            node_name_index_dict[task_type] = index_counter
            task_type_index = index_counter
            nodes_list.append({"group": first_group, "index": task_type_index, "name": str(task_type)})
            for reasoning_task_type in co_occurrence_task_and_reasoning_task[task_type]:
                num_reasoning_tasks = co_occurrence_task_and_reasoning_task[task_type][reasoning_task_type]

                if node_name_index_dict.get(reasoning_task_type) is None:
                    index_counter += 1
                    node_name_index_dict[reasoning_task_type] = index_counter
                    reasoning_task_index = index_counter
                    nodes_list.append({"group": second_group,
                                       "index": reasoning_task_index,
                                       "name": str(reasoning_task_type)})
                else:
                    reasoning_task_index = node_name_index_dict.get(reasoning_task_type)

                links_list.append({"source": task_type_index,
                                   "target": reasoning_task_index,
                                   "value": float(num_reasoning_tasks)})

        return {"nodes": nodes_list, "links": links_list}

