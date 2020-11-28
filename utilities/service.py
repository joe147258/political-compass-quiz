from utilities import json_parser

def add_question(text, type, sway):
    dict = {
        "question_text":text,
        "type":type,
        "sway":sway
    }
    json_parser.append_question(dict)

    return 0

def delete_question(pos):
    new_list = json_parser.question_data()['question_list']
    new_list.pop(pos)
    json_parser.replace_question_list(new_list)

def question_info(pos):
    return json_parser.question_data()['question_list'][pos]
