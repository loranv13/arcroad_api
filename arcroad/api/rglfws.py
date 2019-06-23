from arcroad import db
from arcroad.models import Projet, OS, Rglfw, Serveur, ProjetServeur, Historique
from arcroad.lib.lib import is_entry_db_exist
from flask import jsonify, request
import datetime
import time



'''
-------------------------              --------------------------------------
-------------------------              --------------------------------------
-------------------------    GET       --------------------------------------
-------------------------              --------------------------------------
-------------------------              --------------------------------------
'''

def get_rglfws():
    '''
    Retourne l'ensemble des règles.
    '''
    j       = {}
    data    = []
    status_code = 200

    rglfws = Rglfw.query.all()

    if rglfws:
        for r in rglfws:
            rgl={}
            rgl['rglfwID']          = r.rglfw_id
            rgl['rglfwSource']      = r.source.objrezo_nom
            rgl['rglfwDestination'] = r.destination.objrezo_nom
            rgl['rglfwPort']        = r.rglfw_port
            rgl['rglfwDescription'] = r.rglfw_description
            rgl['rglfwEtat']        = r.rglfw_etat
            rgl['rglfwProjet']      = r.rglfw_projet
            data.append(rgl)
    else:
        status_code = 404
        return jsonify({}), status_code

    j['data']=data
    return jsonify(j), status_code



'''
-------------------------              --------------------------------------
-------------------------              --------------------------------------
-------------------------    POST      --------------------------------------
-------------------------              --------------------------------------
-------------------------              --------------------------------------
'''

#POST /rglfws/
def add_rglfw():
    ''' Ajoute une règle FW'''
    j               = {}
    status_code     = 201
    val = request.get_json()
