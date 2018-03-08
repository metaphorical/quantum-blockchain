import json

import sys

from flask import Flask, request


from modules.creation import bang, create_next_quant
from modules.quant import Quant



node = Flask(__name__)
"""
Basic blockchain sever with ability to 

* register self on the system
* accept data to insert
* register new node form the system
* send local chain stats
* send local chain

"""
local_qbc = [bang()]
last_quant = local_qbc[0]
live_nodes = []
waiting_transactions = []

@node.route('/inject', methods=['POST'])
# Inject transaction (put in waiting queue)
def add_transaction():
	# add transaction to waiting list
  	if request.method == 'POST':
	  	waiting_transactions.append(request.get_json()['data'])
		print "New transaction added"	
		print "{}".format(request.get_json()['data'])
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
		new_quant = create_next_quant(last_quant, new_quant_data)
		local_qbc.append(new_quant)
		print "Quantum leap"	
		print "{}".format(new_quant)
		return "block creation successful\n"

@node.route('/chain', methods=['GET'])
def serve_qbc():
	if request.method == 'GET':
		exported_qbc = [{
				"index": str(quant.index),
				"timestamp": str(quant.timestamp),
				"data": str(quant.data),
				"hash": quant.hash,
				"proof": str(quant.proof)
				} for quant in local_qbc]
				
		exported_qbc = json.dumps(exported_qbc)
		return exported_qbc

@node.route('/discover', methods=['POST', 'GET'])
def register_node():
	if request.method == 'GET':
		return json.dumps(live_nodes)
	if request.method == 'POST':
		live_nodes.append(request.get_json()['host'])
		return "SUCCESS!!!"




port = int(sys.argv[1]) if (len(sys.argv) >= 2) else 5000

node.run(port=port, debug=True)