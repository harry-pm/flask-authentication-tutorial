from run import db
from passlib.hash import pbkdf2_sha256 as sha256 #encodes passwords

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    #if username exists in db, it will return username
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()
    
    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }
        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    #generate a hashed string
    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    
    # will check the given password.
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

#cannot delete tokens on client side as they will still be valid as long as they don’t expire, we need to add these tokens to the blacklist. Then you need to check all incoming tokens against the blacklist and if there is a match — disallow access.
class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))#unique identifier of token

    #adds token to db
    def add(self):
        db.session.add(self)
        db.session.commit()

    #checks if token is revoked
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)
