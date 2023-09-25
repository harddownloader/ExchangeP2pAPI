"""
https://stackoverflow.com/a/20725965
"""
import json


def is_json(json_str):
    try:
        json.loads(json_str)
    except ValueError as e:
        return False
    return True
