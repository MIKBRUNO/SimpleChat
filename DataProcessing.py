"""
all messages are dictionaries
"""

import json


def write_json(dct):
    msg = json.dumps(dct)
    return msg


def read_json(msg):
    return json.loads(msg)


def message_process(msg, handler, read_thread):
    """
    :param read_thread: is a ReadThread instance for handler
    :param msg: decoded bytes were read from connection recv
    :param handler: function that do anything with its params: handler(sender:str, flags:dict, text:str)
    :return: None
    """
    flags = read_json(msg)
    handler(flags, read_thread)
