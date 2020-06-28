import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

#from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'  #app.config['JWT_SECRET_KEY']
api = Api(app)


#jwt = JWT(app, authenticate, identity)  # /auth
jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claim_to_jwt(identity):
    if identity ==2:
        return {'is_admin' : True}
    return {'is_admin' : False}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin,'/login')



if __name__ == '__main__':
    app.run(port=5000, debug= True)

