import os
from flask_script import Manager#manager tracks how the commands are run on the terminal
from flask_migrate import Migrate, MigrateCommand#contains a set of migration commands
from app import db,create_app

config_name= os.getenv('APP_SETTINGS')
app= create_app(config_name)

migrate=Migrate(app,db)
manager=Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
