import ontospy
from collections import defaultdict
import sys

from model.logged_task import URI_START_TIME, URI_TASK_SUB_ACTION, URI_TASK_REASONING_TASK, URI_TASK_SUB_MOTION, \
    URI_TASK_SUB_EVENT
from model.logged_reasoning_task import URI_PREDICATE
from controller.visualizer import Visualizer
import json


def parse_experiment(ontology, save_path):
    entities_dict = defaultdict(lambda: defaultdict(set))
    print "Loading all triplets ..."
    triplet_list = get_all_triplets(ontology)
    print "All triplets are loaded. Number is {}".format(len(triplet_list))
    task_dict = {}
    reasoning_task = {}
    object_dict = {}

    print "Processing all triplets to required data structure..."
    for triplet in triplet_list:
        x, y, z = triplet

        if URI_TASK_SUB_ACTION == y \
                or URI_TASK_REASONING_TASK == y or URI_TASK_SUB_MOTION == y or URI_TASK_SUB_EVENT == y:
                entities_dict[x][y].add(z)
        else:
            entities_dict[x][y] = z

    for entity_key in entities_dict.keys():
        property_dict = entities_dict[entity_key]
        if property_dict.get(URI_PREDICATE):
            reasoning_task[entity_key] = property_dict
        elif property_dict.get(URI_START_TIME):
            task_dict[entity_key] = property_dict
        else:
            object_dict[entity_key] = property_dict

    print "DONE"

    visualizer = Visualizer(task_dict)

    print "Converting task tree to json file ..."
    with open('{}/flare.json'.format(save_path), 'w') as outfile:
        json.dump(visualizer.transform_task_dict_to_d3_json(), outfile)
    print "DONE"


def get_all_triplets(ontology):
    return ontology.query('CONSTRUCT { ?x ?y ?z } WHERE { { ?x ?y ?z } }')


def build_triplet_query(x, y="?y", z="?z"):
    if not y.startswith("?"):
        y = "<{}>".format(y)
    if not z.startswith("?"):
        z = "<{}>".format(z)

    query_str = """CONSTRUCT {{ <{0}> {1} {2} }} WHERE {{ {{ <{0}> {1} {2} }} }}""".format(x, y, z)

    return query_str


if __name__ == "__main__":
    path = sys.argv[1]
    save_path = '.'
    if len(sys.argv) > 2:
        save_path = sys.argv[2]
    experiment_log = ontospy.Ontospy(path)
    print "Experiment will be processed"
    parse_experiment(experiment_log,save_path)
    print "Experiment is processed"
