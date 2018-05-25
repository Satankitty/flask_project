from flask import Flask


class Config(object):
    """配置文件的加载"""

    # 开启调试模式
    DEBUG = True


app = Flask(__name__)

# 配置文件的加载
app.config.from_object(Config)


@app.route('/')
def index():
    return 'index'


if __name__ == '__main__':
    app.run()