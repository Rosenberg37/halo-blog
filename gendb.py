from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from apps import create_app, db

# app.config.from_object('app.config')

app = create_app()
# configuration

"""
在命令行里执行以下：
python gendb.py init
python gendb.py migrate
python gendb.py upgrade
"""
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
