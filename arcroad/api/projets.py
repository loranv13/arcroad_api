from arcroad import db
from arcroad.models import Projet, OS, Rglfw, Serveur, ProjetServeur, Historique
from arcroad.lib.lib import is_entry_db_exist
from flask import jsonify, request
import datetime
import time
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
'''
-------------------------              --------------------------------------
-------------------------              --------------------------------------
-------------------------    GET       --------------------------------------
-------------------------              --------------------------------------
-------------------------              --------------------------------------
'''

#GET /projets
def get_projets():
    '''
    Retourne l'ensemble de projets si aucun <projet> n'est fourni. Retourne le projet identifié par <projet> dans le cas contraire.
    '''
    j           = {}
    data        = []
    status_code = 200

    projets = Projet.query.all()
    for p in projets:
        h = {}
        h['projectClient']      = p.client.client_name
        h['projectDP']          = p.dp.user_prenom+" "+p.dp.user_nom
        h['projectDataMEP']     = p.projet_date_mep.strftime("%d-%m-%Y")
        h['projectDateCreate']  = p.projet_date_creation.strftime("%d-%m-%Y")
        h['projectGed']         = p.projet_ged
        h['projectId']          = p.projet_id
        h['projectName']        = p.projet_name
        h['projectStatus']      = p.projet_status
        h['projectCPI']         = p.cpi.user_prenom+" "+p.cpi.user_nom
        data.append(h)

    j['data'] = data
    return jsonify(j), status_code

#
# ------
#

#GET /projets/{id}
def get_projet_by_id(id):
    '''
    Retourne l'ensemble de projets si aucun <projet> n'est fourni. Retourne le projet identifié par <projet> dans le cas contraire.
    '''
    status_code = 200
    h = {}
    p = Projet.query.filter_by(projet_id=id).first()
    if p:
        h['projectClient']      = p.client.client_name
        h['projectDP']          = p.dp.user_prenom+" "+p.dp.user_nom
        h['projectDataMEP']     = p.projet_date_mep.strftime("%d-%m-%Y")
        h['projectDateCreate']  = 0
        h['projectGed']         = 0
        h['projectId']          = p.projet_id
        h['projectName']        = p.projet_name
        h['projectStatus']      = 0
        h['projectCPI']         = p.cpi.user_prenom+" "+p.cpi.user_nom

    else:
        status_code     = 404

    return jsonify(h), status_code

#
# ------
#

# GET /projets/<id>/rglFW
def get_rglfws_du_projet(idProjet):
    '''
    Retourne l'ensemble des serveurs construits dans le cadre d'un projet <projet>.
    '''
    j       = {}
    data    = []
    status_code = 200

    rglfw = Rglfw.query.filter_by(rglfw_projet=idProjet).all()

    if rglfw:
        for r in rglfw:
            rfw = {}
            rst = Rglfw.query.filter_by(rglfw_source=r.rglfw_source ,rglfw_destination=r.rglfw_destination ,rglfw_port=r.rglfw_port).count()
            rfw['rglfwObjReseauSource']      = r.source.objrezo_nom
            rfw['rglfwObjReseauDestination'] = r.destination.objrezo_nom
            rfw['rglfwPort']                 = r.rglfw_port
            rfw['rglfwDescription']          = r.rglfw_description
            rfw['rglfwCount']                = rst
            rfw['rglfwId']                   = r.rglfw_id
            data.append(rfw)
    else:
        status_code = 404
        return jsonify({}), status_code
    print(data)
    j['data']=data
    return jsonify(j), status_code

#
# ------
#

# GET /projets/<id>/serveurs
def get_serveurs_du_projet(id):
    '''
    Retourne l'ensemble des serveurs construits dans le cadre d'un projet <projet>.
    '''
    j       = {}
    data    = []
    status_code = 200

    # il faut vérifier que le projet existe!!!

    serveurs = ProjetServeur.query.filter_by(p_id=id).all()
    if serveurs:
        for s in serveurs:
            h = {}
            h['srvId']          = s.s_id
            h['srvHostname']    = s.srv.srv_hostname
            h['srvCPU']         = s.srv.srv_cpu
            h['srvRAM']         = s.srv.srv_ram
            h['srvOSName']      = s.srv.os.os_name
            h['srvPCI']         = s.srv.srv_pci
            data.append(h)
            #data.append([s.srv.srv_hostname,s.srv.srv_cpu,s.srv.srv_ram,s.srv.os.os_name,s.srv.srv_pci,s.s_id ])
    else:
        status_code = 404
        return jsonify({}), status_code

    j['data']=data
    return jsonify(j), status_code




'''
-------------------------              --------------------------------------
-------------------------              --------------------------------------
-------------------------    POST       --------------------------------------
-------------------------              --------------------------------------
-------------------------              --------------------------------------
'''

# POST /projets
def add_projets():
    '''
    création d'un projet
    '''
    j               = {}
    status_code     = 201
    val = request.get_json()

    if val['projectName'] == "":
        status_code = 400
        return jsonify({'error':'Le nom du projet est incorrect'}), status_code

    if is_entry_db_exist('user', val['projectCPI']) and is_entry_db_exist('user', val['projectDP']):
        ps = Projet(\
        projet_name=val['projectName'], \
        projet_client=val['projectClient'], \
        projet_date_creation=datetime.datetime.now(),\
        projet_date_mep=datetime.datetime.strptime(val['projectDataMEP'], '%d-%m-%Y'),\
        projet_cpi=val['projectCPI'],\
        projet_dp=val['projectDP'],\
        projet_status=val['projectStatus'],\
        projet_ged=val['projectGed'] )
        db.session.add(ps)
        try:
            db.session.commit()
            projetId = ps.projet_id
        except:
            status_code = 500
            db.session.rollback()
            return jsonify({'error': 'Erreur d\'enregistrement'}), status_code
    else:
        return jsonify({'error':'L\'ID du Chef/Directeur de projet est incorrect'}), status_code

    return jsonify({'projetId': projetId }), status_code



#POST /projets/{idProjet}/rglfw/{idRglfw}
def add_rglfw_au_projet(idProjet):
    ''' Ajoute une règle FW'''
    j               = {}
    status_code     = 201
    val = request.get_json()

    if val['rglfwDescription'] == "":
        status_code = 400
        return jsonify({'error':'La description est obligatoire'}), status_code

    if is_entry_db_exist('objetReseau', val['rglfwSource']) and is_entry_db_exist('objetReseau', val['rglfwDestination']):
        rf = Rglfw(\
        rglfw_source=val['rglfwSource'], \
        rglfw_destination=val['rglfwDestination'], \
        rglfw_port=val['rglfwPort'],\
        rglfw_etat=0,\
        rglfw_projet=idProjet)
        db.session.add(rf)
        try:
            db.session.commit()
            rglfwId = rf.rglfw_id
        except:
            status_code = 500
            db.session.rollback()
            return jsonify({'error': 'Erreur d\'enregistrement'}), status_code
    else:
        return jsonify({'error':'L\'ID de l\'objet réseau source/destination est incorrect'}), status_code

    return jsonify({'rglfwId': rglfwId }), status_code


'''
-------------------------              --------------------------------------
-------------------------              --------------------------------------
-------------------------    PUT       --------------------------------------
-------------------------              --------------------------------------
-------------------------              --------------------------------------
'''



#PUT /projets/{idProjet}/serveur/{idServeur}
def add_serveur_au_projet(idProjet,idServeur):
    status_code     = 201
    srvp = ProjetServeur(p_id=idProjet,s_id=idServeur)

    db.session.commit()
    ps_id = srvp.ps_id
    '''
    status_code = 500
    db.session.rollback()
    return jsonify({'error': 'Erreur d\'enregistrement'}), status_code
    '''
    return jsonify({'projetServeurId': srvp.ps_id}),status_code


def modif_rglfw_au_projet():
    status_code     = 201




'''
-------------------------              --------------------------------------
-------------------------              --------------------------------------
-------------------------    DELETE    --------------------------------------
-------------------------              --------------------------------------
-------------------------              --------------------------------------
'''

#DELETE /projets/{id}
def del_projets_by_id(idp):
    ''' Demande de suppression. On passe le status du projet à 0 '''


#
#DELETE /projets/{idProjet}/serveur/{idServeur}
#
def supp_serveur_au_projet(idProjet, idServeur):

    status_code = 204

    # On vérifie que l'id serveur existe et que l'id projet existe
    if not is_entry_db_exist('serveur', idServeur ):
        status_code = 404
        return jsonify({'ErrorCode': 200, 'ErrorLabel': 'Serveur inexistant'}), status_code
    if not is_entry_db_exist('projet', idProjet):
        status_code = 404
        return jsonify({'ErrorCode': 200, 'ErrorLabel': 'Projet inexistant'}), status_code

    srv = ProjetServeur.query.filter_by(p_id=idProjet, s_id=idServeur).first()
    if not srv:
        status_code = 404
        return jsonify({'ErrorCode': 300, 'ErrorLabel': 'Le serveur ne fait pas parti du projet'}), status_code
    try:
        db.session.delete(srv)
        db.session.commit()
    except:
        status_code = 500
        db.session.rollback()
        return jsonify({'ErrorLabel': 'Erreur technique'}), status_code

    return jsonify({}), status_code


#
#DELETE /projets/{idp}/rglfw/{id}
#
def supp_rglfw_au_projet(idProjet, idRglfw):

    status_code = 204
    rgl = Rglfw.query.filter_by(rglfw_projet=idProjet, rglfw_id=idRglfw).first()
    if rgl.rglfw_etat == 0:
        try:
            db.session.delete(rgl)
            db.session.commit()
        except:
            status_code = 500
            db.session.rollback()
            return jsonify({'ErrorLabel': 'Erreur technique'}), status_code
    else:
        status_code = 409
        return jsonify({'ErrorCode': 101, 'ErrorLabel': 'La règle a été soumise et est en cours de traitement'}), status_code

    return jsonify({}), status_code
