from logic import app,db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# 创建脚本管理对象
manger = Manager(app)
# 让迁移和app和db建立联系
Migrate(app, db)
# 将迁移的脚本命令添加到manager
manger.add_command("mysal", MigrateCommand)


@app.route('/')
def index():

    return 'index'
    redis_store.set("name", "zhangsan")


if __name__ == '__main__':
    manger.run()