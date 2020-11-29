from utilities import JsonReadWrite
from utilities import UniversialConstants as const

def add_question(form_items):
    dict = {
        "question_text":form_items['question_text'],
        "type":form_items['type'],
        "sway":form_items['sway']
    }
    JsonReadWrite.append_question(dict)

    return 0

def delete_question(pos):
    new_list = JsonReadWrite.question_data()['question_list']
    new_list.pop(pos)
    JsonReadWrite.replace_question_list(new_list)

def question_info(pos):
    return JsonReadWrite.question_data()['question_list'][pos]

def edit_question(form_items):
    pos = int(form_items['pos'])
    new_list = JsonReadWrite.question_data()['question_list']
    new_list[pos]['question_text'] = form_items['question_text']
    new_list[pos]['type'] = form_items['type']
    new_list[pos]['sway'] = form_items['sway']
    JsonReadWrite.replace_question_list(new_list)

def restore_cached():
    data = JsonReadWrite.get_cache()['cached_action']
    if data['cache_type'] == const.DELETE_CONST:
        question = question_info(data['pos'])
        print(question)
    elif data['cache_type'] == const.EDIT_CONST:
        print ("ya ya")
    else:
        raise Exception("Cache Error.")