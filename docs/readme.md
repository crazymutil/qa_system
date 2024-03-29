## 开发环境
```
pycharm2021专业版
```
```
依赖的库都可通过pycharm中file-settings-project-python interpreter直接安装
```
```
安装较慢的话 可以设置国内镜像源
```
```
本项目需要连接本地数据库，在conf.py中SQLALCHEMY_DATABASE_URI，root:yinliao0729设置成自己本地数据库的用户名和密码，记得先创建名为flask_qa的数据库。
```
```
第一次运行需要创建表，在app.py文件中，第27-29行代码取消注释，然后运行，便可创建数据表。之后在运行时，把这三行代码再次注释即可。
```


## pip镜像源

清华大学
https://pypi.tuna.tsinghua.edu.cn/simple/
```
pip install flask -i https://pypi.tuna.tsinghua.edu.cn/simple/
```
## Flask
### 1.flask微框架
* [flask 中文文档](http://docs.jinkan.org/docs/flask/index.html)
* [flask 英文文档](https://flask.palletsprojects.com/en/1.1.x/)

### 2.Jinja2模板引擎
* [Jinja2 文档](https://jinja.palletsprojects.com/en/2.11.x/)

## 依赖安装
### 1.mysqlclient
* [whl下载](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient)

### 2. flask-wtf
* [fask-wtf文档](https://flask-wtf.readthedocs.io/en/stable/)
* [wtforms文档](https://wtforms.readthedocs.io/en/stable/)

### 3. flask-sqlalchemy
* [PyPi](https://pypi.org/project/Flask-SQLAlchemy/)
* [fask-sqlalchemy英文文档](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
* [fask-sqlalchemy中文文档](http://www.pythondoc.com/flask-sqlalchemy/quickstart.html)
* [SQLAlchemy文档](https://docs.sqlalchemy.org/)

### 4. flask-login 
* [源码](https://github.com/maxcountryman/flask-login)
* [文档](http://www.pythondoc.com/flask-login/index.html)
