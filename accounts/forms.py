import hashlib
import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from models import User
from utils import constants
from utils.validators import phone_required


class RegisterForm(FlaskForm):
    """用户注册"""
    username = StringField(label='用户名', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入用户名'
    }, validators=[DataRequired('请输入用户名'),  phone_required])
    nickname = StringField(label='用户昵称', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入用户昵称'
    }, validators=[DataRequired('请输入用户昵称'),
                   Length(min=2, max=20, message='昵称长度在2-20之间')])
    password = PasswordField(label='密码', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入密码'
    }, validators=[DataRequired('请输入密码')])
    confirm_password = PasswordField(label='确认密码', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请确认密码'
    }, validators=[DataRequired('请确认密码'),
                   EqualTo('password', message='两次密码输入不一致')])

    # validate_username名字是固定的
    def validate_username(self, field):
        """检测用户是否存在"""
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('该用户名已经存在')
        return field


class LoginForm(FlaskForm):
    """用户注册"""
    username = StringField(label='用户名', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入用户名'
    }, validators=[DataRequired('请输入用户名'),  phone_required])
    password = PasswordField(label='密码', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入密码'
    }, validators=[DataRequired('请输入密码')])

    def validate(self, extra_validators=None):
        result = super().validate()
        username = self.username.data
        receive_password = self.password.data
        password = hashlib.sha256(receive_password .encode()).hexdigest()
        print(password)
        if result:
            user = User.query.filter_by(username=username, password=password).first()
            if user is None:
                result = False
                self.username.errors = ['用户名或者密码错误']
            elif user.status == constants.UserStatus.USER_IN_ACTIVE.value:
                result = False
                self.username.errors = ['用户已被禁用']
        return result
