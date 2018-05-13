import json

from flask import Blueprint, request

from lib.network import load_nodes, save_nodes
from lib.chain import Chain

network_blueprint = Blueprint('network', __name__)

@network_blueprint.route('/discover', methods=['POST', 'GET'])
# Register new node if not already registered
def register_node():
	live_nodes = load_nodes()
	QBC = Chain()
	if request.method == 'GET':
		return json.dumps(live_nodes)
	if request.method == 'POST':
            # import pdb; pdb.set_trace()
            new_host = request.get_json()['host']
            if not (new_host in live_nodes):
                live_nodes.append(new_host)
                save_nodes(live_nodes)
            return json.dumps({
                    "live_nodes": live_nodes,
                    "stats": json.loads(QBC.get_chain_stats())
                })