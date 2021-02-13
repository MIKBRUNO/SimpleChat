import json
"""
all messages are dictionaries converted to JSON format
"""


def write_json(dct: dict) -> str:
    """
    :param dct: dict formatted
    :return:
    """
    msg = json.dumps(dct)
    return msg


def read_json(msg: str) -> dict:
    """
    :param msg: json string
    :return: dict from json string
    """
    return json.loads(msg)


def message_process(msg: str, handler: staticmethod, read_thread) -> None:
    """
    :param read_thread: is a ReadThread instance for handler
    :param msg: decoded bytes read from connection recv
    :param handler: function that do anything with its params: handler(sender:str, flags:dict, text:str)
    :return: None
    """
    flags = read_json(msg)
    handler(flags, read_thread)
