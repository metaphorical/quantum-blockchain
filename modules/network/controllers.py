import json

from flask import Blueprint, request

from lib.network import Network
from lib.chain import Chain

network_blueprint = Blueprint('network', __name__)
QBC = Chain()
QBCN = Network()

@network_blueprint.route('/discover', methods=['POST', 'GET'])
# Register new node if not already registered
def register_node():
	live_nodes = QBCN.load_nodes()
	if request.method == 'GET':
		return json.dumps(live_nodes)
	if request.method == 'POST':
            # import pdb; pdb.set_trace()
            new_host = request.get_json()['host']
            if not (new_host in live_nodes):
                live_nodes.append(new_host)
                QBCN.save_nodes(live_nodes)
            return json.dumps({
                    "live_nodes": live_nodes,
                    "stats": json.loads(QBC.get_chain_stats())
                })