import json, sys, requests

from flask import Flask, request

import hashlib as hasher

from modules.chain import Chain
from modules.network import discover_network
from modules.transactions import broadcast_transaction

system_config = json.load(open('./config/system_preferences.json'))

QBC = Chain()
node = Flask(__name__)

live_nodes = system_config["genesis_nodes"]
waiting_transactions = []
port = int(sys.argv[1]) if (len(sys.argv) >= 2) else 5000

@node.route('/inject', methods=['POST', 'PUT'])
# Inject transaction (put in waiting queue)
def add_transaction():
	# add transaction to waiting list
  	if request.method == 'POST':
	  	waiting_transactions.append(request.get_json()['data'])
		print "New transaction added"	
		print "{}".format(request.get_json()['data'])
		broadcast_transaction(live_nodes, request.get_json()['data'], port)
		return "Transaction submission successful\n"
	# receive transaction from known node on the network
  	if request.method == 'PUT':
	  	waiting_transactions.append(request.get_json()['data'])
		print "ip of node sending transaction - {}".format(request.remote_addr)
		print "New transaction added by the network"	
		print "{}".format(request.get_json())
		return "Transaction submission successful\n"
		
	

@node.route('/leap', methods=['GET'])
# Ad hoc mining - TODO: make this more configurable and automathic so POS and DPOS can be implemented
def add_block():
  	if request.method == 'GET':
	  	# Below is super simple, the idea is to have decision model on number of transactions and 
		# also which transactions go in
		global waiting_transactions
		new_quant_data = waiting_transactions
		waiting_transactions = []
		QBC.create_quant(new_quant_data)
		print "Quantum leap"	
		return "block creation successful\n"

@node.route('/chain', methods=['GET'])
def serve_qbc():
	if request.method == 'GET':
		return QBC.get_json_chain()

@node.route('/stats', methods=['GET'])
def chain_stats():
		return QBC.get_chain_stats()

@node.route('/discover', methods=['POST', 'GET'])
def register_node():
	#Register new node if not already registered
	global live_nodes
	if request.method == 'GET':
		return json.dumps(live_nodes)
	if request.method == 'POST':
		new_host = request.get_json()['host']
		if not (new_host in live_nodes):
			live_nodes.append(new_host)
		return json.dumps({
				"live_nodes": live_nodes,
				"stats": json.loads(QBC.get_chain_stats())
			})



# Discover full network and register on each of the nodes
live_nodes=discover_network(port==5000,live_nodes=live_nodes, port=port)["registered_nodes"]			

node.run(port=port, debug=True)