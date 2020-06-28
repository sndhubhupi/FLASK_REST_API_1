from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_claims, get_jwt_identity
from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be empty'
    )

    parser.add_argument(
        'store_id',
        type= int,
        required=True,
        help='This field cannot be empty'
    )

    @jwt_required
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'Message : Item name : %s already exists ' % (name): 'None'}, 400

        data = Item.parser.parse_args()
        #data = request.get_json()   # force/silent = True
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return({'Message': 'An error occured'} ), 500
        return item.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message' : 'Admin privilege required'} , 401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self,name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):

    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items }
        return {
            'items':[item['name'] for item in items],
            'message':'More data, if login'
        }