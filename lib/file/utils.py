import os, sys, json
def read_json(file):
    if not os.path.isfile(file):
        raise Exception("Not file Found on the system: %s"%file)
    with open(file) as f:
        d = json.load(f)
        return d

def save_json(file_path,json_data):
    json.dump(json_data,file_path)
    return True


def execute_command(command, wait = False):
    # TODO timeout, logger, return response
    import subprocess
    if wait:
        subprocess.call(command)
    else:
        subprocess.Popen(command)