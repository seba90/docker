def get_uri_name(uri):
    return str(uri.decode().split('#')[1])


def get_task_type_from_uri(uri):
    return str(get_uri_name(uri).split('_')[0])


def str2bool(v):
    return v.lower() in ("true")