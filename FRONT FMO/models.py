from arcroad import db
from datetime import datetime
from flask_login import UserMixin
import hashlib


#---------------------------------------------------------- > CLASS :
'''
CLASS : User
'''
class User( UserMixin, db.Model):
    user_id             = db.Column(db.Integer, primary_key=True)
    user_login          = db.Column(db.String(64), index=True, unique=True)
    user_nom            = db.Column(db.String(64), index=True, unique=True)
    user_prenom         = db.Column(db.String(64), index=True, unique=True)
    user_email          = db.Column(db.String(120), index=True, unique=True)
    profil_id           = db.Column(db.Integer, db.ForeignKey('profil.profil_id'))
    user_password_hash  = db.Column(db.String(128))

    profil     = db.relationship("Profil", foreign_keys=[profil_id])

    def __repr__(self):
        return '<User {}>'.format(self.user_login)

    def set_password(self, pwd):
        m = hashlib.md5()
        m.update(pwd.encode('utf-8'))
        self.user_password_hash = m.hexdigest()

    def check_password(self, pwd):
        m = hashlib.md5()
        m.update(pwd.encode('utf-8'))
        if self.user_password_hash == m.hexdigest():
            return True
        return False

    def get_id(self):
        return self.user_id
#---------------------------------------------------------- < CLASS : User




#---------------------------------------------------------- > CLASS : Profil
'''
CLASS : Profil
0: touriste
1: system
2: reseau
4: DP
6: cpi
7: admin
'''
class Profil(db.Model):
    profil_id          = db.Column(db.Integer, primary_key=True)
    profil_name        = db.Column(db.String(140))
    profil_mask        = db.Column(db.Integer)
#---------------------------------------------------------- < CLASS : Profil




#---------------------------------------------------------- > CLASS : Profil
'''
CLASS : Historique
'''
class Historique(db.Model):
    histo_id        = db.Column(db.Integer, primary_key=True)
    histo_projet    = db.Column(db.Integer, db.ForeignKey('projet.projet_id'))
    histo_date      = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    histo_fct       = db.Column(db.String(140))
    histo_data      = db.Column(db.String(140))
    history_user    = db.Column(db.String(140))

#---------------------------------------------------------- < CLASS : Profil






#---------------------------------------------------------- > CLASS :
'''
CLASS : Projet
'''
class Projet(db.Model):
    projet_id               = db.Column(db.Integer, primary_key=True)
    projet_name             = db.Column(db.String(140))
    projet_client           = db.Column(db.Integer, db.ForeignKey('client.client_id'))
    projet_date_creation    = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    projet_date_mep         = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    projet_cpi              = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    projet_dp               = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    projet_status           = db.Column(db.Integer)
    projet_ged              = db.Column(db.String(240))

    cpi     = db.relationship("User", foreign_keys=[projet_cpi])
    dp      = db.relationship("User", foreign_keys=[projet_dp])
    client  = db.relationship("Client", foreign_keys=[projet_client])
#---------------------------------------------------------- < CLASS :




#---------------------------------------------------------- > CLASS :
'''
CLASS : Client
'''
class Client(db.Model):
    client_id           = db.Column(db.Integer, primary_key=True)
    client_name         = db.Column(db.String(140))
#---------------------------------------------------------- < CLASS :




#---------------------------------------------------------- > CLASS :
'''
CLASS : Serveur
'''
class Serveur(db.Model):
    __table_args__    = (db.UniqueConstraint('srv_hostname'),)
    srv_id           = db.Column(db.Integer, primary_key=True)
    srv_hostname     = db.Column(db.String(140))
    srv_cpu          = db.Column(db.Float)
    srv_ram          = db.Column(db.Integer)
    srv_pci          = db.Column(db.Boolean)
    srv_os           = db.Column(db.Integer, db.ForeignKey('OS.os_id'))
    os               = db.relationship("OS", foreign_keys=[srv_os])
#---------------------------------------------------------- < CLASS :



#---------------------------------------------------------- > CLASS :
'''
CLASS : IpServeur
'''
class IpServeur(db.Model):
    __table_args__    = (db.UniqueConstraint('ips_serveur','ips_ip' ),)
    ips_id           = db.Column(db.Integer, primary_key=True)
    ips_serveur      = db.Column(db.Integer, db.ForeignKey('serveur.srv_id'))
    ips_ip           = db.Column(db.String(140))
#---------------------------------------------------------- < CLASS :




#---------------------------------------------------------- > CLASS :
'''
CLASS : CompteServeur
'''
class CompteServeur(db.Model):
    __table_args__    = (db.UniqueConstraint('cps_serveur','cps_compte' ),)
    cps_id           = db.Column(db.Integer, primary_key=True)
    cps_serveur       = db.Column(db.Integer, db.ForeignKey('serveur.srv_id'))
    cps_groupe        = db.Column(db.String(140))
    cps_compte        = db.Column(db.String(140))
#---------------------------------------------------------- < CLASS :



#---------------------------------------------------------- > CLASS :
'''
CLASS : Ksu
'''
class Ksu(db.Model):
    ksu_id           = db.Column(db.Integer, primary_key=True)
    ksu_compte       = db.Column(db.Integer, db.ForeignKey('compte_serveur.cps_id'))
    ksu_serveur      = db.Column(db.Integer, db.ForeignKey('serveur.srv_id'))
    ksu_user         = db.Column(db.String(140))
#---------------------------------------------------------- < CLASS :


#---------------------------------------------------------- > CLASS :
'''
CLASS : FileSystem
'''
class FileSystem(db.Model):
    __table_args__    = (db.UniqueConstraint('fs_serveur','fs_montage' ),)
    fs_id           = db.Column(db.Integer, primary_key=True)
    fs_serveur       = db.Column(db.Integer, db.ForeignKey('serveur.srv_id'))
    fs_montage        = db.Column(db.String(140))
    fs_volume        = db.Column(db.Integer)
#---------------------------------------------------------- < CLASS :



#---------------------------------------------------------- > CLASS :
'''
CLASS : OS
'''
class OS(db.Model):
    os_id           = db.Column(db.Integer, primary_key=True)
    os_name         = db.Column(db.String(140))
#---------------------------------------------------------- < CLASS :




#---------------------------------------------------------- > CLASS :
'''
CLASS : ServeurProjet
'''
class ProjetServeur(db.Model):
    #__table_args__ = (db.UniqueConstraint('p_id','s_id'),)
    ps_id          = db.Column(db.Integer, primary_key=True)
    p_id           = db.Column(db.Integer, db.ForeignKey('projet.projet_id'))
    s_id           = db.Column(db.Integer, db.ForeignKey('serveur.srv_id'))
    srv            = db.relationship("Serveur", foreign_keys=[s_id])
#---------------------------------------------------------- < CLASS :



#---------------------------------------------------------- > CLASS :
'''
CLASS : ObjetReseau
'''
class ObjetReseau(db.Model):
    objrezo_id         = db.Column(db.Integer, primary_key=True)
    objrezo_nom        = db.Column(db.String(140))
#---------------------------------------------------------- < CLASS :




#---------------------------------------------------------- > CLASS :
'''
CLASS : IpObjetReseau
'''
class IpObjetReseau(db.Model):
    ior_id         = db.Column(db.Integer, primary_key=True)
    ior_ip         = db.Column(db.String(140),index=True)
    ior_groupe     = db.Column(db.Integer, db.ForeignKey('objet_reseau.objrezo_id'))

    objet          = db.relationship("ObjetReseau", foreign_keys=[ior_groupe])
#---------------------------------------------------------- < CLASS :




#---------------------------------------------------------- > CLASS :
'''
CLASS : rglfw
'''
class Rglfw(db.Model):
    __table_args__ = (db.UniqueConstraint('rglfw_source','rglfw_destination','rglfw_port','rglfw_projet'),)
    rglfw_id            = db.Column(db.Integer, primary_key=True)
    rglfw_source        = db.Column(db.Integer, db.ForeignKey('objet_reseau.objrezo_id'))
    rglfw_destination   = db.Column(db.Integer, db.ForeignKey('objet_reseau.objrezo_id'))
    rglfw_port          = db.Column(db.Integer)
    # 0=non soumis / 1=soumis / 2=traité
    rglfw_etat          = db.Column(db.Integer)
    # date de soumission
    rglfw_date          = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    rglfw_projet        = db.Column(db.Integer, db.ForeignKey('projet.projet_id'))
    rglfw_description   = db.Column(db.String(140),index=True)
    #
    source              = db.relationship("ObjetReseau", foreign_keys=[rglfw_source])
    destination         = db.relationship("ObjetReseau", foreign_keys=[rglfw_destination])
#---------------------------------------------------------- < CLASS :

#----------------------------------------------------- Roadmap


#---------------------------------------------------------- > CLASS :
'''
CLASS : solution
'''
class Solution(db.Model):
    sol_id      = db.Column(db.Integer, primary_key=True)
    sol_nom     = db.Column(db.String(140),index=True)

#---------------------------------------------------------- < CLASS :


#---------------------------------------------------------- > CLASS :
'''
CLASS : roadmap
'''
class Roadmap(db.Model):
    rmp_id      = db.Column(db.Integer, primary_key=True)
    rmp_sol     = db.Column(db.Integer, db.ForeignKey('solution.sol_id'))
    rmp_date    = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    rmp_semaine = db.Column(db.String(5),index=True)
    rmp_fct     = db.Column(db.String(50),index=True)
    rmp_desc    = db.Column(db.Text(200))
    solution    = db.relationship("Solution", foreign_keys=[rmp_sol])
#---------------------------------------------------------- < CLASS :




'''
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    '''
