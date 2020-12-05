from utilities import service, json_manager, universal_constants as const
from threading import Thread
from time import sleep

undo_queue = list()
redo_queue = list()

def cache_action(cache_type, pos):
    dict = service.question_info(pos)
    cache_dict = {
        "cache_type": cache_type,
        "question": dict['question_text'],
        "question_type": dict['type'],
        "sway": dict['sway'],
        "pos": pos
    }
    if(len(undo_queue) < const.CACHE_QUEUE_MAX_SIZE):
        undo_queue.append(cache_dict)
    else:
        undo_queue.pop(0)
        undo_queue.append(cache_dict)

def cache_redo(data):
    if(len(redo_queue) < const.CACHE_QUEUE_MAX_SIZE):
        redo_queue.append(data)
    else:
        redo_queue.pop(0)
        redo_queue.append(data)

def cache_undo(data):
    if(len(undo_queue) < const.CACHE_QUEUE_MAX_SIZE):
        undo_queue.append(data)
    else:
        undo_queue.pop(0)
        undo_queue.append(data)

def restore_redo():
    if len(redo_queue) == 0:
        raise Exception("No Cache")

    data = undo_queue.pop()
    if data['cache_type'] == const.DELETE_CONST:
        print("test")

def restore_undo():
    if len(undo_queue) == 0:
        raise Exception("No Cache")

    data = undo_queue.pop()
    question_list = json_manager.question_list()
    restored_question = {
            'question_text': data['question'],
            'type': data['question_type'],
            'sway': data['sway']
        }

    if data['cache_type'] == const.DELETE_CONST:
        new_question_list = question_list[0:data['pos']]
        new_question_list.append(restored_question)
        new_question_list = new_question_list + question_list[data['pos']:len(question_list)]
        json_manager.replace_question_list(new_question_list)
    elif data['cache_type'] == const.EDIT_CONST:
        question_list[data['pos']] = restored_question
        json_manager.replace_question_list(question_list)
    else:
        raise Exception("Cache Error.")

