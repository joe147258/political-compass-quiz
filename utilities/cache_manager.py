from utilities import service, json_manager, universal_constants as const
from threading import Thread
from time import sleep

cache_queue = list()

# Recall determines if the thread is calling itself twice
# This prevents it being stop in a loop.
def cache_action(cache_type, pos):
    dict = service.question_info(pos)
    cache_dict = {
        "cache_type": cache_type,
        "question": dict['question_text'],
        "question_type": dict['type'],
        "sway": dict['sway'],
        "pos": pos
    }
    if(len(cache_queue) < const.CACHE_QUEUE_MAX_SIZE):
        cache_queue.append(cache_dict)
    else:
        cache_queue.pop(0)
        cache_queue.append(cache_dict)

def restore_last():
    if len(cache_queue) == 0:
        raise Exception("No Cache")
    data = cache_queue.pop()
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

