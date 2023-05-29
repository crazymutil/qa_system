import os

from flask import current_app
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, PasswordField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_ckeditor import CKEditorField
from models import Question, db, QuestionTags, Answer


class WriteQuestionForm(FlaskForm):
    """写文章"""
    img = FileField(label='上传图片', render_kw={
        'accept': '.jpeg, .jpg, .png'
    }, validators=[FileAllowed(['png', 'jpg', 'jpeg'], '请选择合适的图片类型v')])
    title = StringField(label='标题', render_kw={
        'class': 'form-control',
        'placeholder': '请输入标题（最多50个字）'
    }, validators=[DataRequired('请输入标题v'), Length(min=5, max=50, message='')])
    tags = StringField(label='标签', render_kw={
        'class': 'form-control',
        'placeholder': '输入标签，用,分隔（最多50个字）'
    })
    desc = TextAreaField(label='描述', render_kw={
        'class': 'form-control',
        'placeholder': '简述'
    }, validators=[Length(max=150, message='描述最长为150个字v')])
    content = CKEditorField(label='文章内容', render_kw={
        'class': 'form-control',
        'placeholder': '请输入正文'
    }, validators=[DataRequired('请输入正文v'), Length(min=5, message='标题不能少于5个字v')])

    def save(self):
        """发布问题"""
        # 1.获取图片
        img = self.img.data
        img_name = ''
        if img:
            img_name = secure_filename(img.filename)
            img_path = os.path.join(current_app.config['MEDIA_ROOT'], img_name)
            img.save(img_path)
            print(img_path)
        else:
            print("没有图片")
        # 2.保存问题
        title = self.title.data
        desc = self.desc.data
        content = self.content.data
        que_obj = Question(title=title, desc=desc, img=img_name, content=content, user=current_user)
        db.session.add(que_obj)
        # 3.保存标签
        tags = self.tags.data
        if tags:
            for tag_name in tags.split('，'):
                tag_obj = QuestionTags(tag_name=tag_name, question=que_obj)
                db.session.add(tag_obj)
        db.session.commit()
        return que_obj


class WriteAnswerForm(FlaskForm):
    """写回答"""
    content = CKEditorField(label='回答内容', validators=[
        DataRequired('请输入正文v'), Length(min=5, message='回答内容不能少于5个字v')
    ])

    def save(self, question):
        """保存表单数据"""
        content = self.content.data
        user = current_user
        answer_obj = Answer(content=content, user=user, question=question)
        db.session.add(answer_obj)
        db.session.commit()
        return answer_obj
