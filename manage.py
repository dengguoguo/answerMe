#!/usr/bin/python
# -*- coding: utf-8 -*-
#author dengguo
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from pythonqa import app
from exts import db
from models import User, Question, Answer

manager = Manager(app)

#绑定app和db
migrate = Migrate(app, db)

#迁移脚本命令到manager中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
