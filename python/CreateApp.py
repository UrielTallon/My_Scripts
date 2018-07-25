###################################################################
#
###################################################################

import argparse
import os

class AppBuilder:
    def __init__(self, name):
        
        # supported features
        self.sp_database = False
        self.sp_logging = False # TODO: implement logging
        self.sp_wtf = False
        
        # directories path
        self.path_for_root =  os.path.join('.', name)
        self.path_for_app = os.path.join(self.path_for_root, 'app')
        self.path_for_cfg = os.path.join(self.path_for_root, 'config.py')
        self.path_for_vws = os.path.join(self.path_for_app, 'views.py')
        
        # create the root directory for the app
        os.mkdir(self.path_for_root)
        
        # add directory for temporary files (logs)
        os.mkdir(os.path.join(self.path_for_root, 'tmp'))
        
        # add actual app directories
        os.mkdir(self.path_for_app)
        os.mkdir(os.path.join(self.path_for_app, 'static'))
        os.mkdir(os.path.join(self.path_for_app, 'templates'))
    
        # add file to run app locally
        with open(os.path.join(self.path_for_root, 'run.py'), 'w') as run_file:
            run_file.write('from app import app\n')
            run_file.write('\n')
            run_file.write('app.run(debug = False)')
        
        # add configuration file
        with open(self.path_for_cfg, 'w') as cfg_file:
            cfg_file.write('import os\n')
            cfg_file.write('\n')
            cfg_file.write('basedir = os.path.abspath(os.path.dirname(__file__))\n')
            cfg_file.write('\n')

        # add test set up file
        with open(os.path.join(self.path_for_root, 'test.py'), 'w') as tst_file:
            tst_file.write('import os\n')
            tst_file.write('import unittest\n')
            tst_file.write('from datetime import datetime, timedelta\n')
            tst_file.write('from config import basedir\n')
            tst_file.write('\n')
        
        # add basic views file to complete
        with open(self.path_for_vws, 'w') as view_file:
            view_file.write('from flask import render_template, flash, redirect, url_for, session, request, g\n')
            
        # add base html template
        with open(os.path.join(self.path_for_app, 'templates/base.html'), 'w') as base_file:
            base_file.write('<!DOCTYPE html>\n')
            base_file.write('<html lang="en">\n')
            base_file.write('\n')
            base_file.write('\t<head>\n')
            base_file.write('\t\t<meta charset="utf-8" />\n')
            base_file.write('\t\t<meta http-equiv="X-UA-Compatible" content="IE=edge" />\n')
            base_file.write('\t\t<!-- <meta name="viewport" content="width=device-width, initial-scale=1" /> for responsiveness -->\n')
            base_file.write('\t\t<title>Place Title in Here</title>\n')
            base_file.write('\t\t<!-- add a favicon from static directory (16x16px png) -->\n')
            base_file.write('\t\t<!-- <link rel="shortcut icon" href="{}" /> -->\n'.format("{{ url_for('static', filename='favicon.ico') }}"))
            base_file.write('\t\t<!-- links to css and javascript libraries to place below -->\n')
            base_file.write('\t</head>\n')
            base_file.write('\n')
            base_file.write('\t<body>\n')
            base_file.write('\t\t{% block content %}{% endblock %}\n')
            base_file.write('\t</body>\n')
            base_file.write('\n')
            base_file.write('</html>\n')
        
    def addFormSupport(self, fields = None, validators = None):
        self.sp_wtf = True
        with open(self.path_for_cfg, 'a') as cfg_file:
            cfg_file.write('# Support for forms added:\n')
            cfg_file.write('WTF_CSRF_ENABLED = True\n')
            cfg_file.write('SECRET_KEY = "SOMETHING_HARD_TO_GUESS"\n')
            cfg_file.write('\n')
            
        with open(os.path.join(self.path_for_app, 'forms.py'), 'w') as form_file:
            form_file.write('from flask_wtf import Form\n')
            if fields is not None:
                form_file.write('from wtforms import {}\n'.format(', '.join(fields)))
            else:
                form_file.write('from wtforms import *\n')
            if validators is not None:
                form_file.write('from wtforms.validators import {}\n'.format(', '.join(validators)))
            else:
                form_file.write('from wtforms.validators import *\n')
                
        with open(self.path_for_vws, 'a') as view_file:
            view_file.write('from .forms import *\n')
    
    def addDatabaseSupport(self):
        self.sp_database = True
        with open(self.path_for_cfg, 'a') as cfg_file:
            cfg_file.write('# Support for database added:\n')
            cfg_file.write("SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')\n")
            cfg_file.write("SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')\n")
            cfg_file.write('\n')
        
        with open(os.path.join(self.path_for_app, 'models.py'), 'w') as mod_file:
            mod_file.write('from app import db\n')
            mod_file.write('from app import app\n')
            mod_file.write('import sys\n')
            
        with open(self.path_for_vws, 'a') as view_file:
            view_file.write('from .models import *\n')
            
        # create db script:
        with open(os.path.join(self.path_for_root, 'db_create.py'), 'w') as script_db:
            script_db.write('# Inspired by Miguel Grinberg\'s Flask Mega Tutorial.\n')
            script_db.write('# Check it out at https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world')
            script_db.write('\n\n')
            script_db.write('from migrate.versioning import api\n')
            script_db.write('from config import SQLALCHEMY_DATABASE_URI\n')
            script_db.write('from config import SQLALCHEMY_MIGRATE_REPO\n')
            script_db.write('from app import db\n')
            script_db.write('import os.path\n')
            script_db.write('\n')
            script_db.write('db.create_all()\n')
            script_db.write('if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):\n')
            script_db.write("\tapi.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')\n")
            script_db.write('\tapi.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)\n')
            script_db.write('else:\n')
            script_db.write('\tapi.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))\n')
        
        with open(os.path.join(self.path_for_root, 'db_migrate.py'), 'w') as script_mg:
            script_mg.write('# Inspired by Miguel Grinberg\'s Flask Mega Tutorial.\n')
            script_mg.write('# Check it out at https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world')
            script_mg.write('\n\n')
            script_mg.write('import imp\n')
            script_mg.write('from migrate.versioning import api\n')
            script_mg.write('from app import db\n')
            script_mg.write('from config import SQLALCHEMY_DATABASE_URI\n')
            script_mg.write('from config import SQLALCHEMY_MIGRATE_REPO\n')
            script_mg.write('\n')
            script_mg.write('v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)\n')
            script_mg.write("migration = SQLALCHEMY_MIGRATE_REPO + '/versions/{:03d}_migration.py'.format(v + 1)\n")
            script_mg.write("tmp_module = imp.new_module('old_model')\n")
            script_mg.write('old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)\n')
            script_mg.write('exec(old_model, tmp_module.__dict__)\n')
            script_mg.write('script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)\n')
            script_mg.write("open(migration, 'wt').write(script)\n")
            script_mg.write('api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)\n')
            script_mg.write('v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)\n')
            script_mg.write('\n')
            script_mg.write("print('New migration saved as {}'.format(migration))\n")
            script_mg.write("print('Current database version: {}'.format(v))\n")
            
        with open(os.path.join(self.path_for_root, 'db_downgrade.py'), 'w') as script_dg:
            script_dg.write('# Inspired by Miguel Grinberg\'s Flask Mega Tutorial.\n')
            script_dg.write('# Check it out at https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world')
            script_dg.write('\n\n')
            script_dg.write('from migrate.versioning import api\n')
            script_dg.write('from config import SQLALCHEMY_DATABASE_URI\n')
            script_dg.write('from config import SQLALCHEMY_MIGRATE_REPO\n')
            script_dg.write('\n')
            script_dg.write('v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)\n')
            script_dg.write('api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)\n')
            script_dg.write('v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)\n')
            script_dg.write('\n')
            script_dg.write("print('Current database version: {}'.format(v))\n")
            
        with open(os.path.join(self.path_for_root, 'db_upgrade.py'), 'w') as script_ug:
            script_ug.write('# Inspired by Miguel Grinberg\'s Flask Mega Tutorial.\n')
            script_ug.write('# Check it out at https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world')
            script_ug.write('\n\n')
            script_ug.write('from migrate.versioning import api\n')
            script_ug.write('from config import SQLALCHEMY_DATABASE_URI\n')
            script_ug.write('from config import SQLALCHEMY_MIGRATE_REPO\n')
            script_ug.write('\n')
            script_ug.write('api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)\n')
            script_ug.write('v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)\n')
            script_ug.write('\n')
            script_ug.write("print('Current database version: {}'.format(v))\n")
    
    def finalizeApp(self):
        imp_l = ['views']
        # Set the initialization script
        with open(os.path.join(self.path_for_app, '__init__.py'), 'w') as init_script:
            init_script.write('import os\n')
            init_script.write('from flask import Flask\n')
            if self.sp_database:
                imp_l.append('models')
                init_script.write('from flask_sqlalchemy import SQLAlchemy\n')
            init_script.write('from config import basedir\n')
            init_script.write('\n')
            init_script.write('app = Flask(__name__)\n')
            init_script.write("app.config.from_object('config')\n")
            if self.sp_database:
                init_script.write('db = SQLAlchemy(app)\n')
            init_script.write('\n')
            
            init_script.write('from app import {}\n'.format(', '.join(imp_l)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Create Flask application arborescence')
    parser.add_argument('name', type = str, 
                        help = 'The name of the application; will set the name of the root directory.')
    args = parser.parse_args()
    
    FORM_FIELDS = ['StringField', 'TextAreaField']
    FORM_VALIDATORS = ['DataRequired', 'Length']
    
    builder = AppBuilder(args.name)
    # Add support for various features here
    builder.addFormSupport(FORM_FIELDS, FORM_VALIDATORS)
    builder.addDatabaseSupport()
    # Do not edit below this point
    builder.finalizeApp()