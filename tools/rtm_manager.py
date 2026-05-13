import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RTM_FILE = os.path.join(BASE_DIR, "rtm", "rtm.json")


def load_rtm():
    with open(RTM_FILE, "r") as f:
        return json.load(f)

def get_requirements_for_file(file_path):
    rtm = load_rtm()

    matched = []

    for req_id, data in rtm.items():
        if data["linked_file"] == file_path:
            matched.append((req_id, data))

    return matched


def update_rtm(req_id, coverage, tests_generated, status):
    rtm = load_rtm()

    if req_id in rtm:
        rtm[req_id]["coverage"] = coverage
        rtm[req_id]["tests_generated"] = tests_generated
        rtm[req_id]["status"] = status

    with open(RTM_FILE, "w") as f:
        json.dump(rtm, f, indent=4)
