import json

from flask import Flask
from flask import request

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

@node.route('/quant', methods=['POST'])
def add_block():
  if request.method == 'POST':
		new_quant_data = request.get_json()
		new_quant = create_next_quant(last_quant, new_quant_data)
		local_qbc.append(new_quant)
		print "New block added"	
		print "{}".format(new_quant)
		return "Submission successful\n"

@node.route('/chain', methods=['GET'])
def serve_qbc():
	if request.method == 'GET':
		exported_qbc = [{
				"index": str(quant.index),
				"timestamp": str(quant.timestamp),
				"data": str(quant.data),
				"hash": quant.hash
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



node.run(port=5000, debug=True)