import os.path


class Config(object):
    """项目的配置文件"""
    # 数据库链接URI
    SQLALCHEMY_DATABASE_URI = 'mysql://root:yinliao0729@localhost/flask_qa'
    # flash form wtf
    SECRET_KEY = 'abcdsacd12312'
    # 文件上传的根路径
    MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'assets/medias')


