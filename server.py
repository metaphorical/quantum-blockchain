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
		return json.dumps(live_nodes)




port = int(sys.argv[1]) if (len(sys.argv) >= 2) else 5000

# registering on the network, currently no channel to broadcast, so we can use ping to everyone in genesis nodes list
# TODO: discover and register on new peers by getting data about peers registered on network
# TODO: implement timeout for request and fallback... Probably hardcoded genesis node should be fallback and some (maybe serverless?) discovery mechanism should be created
# TODO: review ip fetching, must be less hacky way
if port != 5000:
	node_ip = socket.gethostbyname(socket.gethostname())
	this_node = "http://{}:{}".format(node_ip, port)
	new_nodes = []
	for qbc_node in live_nodes:
		discover_payload = {'host': this_node}
		register_request = requests.post("{}/discover".format(qbc_node), json=discover_payload)
		print(register_request.text)
		hosts_from_node = json.loads(register_request.text)
		new_nodes += [x for x in hosts_from_node if (x != this_node and x not in live_nodes)]
		print(json.dumps(new_nodes))
		if(len(new_nodes) > 0):
			live_nodes += new_nodes
			for new_node in new_nodes:
				if node_ip not in new_node:
					node_addr = new_node
				else:
					node_addr = new_node.replace(node_ip, "localhost")
				print(node_addr)
				discover_payload = {'host': this_node}
				register_request = requests.post("{}/discover".format(node_addr), json=discover_payload)
				print(register_request.text)
		else:
			print("I guess this is second node on the network...")				

node.run(port=port, debug=True)