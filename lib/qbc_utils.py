import json, socket, sys

system_config = json.load(open('./config/system_preferences.json'))
class QbcUtils:
    def get_current_ip(self):
        return socket.gethostbyname(socket.gethostname())

    def get_port(self):
        return int(sys.argv[1]) if (len(sys.argv) >= 2) else 5000

    def parse_localhost(self, new_node):
        """
            for testing purposes, for node to communicate inside same machine,
            we need to parse all the IP addresses and replace current machine ones with localhost
        """
        current_node_ip = self.get_current_ip()
        if current_node_ip not in new_node:
            node_addr = new_node
        else:
            node_addr = new_node.replace(current_node_ip, "localhost")
        return node_addr

    def get_hostname(self, ip, port):
        # TODO: handle different protocols
        return "http://{}:{}".format(ip, port)

    def is_genesis_node(self):
        """
            Shows if current node belongs to list of initial nodes
            (it usually mean that those will stay longest time - i.e. forever)
        """
        genesis_nodes = system_config["genesis_nodes"]
        this_node = self.get_hostname(self.get_current_ip(), self.get_port())
        return this_node in genesis_nodes or self.parse_localhost(this_node) in genesis_nodes