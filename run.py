import json, sys, requests, pickle

from flask import Flask, request

import hashlib as hasher

from lib.chain import Chain
from lib.network import discover_network, broadcast_quant, load_nodes, save_nodes
from lib.qbc_utils import get_port, is_genesis_node

from modules.transactions.controllers import transactions_blueprint
from modules.mining.controllers import mining_blueprint
from modules.network.controllers import network_blueprint

system_config = json.load(open('./config/system_preferences.json'))

node = Flask(__name__)

QBC = Chain()
port = get_port()

# Registering all the modules using blueprints
# TODO leap (mine), chain, stats, add-block
node.register_blueprint(transactions_blueprint)

node.register_blueprint(mining_blueprint)

node.register_blueprint(network_blueprint)

@node.route('/json-chain', methods=['GET'])
# Route to get chain in JSON format
def serve_json_qbc():
	QBC = Chain()
	if request.method == 'GET':
		return QBC.get_chain("json")

@node.route('/chain', methods=['GET'])
# Route to get chain in Pickel format
def serve_qbc():
	QBC = Chain()
	if request.method == 'GET':
		return QBC.get_chain("serialized")

@node.route('/stats', methods=['GET'])
# Route to get Node stats
def chain_stats():
	QBC = Chain()
	return QBC.get_chain_stats()

@node.route('/add-block', methods=['POST'])
# Route to simply submit new, just mined block to this node
def add_block():
	QBC = Chain()
	if request.method == 'POST':
		new_quant_pickle = request.get_json()['quant']
		new_quant = pickle.loads(new_quant_pickle)
		QBC.add_quant(new_quant)
		# TODO: better detection if it succided
		return "Success"

# Discover full network and register on each of the nodes
network=discover_network()
live_nodes=network["registered_nodes"]

if not is_genesis_node() and json.loads(QBC.get_chain_stats())["length"] < network["longest_chain_length"]:
	save_nodes(live_nodes)
	QBC.get_remote_node_chain(network["longest_chain_node"])


node.run(host='0.0.0.0', port=port, debug=True)