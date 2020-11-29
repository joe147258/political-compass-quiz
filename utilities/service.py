from utilities import json_parser

def add_question(form_items):
    dict = {
        "question_text":form_items['question_text'],
        "type":form_items['type'],
        "sway":form_items['sway']
    }
    json_parser.append_question(dict)

    return 0

def delete_question(pos):
    new_list = json_parser.question_data()['question_list']
    new_list.pop(pos)
    json_parser.replace_question_list(new_list)

def question_info(pos):
    return json_parser.question_data()['question_list'][pos]

def edit_question(form_items):
    pos = int(form_items['pos'])
    new_list = json_parser.question_data()['question_list']
    new_list[pos]['question_text'] = form_items['question_text']
    new_list[pos]['type'] = form_items['type']
    new_list[pos]['sway'] = form_items['sway']
    json_parser.replace_question_list(new_list)
