from arcroad import db, login
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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
