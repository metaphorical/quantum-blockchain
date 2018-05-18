import os, requests, json

from lib.qbc_utils import parse_localhost, get_current_ip, get_port, get_hostname

# TODO: All the saves and loads should be improved by adding in memory storage for performance and encryption for security

class Transactions:
    def broadcast_transaction(self, nodes, transaction, port):
        node_ip = get_current_ip()
        port = get_port()
        this_node = parse_localhost(get_hostname(node_ip, port))
        for node in nodes:
            node = parse_localhost(node)
            if node != this_node:
                r = requests.put("{}/inject".format(node), json={"data":transaction})
                print(r.text)

    def load_transactions(self):
        with open(os.path.join(os.getcwd(),'storage', 'transactions.json'), 'rb') as transactions_file:
                return json.load(transactions_file)

    def save_transactions(self, transactions):
        with open(os.path.join(os.getcwd(),'storage', 'transactions.json'), 'wb') as fp:
                json.dump(transactions, fp)