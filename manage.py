from logic import create_app, db, models
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


# 创建app
app = create_app('dev')
# 创建脚本管理对象
manger = Manager(app)
# 让迁移和app和db建立联系
Migrate(app, db)
# 将迁移的脚本命令添加到manager
manger.add_command("mysql", MigrateCommand)

if __name__ == '__main__':
    print(app.url_map)
    manger.run()
