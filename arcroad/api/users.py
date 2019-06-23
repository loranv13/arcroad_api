from arcroad import db
from arcroad.models import User
from arcroad.lib.lib import is_entry_db_exist
from flask import jsonify

#GET /users
def get_users():
    '''
    Retourne l'ensemble des users ayant des droits spécifiques.
    '''
    j           = {}
    data        = []
    status_code = 200

    users = User.query.all()
    for u in users:
        h = {}
        h['userId']             = u.user_id
        h['userNom']            = u.user_nom
        h['userPrenom']         = u.user_prenom
        h['userEmail']          = u.user_email
        h['profilId']           = u.profil_id

        data.append(h)

    j['data'] = data
    return jsonify(j), status_code

#GET /users/{id}
def get_user_by_id(id):
    '''
    Retourne le user avec l'id transmis
    '''
    h           = {}
    status_code = 200

    u = User.query.filter_by(user_id=id).first()
    if u:
        h['userId']             = u.user_id
        h['userNom']            = u.user_nom
        h['userPrenom']         = u.user_prenom
        h['userEmail']          = u.user_email
        h['profilId']           = u.profil_id
    else:
        status_code     = 404
    return jsonify(h), status_code
