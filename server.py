import json, sys, requests, socket

from flask import Flask, request


from modules.creation import bang, create_next_quant
from modules.quant import Quant

system_config = json.load(open('./config/system_preferences.json'))


node = Flask(__name__)

local_qbc = [bang()]
last_quant = local_qbc[0]
live_nodes = system_config["genesis_nodes"]
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
	#Register new node if not already registered
	global live_nodes
	if request.method == 'GET':
		return json.dumps(live_nodes)
	if request.method == 'POST':
		new_host = request.get_json()['host']
		if not (new_host in live_nodes):
			live_nodes.append(new_host)
		return "SUCCESS!!!"




port = int(sys.argv[1]) if (len(sys.argv) >= 2) else 5000

# registering on the network, currently no channel to broadcast, so we can use ping to everyone in the list
if port != 5000:
	for qbc_node in live_nodes:
		discover_payload = {'host': "http://{}:{}".format(socket.getfqdn(), port)}
		requests.post("{}/discover".format(qbc_node), json=discover_payload)
		print("REGISTERING")
		print(socket.getfqdn())
		print(port)

node.run(port=port, debug=True)