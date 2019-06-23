import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
from flask_cors import CORS

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)



#------------------------------------------------> Création de l'application
arcroadConnexion   = connexion.App(__name__, specification_dir='swagger/')
application = arcroadConnexion.app
CORS(application)
application.config.from_object(Config)
#login       = LoginManager(application) # gestion des users
db          = SQLAlchemy(application) # pour créer la bdd. Est appelé dans le modèle
migrate     = Migrate(application, db) #
jwt         = JWTManager(application)
arcroadConnexion.add_api('openapi.yaml')
#------------------------------------------------< Création de l'application
#login
#LOGIN_TYPE = os.environ.get('LOGIN_TYPE') or 'LDAP'
