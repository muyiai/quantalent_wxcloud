import json

from flask import Response
from wxcloudrun.model import Questions
from wxcloudrun.dao import get_question_num_with_company

def get_company_name(key_name):
    company_map = {
        "belvedere": "Belvedere Capital",
        "citadel": "Citadel",
        "goldman_sachs": "Goldman Sachs",
        "hrt": "Hudson River Trading",
        "imc": "IMC Trading",
        "squarepoint": "Squarepoint",
        "worldquant": "WorldQuant",
        "transmarket": "Trans Market Group",
        "akuna": "Akuna Capital",
        "drw": "DRW Holdings",
        "five_rings": "Five Rings",
        "jane_street": "Jane Street",
        "oldmission": "Old Mission",
        "optiver": "Optiver",
        "sig": "SIG",
        "two_sigma": "Two Sigma",
    }
    if key_name in company_map:
        return company_map[key_name]
    return key_name


def make_succ_empty_response():
    data = json.dumps({'code': 0, 'data': {}})
    return Response(data, mimetype='application/json')


def make_succ_response(data):
    data = json.dumps({'code': 200, 'data': data})
    return Response(data, mimetype='application/json')


def make_succ_companies_response(data):
    data_res = []
    if isinstance(data, list):
        for item in data:
            tmp = {}
            tmp['id'] = item.id
            tmp['name'] = get_company_name(item.name)
            tmp['image'] = item.image_url
            tmp['question_count'] = get_question_num_with_company(item.name)
            data_res.append(tmp)
    return Response(
        json.dumps({'code': 200, 'message': 'success', 'data': data_res}),
        mimetype='application/json')


def make_succ_questions_response(data, page, page_size):
    data_res = {
        "list": [],
        "total": len(data),
        "page": page,
        "page_size": page_size,
    }
    if page_size == 0:
        return make_err_response('page_size is out of range')
    page_num = len(data) // page_size + 1
    if page > page_num:
        return make_err_response('page is out of range')
    if page < 1:
        return make_err_response('page is out of range')
    if page_size < 1:
        return make_err_response('page_size is out of range')
    if isinstance(data, list):
        for item in data[page_size * (page - 1):page_size * page]:
            tmp = {}
            tmp['id'] = item.id
            tmp['title'] = item.title
            tmp['difficulty'] = item.level
            tmp['tags'] = item.tags
            data_res["list"].append(tmp)
    else:
        return make_err_response('data is not a list')
    return Response(
        json.dumps({'code': 200, 'message': 'success', 'data': data_res}),
        mimetype='application/json')


def make_succ_question_detail_response(data):
    data_res = {}
    if isinstance(data, Questions):
        data_res['id'] = data.id
        data_res['company_name'] = data.company_name
        data_res['title'] = data.title
        data_res['level'] = data.level
        data_res['tags'] = data.tags
        data_res['firms'] = data.firms
        data_res['content'] = data.content
        data_res['solution'] = data.solution
        data_res['answer'] = data.answer
        data_res['hint'] = data.hint
    else:
        return make_err_response('data is not a Question')
    data = json.dumps({'code': 200, 'message': 'success', 'data': data_res})
    return Response(data, mimetype='application/json')


def make_err_response(err_msg):
    data = json.dumps({'code': -1, 'message': err_msg})
    return Response(data, mimetype='application/json')
