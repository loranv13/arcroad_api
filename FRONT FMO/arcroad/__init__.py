import os
# Moteur http
from flask import Flask
# module de gestion des users (authentification)
from flask_login import LoginManager
# utile pour le wtf des templates
from flask_bootstrap import Bootstrap
# JWT
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
#u_arc dfgt12ll0

#------------------------------------------------> Création de l'application
arcroad = Flask(__name__)
arcroad.config.from_object(Config)
arcroad.config['SECRET_KEY']        = 'incimdsosbdvoduvboqozuvhihiHIHI%HHihcichùehHIHZ'


arcroad.config['JWT_TOKEN_LOCATION']        = ['cookies']
arcroad.config['JWT_ACCESS_COOKIE_PATH']    = '/'
arcroad.config['JWT_REFRESH_COOKIE_PATH']   = '/refresh'
arcroad.config['JWT_COOKIE_CSRF_PROTECT']   = False
arcroad.config['JWT_SECRET_KEY']            = 'scdvbbfdb5fdbsdfbDZSDd5d6zd54DZBG::E$'
arcroad.config['JWT_USER_CLAIMS']           = 'info'
arcroad.config['JWT_ACCESS_TOKEN_EXPIRES']  = False
login       = LoginManager(arcroad)
bootstrap   = Bootstrap(arcroad)

db          = SQLAlchemy(arcroad)
migrate     = Migrate(arcroad, db) #
jwt         = JWTManager(arcroad)

#------------------------------------------------< Création de l'application

#login
LOGIN_TYPE = os.environ.get('LOGIN_TYPE') or 'LDAP'

# On importe les éléments pour créer la bdd et déclencher l'appli
from arcroad.routes import main
from arcroad import models
