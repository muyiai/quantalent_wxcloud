from flask import render_template, request, jsonify
from run import app
from wxcloudrun.dao import (
    query_questionbyid,
    insert_question,
    get_questionsbylevel,
    get_company_list,
    get_company_by_id
)
from wxcloudrun.model import Questions
from wxcloudrun.response import make_succ_response, make_err_response, make_succ_questions_response, make_succ_companies_response, make_succ_question_detail_response


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/health')
def health():
    """
    健康检查端点
    :return: 返回健康状态
    """
    return jsonify({"status": "ok", "message": "service is running"}), 200


@app.route('/api/add_questions', methods=['POST'])
def add_question():
    """
    :return:添加面试题结果
    """

    # 获取请求体参数
    params = request.get_json() if request.get_json() else request.form.to_dict()
    question = Questions()
    question.company_name = params['company_name']
    question.title = params['title']
    question.content = params['content']
    question.solution = params['solution']
    question.answer = params['answer']
    question.level = params['level']
    question.hint = params['hint']
    question.tags = params['tags']
    question.firms = params['firms']
    insert_question(question)
    return make_succ_response(question.id)


@app.route('/api/questions', methods=['GET'])
def get_questions():
    """
    :return: 面试题列表
    """
    company_id = request.args.get('company_id')
    level = request.args.get('difficulty', None)
    tag = request.args.get('tag', None)
    page = request.args.get('page', 1)
    page_size = request.args.get('page_size', 10)
    company_name = get_company_by_id(company_id)
    if company_name is None:
        return make_err_response('Company not found')
    questions = get_questionsbylevel(company_name, level, tag)
    return make_succ_questions_response(
        questions, int(page), int(page_size))


@app.route('/api/question_detail', methods=['GET'])
def get_question_detail():
    """
    :return: 面试题详情
    """
    question_id = request.args.get('question_id')
    question = query_questionbyid(question_id)
    if question is None:
        return make_err_response('Question not found')
    return make_succ_question_detail_response(question)


@app.route('/api/companies', methods=['GET'])
def get_all_companies():
    """
    :return: 所有公司列表
    """
    companies = get_company_list()
    if companies is None:
        return make_err_response('No companies found')
    return make_succ_companies_response(companies)