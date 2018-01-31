import os
import sys

from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)

def is_exist(currency):
    # file = open('config.ini', 'r')
    file = open(os.path.join(os.path.dirname(sys.argv[0]), 'config.ini'))
    while True:
        line = file.readline()
        if not line: break
        if line.__contains__(currency):
            return True
    return False


class add_user(Resource):
    def post(self):
        try:
            request_parser = reqparse.RequestParser()
            request_parser.add_argument('user_id', type=str)
            args = request_parser.parse_args()

            db = client.wallet
            db.flask_test.insert({'user_id': args['user_id'], 'wallet':{}})
        except Exception as e:
            return {'error': str(e), 'StatusCode': 401}
        return {'result': args['user_id'], 'StatusCode': 200}


class get_balance(Resource):
    """ Use body parameters as needed information """
    def post(self):
        try:
            request_parser = reqparse.RequestParser()
            request_parser.add_argument('user_id', type=str)
            request_parser.add_argument('currency', type=str)
            args = request_parser.parse_args()

            db = client.wallet
            info = db.flask_test.find_one({'user_id': args['user_id']})
            client.close()

            if info is None:
                return {'error': 'User not found', 'StatusCode': 401}

            info = info['wallet']
            try:
                info = info[args['currency']]
            except Exception as e:
                if args['currency'] is not None and args['currency'] != "''":
                    return {'error': args['currency'] + ' doesn\'t exist in your wallet', 'StatusCode': 401}
                pass

            return {'result': info, 'StatusCode': 200}
        except Exception as e:
            return {'error': str(e), 'StatusCode': 401}


class credit(Resource):
    """"""
    def post(self):
        try:
            request_parser = reqparse.RequestParser()
            request_parser.add_argument('user_id', type=str)
            request_parser.add_argument('currency', type=str)
            request_parser.add_argument('amount', type=str)
            request_parser.add_argument('tx_id', type=str)
            args = request_parser.parse_args()

            if not is_exist(args['currency']):
                return {'error': args['currency'] + ' incorrect', 'StatusCode': 401}

            db_transact = client.transaction
            db_userinfo = client.wallet

            tx_id = db_transact.tx_collection.find_one({'tx_id': args['tx_id']})
            if tx_id is not None:
                return {'error': 'Duplicated transactionId. ***Reject*** from server.', 'StatusCode': 401}

            user_info = db_userinfo.flask_test.find_one({'user_id': args['user_id']})
            if user_info is None:
                return {'error': 'User not found.', 'StatusCode': 401}

            wallet = user_info['wallet']
            amount = float(args['amount'])
            try:
                amount += float(wallet[args['currency']])
            except Exception as e:
                pass

            wallet[args['currency']] = amount

            db_userinfo.flask_test.update_one(
                {'_id': user_info['_id']},
                {
                    '$set': {
                        'wallet': wallet
                    }
                }
            )
            db_transact.tx_collection.insert_one({'tx_id': args['tx_id']})

            return {'result': 'Amount of ' + args['currency'] + ' is ' + str(amount), 'StatusCode': 200}
        except Exception as e:
            return {'error': str(e), 'StatusCode': 401}


class debit(Resource):
    def post(self):
        try:
            request_parser = reqparse.RequestParser()
            request_parser.add_argument('user_id', type=str)
            request_parser.add_argument('currency', type=str)
            request_parser.add_argument('amount', type=str)
            request_parser.add_argument('tx_id', type=str)
            args = request_parser.parse_args()


            if not is_exist(args['currency']):
                return {'error': args['currency'] + ' incorrect', 'StatusCode': 401}
            db_transact = client.transaction
            db_userinfo = client.wallet

            tx_id = db_transact.tx_collection.find_one({'tx_id': args['tx_id']})
            if tx_id is not None:
                return {'error': 'Duplicated transactionId. ***Reject*** from server.', 'StatusCode': 401}

            user_info = db_userinfo.flask_test.find_one({'user_id': args['user_id']})
            if user_info is None:
                return {'error': 'User not found.', 'StatusCode': 401}

            wallet = user_info['wallet']
            amount = float(args['amount'])
            try:
                amount = float(wallet[args['currency']]) - amount
            except Exception as e:
                amount = -1

            if amount < 0:
                return {'error': 'Amount of your currency is insufficient.', 'StatusCode': 401}

            wallet[args['currency']] = amount

            db_userinfo.flask_test.update_one(
                {'_id': user_info['_id']},
                {
                    '$set': {
                        'wallet': wallet
                    }
                }
            )
            db_transact.tx_collection.insert_one({'tx_id': args['tx_id']})

            return {'result': 'Amount of ' + args['currency'] + ' is ' + str(amount), 'StatusCode': 200}
        except Exception as e:
            return {'error': str(e), 'StatusCode': 401}


api.add_resource(get_balance, '/getbalance')
api.add_resource(credit, '/credit')
api.add_resource(debit, '/debit')
api.add_resource(add_user, '/adduser')

app.secret_key = 'sxxddj25e$iwrp$zdhgh$sjn0)s*9#*rekptyapb8=bec8!s%z'

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
