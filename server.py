import json, sys, requests, pickle

from flask import Flask, request

import hashlib as hasher

from modules.chain import Chain
from modules.network import discover_network, broadcast_quant
from modules.transactions import broadcast_transaction

system_config = json.load(open('./config/system_preferences.json'))

QBC = Chain()
node = Flask(__name__)

live_nodes = system_config["genesis_nodes"]
waiting_transactions = []
port = int(sys.argv[1]) if (len(sys.argv) >= 2) else 5000

@node.route('/inject', methods=['POST', 'PUT'])
# Route to inject transaction (put in waiting queue)
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
# Route to trigger ad hoc mining
# TODO: make mining configurable and automathic so POS and DPOS can be implemented
def generate_block():
  	if request.method == 'GET':
	  	# Below is super simple, the idea is to have decision model on number of transactions and 
		# also which transactions go in
		global waiting_transactions
		global live_nodes
		global port
		print "Starting leap"
		new_quant_data = waiting_transactions
		waiting_transactions = []
		new_quant = QBC.create_quant(new_quant_data)
		print new_quant
		broadcast_quant(live_nodes, new_quant, port)
		print "Quantum leap"	
		return "block creation successful\n"

@node.route('/json-chain', methods=['GET'])
# Route to get chain in JSON format
def serve_json_qbc():
	if request.method == 'GET':
		return QBC.get_chain("json")

@node.route('/chain', methods=['GET'])
# Route to get chain in Pickel format
def serve_qbc():
	if request.method == 'GET':
		return QBC.get_chain("serialized")

@node.route('/stats', methods=['GET'])
# Route to get Node stats
def chain_stats():
		return QBC.get_chain_stats()

@node.route('/add-block', methods=['POST'])
# Route to simply submit new, just mined block to this node
def add_block():
		if request.method == 'POST':
			new_quant_pickle = request.get_json()['quant']
			new_quant = pickle.loads(new_quant_pickle)
			QBC.add_quant(new_quant)
			# TODO: better detection if it succided
			return "Success"

@node.route('/discover', methods=['POST', 'GET'])
# Register new node if not already registered
def register_node():
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

# TODO: make deteriming genesis node proper - currently, first node is detected by looking at port (if it is 5000 it is base node) - better way is ot look into config and comparing within network module, thus shielding from implementation.
# Discover full network and register on each of the nodes
network=discover_network(port==5000,live_nodes=live_nodes, port=port)
live_nodes=network["registered_nodes"]

if port!=5000 and json.loads(QBC.get_chain_stats())["length"] < network["longest_chain_length"]:
	QBC.get_remote_node_chain(network["longest_chain_node"])


node.run(host='0.0.0.0', port=port, debug=True)