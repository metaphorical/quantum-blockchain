from flask import Blueprint, request

from lib.transactions import broadcast_transaction, load_transactions, save_transactions

def construct_transaction_blueprint(live_nodes, port):

    transactions_blueprint = Blueprint('transactions', __name__)

    @transactions_blueprint.route('/inject', methods=['POST', 'PUT'])
    # Route to inject transaction (put in waiting queue)
    def add_transaction():
        waiting_transactions = load_transactions()
        # add transaction to waiting list
        if request.method == 'POST':
            waiting_transactions.append(request.get_json()['data'])
            save_transactions(waiting_transactions)
            print "New transaction added"	
            print "{}".format(request.get_json()['data'])
            broadcast_transaction(live_nodes, request.get_json()['data'], port)
            return "Transaction submission successful\n"
        # receive transaction from known node on the network
        if request.method == 'PUT':
            waiting_transactions.append(request.get_json()['data'])
            save_transactions(waiting_transactions)
            print "ip of node sending transaction - {}".format(request.remote_addr)
            print "New transaction added by the network"	
            print "{}".format(request.get_json())
            return "Transaction submission successful\n"

    return transactions_blueprint