import pickle

from flask import Blueprint, request

from lib.chain import Chain

chain_blueprint = Blueprint('chain', __name__)

@chain_blueprint.route('/add-block', methods=['POST'])
# Route to simply submit new, just mined block to this node
def add_block():
	QBC = Chain()
	if request.method == 'POST':
		new_quant_pickle = request.get_json()['quant']
		new_quant = pickle.loads(new_quant_pickle)
		QBC.add_quant(new_quant)
		# TODO: better detection if it succided
		return "Success"

@chain_blueprint.route('/json-chain', methods=['GET'])
# Route to get chain in JSON format
def serve_json_qbc():
	QBC = Chain()
	if request.method == 'GET':
		return QBC.get_chain("json")

@chain_blueprint.route('/chain', methods=['GET'])
# Route to get chain in Pickel format
def serve_qbc():
	QBC = Chain()
	if request.method == 'GET':
		return QBC.get_chain("serialized")

@chain_blueprint.route('/stats', methods=['GET'])
# Route to get Node stats
def chain_stats():
	QBC = Chain()
	return QBC.get_chain_stats()