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
        question_list = JsonReadWrite.question_list()
        new_question_list = question_list[0:data['pos']]
        restored_question = {
            'question_text': data['question'],
            'type': data['question_type'],
            'sway': data['sway']
        }
        new_question_list.append(restored_question)
        new_question_list = new_question_list + question_list[data['pos']:len(question_list)]
        JsonReadWrite.replace_question_list(new_question_list)
    elif data['cache_type'] == const.EDIT_CONST:
        question = question_info(data['pos'])
        print(question)
    else:
        raise Exception("Cache Error.")

    JsonReadWrite.clear_cache()