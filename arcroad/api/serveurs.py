from arcroad import db
from arcroad.models import Serveur
from flask import jsonify
from arcroad.lib.lib import is_entry_db_exist



'''
-------------------------              --------------------------------------
-------------------------              --------------------------------------
-------------------------    GET       --------------------------------------
-------------------------              --------------------------------------
-------------------------              --------------------------------------
'''

#GET /serveurs
def get_serveurs():
    #Retourne l'ensemble des serveurs si aucun <serveur> n'est fourni. Retourne le serveur identifié par <serveur> dans le cas contraireself.
    j       = {}
    data    = []
    status_code = 200

    serveurs = Serveur.query.all()
    if serveurs:
        for s in serveurs:
            srv = {}
            srv['srvHostname']    = s.srv_hostname
            srv['srvCPU']         = s.srv_cpu
            srv['srcRAM']         = s.srv_ram
            srv['srvOSName']      = s.os.os_name
            srv['srvPCI']         = s.srv_pci
            srv['srvId']          = s.srv_id
            data.append(srv)
    else:
        status_code = 404
        return jsonify({}), status_code

    j['data']=data
    return jsonify(j), status_code


#GET /serveurs/{id}
def get_serveur_by_id(ids):
    #Retourne l'ensemble des serveurs si aucun <serveur> n'est fourni. Retourne le serveur identifié par <serveur> dans le cas contraireself.
    j       = {}
    data    = []
    status_code = 200

'''
-------------------------              --------------------------------------
-------------------------              --------------------------------------
-------------------------    DELETE    --------------------------------------
-------------------------              --------------------------------------
-------------------------              --------------------------------------
'''
#DELETE /srveurs/{id}
def supp_serveur(id):
    ''' supprime le serveur'''
    j       = {}
    status_code = 200
    pjsrv = is_entry_db_exist("ProjetServeur", id)
    if not pjsrv:
        # on supprime le serveur, les fs, les users
        print('Demande de supp')
    else:
        status_code = 409
        data = []
        for ps in pjsrv:
            data.append(ps.p_id)
        j['ErrorCode']      = 100 #La demande de suppression ne peut être honnoré car l'objet appartient à un autre objet
        j['ErrorLabel']     = 'Le serveur utilisé dans un ou plusieurs projets'
        j['idProjets']      = data
        return jsonify(j), status_code
