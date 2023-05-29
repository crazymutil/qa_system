from flask import Blueprint, render_template, request, flash, url_for, redirect, jsonify, abort
from flask_login import login_required, current_user

from models import Question, Answer, AnswerComment, db
from qa.forms import WriteQuestionForm, WriteAnswerForm
from utils.constants import Page

qa = Blueprint('qa', __name__,
               template_folder='templates',
               static_folder='../assets')


@qa.route('/')
def hello_world():  # put application's code here
    return redirect(url_for('qa.index', page=1))
    # return render_template('index.html')


@qa.route('/follow')
def follow():
    """关注"""
    per_page = Page.per_page.value
    page = int(request.args.get('page', 1))
    page_data = Question.query.filter_by(is_valid=True).paginate(
        page=page,
        per_page=per_page
    )
    print(page_data)
    return render_template('follow.html', page_data=page_data)


@qa.route('/qa/list')
def question_list():
    """查询问题数据列表"""
    try:
        per_page = Page.per_page.value
        page = int(request.args.get('page', 1))
        page_data = Question.query.filter_by(is_valid=True).paginate(
            page=page,
            per_page=2
        )
        data = render_template('qa_list.html', page_data=page_data)
        return {'code': 0, 'data': data}
    except Exception as e:
        print(e)


@qa.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    """写文章提问"""
    form = WriteQuestionForm()
    if form.validate_on_submit():
        try:
            que_obj = form.save()
            if que_obj:
                flash('发布成功', 'success')
                return redirect(url_for('qa.index', page=1))
        except Exception as e:
            print(e)
        flash('发布失败', 'danger')

    return render_template('write.html', form=form)


@qa.route('/index/<int:page>')
def index(page):
    """首页"""
    per_page = Page.per_page.value
    # page = int(request.args.get('page', 1))
    page_data = Answer.query.filter_by(is_valid=True).paginate(
        page=page,
        per_page=2
    )
    return render_template('index.html', page_data=page_data)


@qa.route('/detail/<int:q_id>', methods=['GET', 'POST'])
def detail(q_id):
    # 1.查询问题信息
    question = Question.query.get_or_404(q_id)
    # 2.展示第一条回答信息
    answer = question.answer_list.filter_by(is_valid=True).first()
    # 3.添加回答
    form = WriteAnswerForm()
    if form.validate_on_submit():
        try:
            if not current_user.is_authenticated:
                flash('请先登录', 'danger')
                return redirect(url_for('accounts.login'))
            form.save(question=question)
            flash('回答成功', 'success')
            return redirect(url_for('qa.detail', q_id=q_id))
        except Exception as e:
            print(e)
            print(form.errors)
    return render_template('detail.html', question=question, answer=answer, form=form)


@qa.route('/comments/<int:answer_id>', methods=['GET', 'POST'])
def comments(answer_id):
    """评论"""
    answer = Answer.query.get(answer_id)
    if request.method == 'POST':
        # 添加评论
        # 1.获取评论
        try:
            if not current_user.is_authenticated:
                result = {'code': 1, 'message': '请登录'}
                return jsonify(result), 400
            content = request.form.get('content', '')
            reply_id = request.form.get('reply_id', None)
            question = answer.question
            comment_obj = AnswerComment(content=content,
                                        user=current_user,
                                        answer=answer,
                                        reply_id=reply_id,
                                        question=question)
            # 2.提交数据库
            db.session.add(comment_obj)
            db.session.commit()
            return '', 201
        except Exception as e:
            result = {'code': 1, 'message': '服务器正忙'}
            return jsonify(result), 400
    else:
        # 获取评论列表
        try:
            page = int(request.args.get('page', 1))
            page_data = answer.comment_list().paginate(
                page=page,
                per_page=2
            )
            data = render_template('comments.html', page_data=page_data, answer=answer)
            return jsonify({'code': 0, 'data': data, 'meta': {'page': page}}), 200
        except Exception as e:
            print(e)
            return jsonify({'code': 0, 'data': '', 'message': '服务器正忙'}), 500


@qa.route('/comment/love/<int:comment_id>', methods=['POST'])
def comment_love(comment_id):
    """为评论点赞"""
    try:
        if not current_user.is_authenticated:
            return '', 401
        comment_obj = AnswerComment.query.get(comment_id)
        comment_obj.love_count += 1
        db.session.add(comment_obj)
        db.session.commit()
    except Exception as e:
        abort(501)

    return '', 201


