import json, sys, requests, pickle

from flask import Flask, request

import hashlib as hasher

from lib.chain import Chain
from lib.network import discover_network, broadcast_quant, load_nodes, save_nodes
from lib.qbc_utils import get_port, is_genesis_node

from modules.transactions.controllers import transactions_blueprint
from modules.mining.controllers import mining_blueprint
from modules.network.controllers import network_blueprint
from modules.chain.controllers import chain_blueprint

system_config = json.load(open('./config/system_preferences.json'))

node = Flask(__name__)

QBC = Chain()
port = get_port()

# Registering all the modules
node.register_blueprint(transactions_blueprint)

node.register_blueprint(mining_blueprint)

node.register_blueprint(network_blueprint)

node.register_blueprint(chain_blueprint)


# Discover full network and register on each of the nodes
network=discover_network()
live_nodes=network["registered_nodes"]

if not is_genesis_node() and json.loads(QBC.get_chain_stats())["length"] < network["longest_chain_length"]:
	save_nodes(live_nodes)
	QBC.get_remote_node_chain(network["longest_chain_node"])


node.run(host='0.0.0.0', port=port, debug=True)