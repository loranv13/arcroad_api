from arcroad import arcroad, jwt, db, LOGIN_TYPE
from flask import request, render_template, redirect, jsonify, url_for, session, send_from_directory
from random import *
import datetime
from sqlalchemy import extract, distinct, func

import ldap
from arcroad.models import User
from arcroad.classes.formulaire.login import LoginForm
from flask_login import login_user, logout_user
from arcroad.lib.deco import historique, profil

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
import json



#-------------------------------------------------------------------------------------------
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    #global  ProjetId
    return {
        'profil': identity['profil_id']
    }

# On génère les token d'accès
def generate_token(identity):
    access_token = create_access_token(identity = identity)
    refresh_token = create_refresh_token(identity = identity)
    resp = jsonify({'login': True})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp,200

# ------------------------------------->> Endpoint pour récupérer des tokens avec le refresh
@arcroad.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    return generate_token(current_user)
# --------------------------------------<<

#
#
# ----------------------------------->> Redéfinition des callback JWT
@jwt.unauthorized_loader
def unauthorized_loader_arcroad(r):
        return redirect(url_for('login'))

@jwt.expired_token_loader
def expired_token_loader_arcroad():
        return redirect(url_for('login'))
# -----------------------------------<< Redéfinition des callback JWT

@arcroad.route('/')
@arcroad.route('/index')
@jwt_required
def index():
    return render_template('index.html')


@arcroad.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    print(str(form.login.data)+" "+str(form.password.data))
    message = ""
    if form.validate_on_submit():
        print(">>>> F_Send\n")
        if LOGIN_TYPE is not 'LDAP':
            user = User.query.filter_by(user_login=form.login.data).first()
            if user is None or not user.check_password(form.password.data):
                return redirect(url_for('login'))
            login_user(user, remember=False)

            j = {}
            j['profil_id'] = user.profil.profil_mask
            j['user_login'] = user.user_login
            j['user_nom'] = user.user_nom
            j['user_prenom'] = user.user_prenom

            return generate_token(j)
        else:
            connect = ldap.initialize('ldap://monext.net')
            connect.simple_bind_s('MONEXT\lvillatte', '10Ran355O92&')
            dn = "OU=AIX,OU=FRANCE,OU=_MONEXT,DC=monext,DC=net"
            connect.set_option(ldap.OPT_REFERRALS, 0)
            result = connect.simple_bind_s("MONEXT\\"+form.login.data, form.password.data)
            if result[0] == 97:
                j = {}
                user = User.query.filter_by(user_login=form.login.data).first()
                if user is None:
                    user = User(user_login=form.login.data,user_nom='Bond',user_prenom='James',profil_id=4)
                    db.session.add(user)
                    db.session.commit()
                j['profil_id'] = user.profil.profil_mask
                j['user_login'] = user.user_login
                j['user_nom'] = user.user_nom
                j['user_prenom'] = user.user_prenom
                login_user(user, remember=False)
                return generate_token(j)


    return render_template('login.html',form=form)
# ----------------------------------->> Login / logout




#------------------------------------------------------ Retourne le formulaire de création de projet
@arcroad.route('/formCreateProjet')
@jwt_required
@profil(7,6)
def formCreateProjet():
    return render_template('formCreateProjet.html')
