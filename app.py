from flask import Flask, session, g
from flask_login import LoginManager
from models import db, User
from accounts.views import accounts
from qa.views import qa
from utils.filters import number_split, dt_format_show
from flask_ckeditor import CKEditor

app = Flask(__name__, static_folder='assets')

app.config.from_object('conf.Config')

# 数据库初始化
db.init_app(app)

# 富文本初始化
ckeditor = CKEditor()
ckeditor.init_app(app)


# 登录验证
login_manager = LoginManager()
login_manager.login_view = "accounts.login"
login_manager.login_message = "please login firstly"
login_manager.login_message_category = "danger"
login_manager.init_app(app)
# with app.app_context():
#     """创建数据库"""
#     db.create_all()
# 注册蓝图
app.register_blueprint(accounts, url_prefix='/accounts')  # url_prefix类似于路由分发
app.register_blueprint(qa, url_prefix='/')

# 注册过滤器
app.jinja_env.filters['number_split'] = number_split
app.jinja_env.filters['dt_format_show'] = dt_format_show



# @app.before_request
# def before_request():
#     """如果有用户id 设置到全局变量"""
#     user_id = session.get('user_id', None)
#     if user_id:
#         user = User.query.get(user_id)
#         print(user)
#         g.current_user = user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


