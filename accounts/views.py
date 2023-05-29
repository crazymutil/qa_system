import hashlib

from flask import Blueprint, render_template, flash, url_for, redirect, session, request
from flask_login import login_user, logout_user

from accounts.forms import RegisterForm, LoginForm
from models import User, db, UserProfile, UserLoginHistory

accounts = Blueprint('accounts', __name__,
                     template_folder='templates',
                     static_folder='../assets')


@accounts.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # 没get到参数的话 就是后面的那个url
    next_url = request.values.get('next', url_for('qa.index', page=1))
    # 这两句代码会在页面刷新时执行一次，提交表单后会再执行一次
    # print('第一个nexturl{}'.format(next_url))
    if form.validate_on_submit():
        print('正在登录')
        username = form.username.data
        receive_password = form.password.data
        password = hashlib.sha256(receive_password.encode()).hexdigest()
        print(password)

        # password = form.password.data
        # 1.查找对应的用户
        user = User.query.filter_by(username=username, password=password).first()
        # 2.登录用户
        # session['user_id'] = user.id
        login_user(user)
        # 3.记录日志
        ip = request.remote_addr
        ua = request.headers.get('user-agent', None)
        obj = UserLoginHistory(username=username, ip=ip, ua=ua, user=user)
        db.session.add(obj)
        db.session.commit()
        # 4.跳转到首页

        flash('{},欢迎回来'.format(user.nickname), 'success')
        # print('第二个nexturl{}'.format(next_url))
        return redirect(next_url)
    else:
        print(form.errors)
    return render_template('login.html', form=form, next_url=next_url)


@accounts.route('/logout')
def logout():
    """退出登录"""
    # 自定义登录
    # session['user_id'] = ''
    # g.current_user = None
    logout_user()
    flash('欢迎下次再来', 'success')
    return redirect(url_for('accounts.login'))


@accounts.route('/register', methods=['GET', 'POST'])
def register():
    """注册"""
    form = RegisterForm()
    if form.validate_on_submit():
        # 1.获取表单信息
        username = form.username.data
        password = form.password.data
        nickname = form.nickname.data
        # 2.添加到db.session
        try:
            # 将密码加密存储
            password = hashlib.sha256(password.encode()).hexdigest()
            user_obj = User(username=username, password=password, nickname=nickname)
            db.session.add(user_obj)
            profile = UserProfile(username=username, user=user_obj)
            db.session.add(profile)
            db.session.commit()
            # 3.跳转到成功页面
            flash('注册成功，请登录', 'success')
            return redirect(url_for('accounts.login'))
        except Exception as e:
            print(e)
            flash('注册失败', 'danger')
    return render_template('register.html', form=form)


@accounts.route('/mine')
def mine():
    return render_template('mine.html')
