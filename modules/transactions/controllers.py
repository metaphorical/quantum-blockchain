from flask import Blueprint, request

from lib.transactions import Transactions
from lib.qbc_utils import QbcUtils
from lib.network import Network

transactions_blueprint = Blueprint('transactions', __name__)
QBCN = Network()
QBCT = Transactions()
QBCU = QbcUtils()

@transactions_blueprint.route('/inject', methods=['POST', 'PUT'])
# Route to inject transaction (put in waiting queue)
def add_transaction():
    waiting_transactions = QBCT.load_transactions()
    live_nodes = QBCN.load_nodes()
    port = QBCU.get_port()
    # add transaction to waiting list
    if request.method == 'POST':
        waiting_transactions.append(request.get_json()['data'])
        QBCT.save_transactions(waiting_transactions)
        print "New transaction added"
        print "{}".format(request.get_json()['data'])
        QBCT.broadcast_transaction(live_nodes, request.get_json()['data'], port)
        return "Transaction submission successful\n"
    # receive transaction from known node on the network
    if request.method == 'PUT':
        waiting_transactions.append(request.get_json()['data'])
        QBCT.save_transactions(waiting_transactions)
        print "ip of node sending transaction - {}".format(request.remote_addr)
        print "New transaction added by the network"
        print "{}".format(request.get_json())
        return "Transaction submission successful\n"