import logging
import urllib.parse

from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.model import Questions, Companies

# 初始化日志
logger = logging.getLogger('log')

level_map = {
    "Easy": 1,
    "Medium": 2,
    "Hard": 3,
}


def get_company_by_id(company_id):
    """
    根据ID获取公司
    :param company_id: Companies的ID
    :return: Companies实体
    """
    try:
        company = Companies.query.filter(Companies.id == company_id).first()
        return company.name
    except OperationalError as e:
        logger.info("get_company_by_id errorMsg= {} ".format(e))
        return None, None


def get_company_list():
    """
    获取公司列表
    :return: 公司列表
    """
    try:
        data = Companies.query.all()
        return data
    except OperationalError as e:
        logger.info("get_company_list errorMsg= {} ".format(e))
        return None


def get_question_num_with_company(company_name):
    """
    获取公司对应的面试题数量
    :param company_name: Companies的名称
    :return: 面试题数量
    """
    try:
        return Questions.query.filter(Questions.company_name == company_name).count()
    except OperationalError as e:
        logger.info("get_question_num_with_company errorMsg= {} ".format(e))
        return None


def query_questionbyid(question_id):
    """
    根据ID查询Questions实体
    :param question_id: Questions的ID
    :return: Questions实体
    """
    try:
        return Questions.query.filter(
            Questions.id == int(question_id)).first()
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None


def query_question_statistics():
    """
    查询Questions的统计信息
    :return: Questions的统计信息
    """
    try:
        return Questions.query.count()
    except OperationalError as e:
        logger.info("query_question_statistics errorMsg= {} ".format(e))
        return None


def delete_questionbyid(id):
    """
    根据ID删除Questions实体
    :param id: Questions的ID
    """
    try:
        question = Questions.query.get(id)
        if question is None:
            return
        db.session.delete(question)
        db.session.commit()
    except OperationalError as e:
        logger.info("delete_questionbyid errorMsg= {} ".format(e))


def insert_question(question):
    """
    插入一个Questions实体
    :param question: Questions实体
    """
    try:
        db.session.add(question)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_question errorMsg= {} ".format(e))


def update_questionbyid(question):
    """
    根据ID更新question的值
    :param question实体
    """
    try:
        question = query_questionbyid(question.id)
        if question is None:
            return
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_questionbyid errorMsg= {} ".format(e))


def get_questionsbycompany(company_name):
    """
    根据公司名称查询Questions实体
    :param company_name: Companies的名称
    :return: Questions实体列表
    """
    try:
        return Questions.query.filter(Questions.company_name.like(f'%{company_name}%')).all()
    except OperationalError as e:
        logger.info("get_questionsbycompany errorMsg= {} ".format(e))
        return None


def get_questionsbylevel(company_name, level=None, tags=None):
    """
    根据公司名称查询Questions实体
    :param company_name: Companies的名称
    :param level: 难度等级
    :param tag: 标签
    :return: Questions实体列表
    """
    try:
        if level and tags:
            tags = [urllib.parse.unquote(t) for t in tags.split(',')]
            tag = tags[0]
            levels = [level_map[l.strip()] for l in level.split(',')]
            data = Questions.query.filter(
                Questions.company_name == company_name, 
                Questions.level.in_(levels), 
                Questions.tags.like(f'%{tag}%')  # 'tags' instead of 'tag'
            ).order_by(Questions.id.desc()).all()
        elif level:
            levels = [level_map[l.strip()] for l in level.split(',')]
            data = Questions.query.filter(
                Questions.company_name == company_name, 
                Questions.level.in_(levels)
            ).order_by(Questions.id.desc()).all()
        elif tags:
            tags = [urllib.parse.unquote(t) for t in tags.split(',')]
            tag = tags[0]
            data = Questions.query.filter(
                Questions.company_name == company_name, 
                Questions.tags.like(f'%{tag}%')
            ).order_by(Questions.id.desc()).all()
        else:
            data = Questions.query.filter(
                Questions.company_name == company_name
            ).order_by(Questions.id.desc()).all()
        return data
    except OperationalError as e:
        logger.info("get_questionsbylevel errorMsg= {} ".format(e))
        return None
