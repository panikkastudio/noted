import hashlib
import functools as ft
from typing import List


def set_hashes(task: dict, input_keys: List[str] = None):
    if input_keys is None:
        input_keys = ["text"]

    initial_key = input_keys.pop(0)
    reducer_fn = lambda left, right: left + ";" + task.get(right, "")
    hash_value = ft.reduce(reducer_fn, input_keys, task.get(initial_key, ""))
    hash_dig = hashlib.sha1(hash_value.encode("utf-8")).hexdigest()

    task["task_hash"] = hash_dig
    return task
