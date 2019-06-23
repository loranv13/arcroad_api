from arcroad import db
from arcroad.models import Projet, OS, Rglfw, Serveur, ProjetServeur, User, ObjetReseau


def is_entry_db_exist(obj, id):

    #val = ft[obj].query.filter_by(exec("%s=%d" % (id[obj],id)))

    if obj == "user":
        val = User.query.filter_by(user_id=id).all()
    elif obj == 'serveur':
        val = Serveur.query.filter_by(srv_id=id).all()
    elif obj == "ProjetServeur":
        # utiliser pour la suppression d'un serveur. On vérifie qu'il ne soit pas rattaché à un projet
        val = ProjetServeur.query.filter_by(s_id=id).all()
    elif obj == "CompteServeur":
        val = CompteServeur.query.filter_by(cps_serveur=id).all()
    elif obj == 'projet':
        val = Projet.query.filter_by(projet_id=id).all()
    elif obj == 'objetReseau':
        val = ObjetReseau.query.filter_by(objrezo_id=id).all()

    if val:
        return val
    else:
        return False
