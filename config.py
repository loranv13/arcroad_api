import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://loran:loranv@192.168.30.21/arcroadp_beta'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY        = 'incimdsosbdvoduvboqozuvhihiHIHI%HHihcichùehHIHZ'

    JWT_TOKEN_LOCATION        = ['cookies']
    JWT_ACCESS_COOKIE_PATH    = '/'
    JWT_REFRESH_COOKIE_PATH   = '/refresh'
    JWT_COOKIE_CSRF_PROTECT   = False
    JWT_SECRET_KEY            = 'scdvbbfdb5fdbsdfbDZSDd5d6zd54DZBG::E$'
    JWT_USER_CLAIMS           = 'info'
    JWT_ACCESS_TOKEN_EXPIRES  = False



