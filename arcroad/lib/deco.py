from flask import jsonify, request, session
from arcroad.models import Historique
from flask_jwt_extended import get_jwt_identity, get_jwt_claims
from arcroad import arcroad, db
from functools import wraps
import logging
import datetime

def historique(fct):
    @wraps(fct)
    def historique_(*parametres_non_nommes, **parametres_nommes):
        claims = get_jwt_claims()
        id = get_jwt_identity()
        if request.method != 'GET':
            h = Historique(histo_fct=request.method+" "+request.full_path, histo_projet=session['projet'], histo_data=request.get_json(), history_user=id['user_login']  )
            db.session.add(h)
            db.session.commit()
        #arcroad.logger.addHandler(logging.StreamHandler())
        log = logging.getLogger('werkzeug')
        #arcroad.logger.setLevel(logging.INFO)
        #arcroad.logger.info(str(request.method)+" "+str(request.full_path)+" "+str(request.get_json()))
        log.info("_INFO APPEL API - ["+str(datetime.datetime.now().strftime('%d/%b/%Y %H:%M:%S'))+"] - "+str(request.method)+" "+str(request.full_path)+" "+str(request.get_json()))

        return fct(*parametres_non_nommes, **parametres_nommes)

    return historique_



def profil(*a_args, **a_kwargs):
    def profil_deco(fct):
        @wraps(fct)
        def profil_(*args, **kwargs):
            claims = get_jwt_claims()
            if claims['profil'] not in a_args:
                return ('{"ErrorCode":666,"ErrorLabel":"Tu crois que c\'est la fête??!! Droits insuffisants!!!"}')
            return fct(*args, **kwargs)
        return profil_
    return profil_deco
