from arcroad import db
from arcroad.models import ObjetReseau
from arcroad.lib.lib import is_entry_db_exist
from flask import jsonify, request
import datetime
import time


#GET /projets
def get_objetReseaux():
    '''
    Retourne l'ensemble de projets si aucun <projet> n'est fourni. Retourne le projet identifié par <projet> dans le cas contraire.
    '''
    j           = {}
    data        = []
    status_code = 200

    objr = ObjetReseau.query.all()
    for o in objr:
        h = {}
        h['objetId']      = o.objrezo_id
        h['objetName']    = o.objrezo_nom
        data.append(h)

    j['data'] = data
    return jsonify(j), status_code


def add_objetReseaux():
    '''ajout d un objet reseau'''
    j               = {}
    status_code     = 201
    val = request.get_json()

    if val['objName'] == "":
        status_code = 400
        return jsonify({'error':'Le nom de l\'objet est incorrect'}), status_code

    obj = ObjetReseau(objrezo_nom=val['objName'])
    db.session.add(obj)
    try:
        db.session.commit()
    except:
        status_code = 500
        db.session.rollback()
        return jsonify({'error': 'Erreur d\'enregistrement'}), status_code

    return jsonify({'objId': obj.objrezo_id }), status_code
