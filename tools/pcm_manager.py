import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PCM_FILE = os.path.join(BASE_DIR, "pcm", "protocol_context.json")


def load_pcm():
    with open(PCM_FILE, "r") as f:
        return json.load(f)


def get_protocol_context(protocol_name):
    pcm = load_pcm()
    return pcm.get(protocol_name, {})
