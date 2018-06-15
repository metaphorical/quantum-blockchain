import datetime as date
import json, pickle, os
import hashlib as hasher

from lib.quant import Quant
from lib.network import Network

# TODO: All the saves and loads should be improved by adding in memory storage for performance and encryption for security
QBCN = Network()

class Chain:
    """
    QBC structure implementation
    """
    def __init__(self):
        # If there is locally storred chain it should be read and used on init
        # (instead of basic initiation of genesis block)
        if(os.path.exists(os.path.join(os.getcwd(),'storage', 'q.bc'))):
            self.qbc = Chain.__read_chain_from_disc()
        else:
            self.qbc = [Chain.__bang()]
            self.save()
        self.current_quant = self.qbc[0]

    @classmethod
    def __bang(self):
        """Bang starts new blockchain creating what is known as 'genesis block'"""
        return Quant(0, date.datetime.now(), "Small Bang", "0", "1")
    @classmethod
    def __create_next_quant(self, last_quant, data):
        """
            Creates next block in Quantum Blockchain, known as Quant
        """
        this_index = last_quant.index + 1
        this_timestamp = date.datetime.now()
        this_data = data
        last_hash = last_quant.hash
        last_proof = last_quant.proof
        return Quant(this_index, this_timestamp, this_data, last_hash, last_proof)
    @classmethod
    def __read_chain_from_disc(self):
        with open(os.path.join(os.getcwd(),'storage', 'q.bc'), 'rb') as qbc_file:
            return pickle.load(qbc_file)

    def get_chain_stats(self):
        sha = hasher.sha256()
        sha.update(self.get_chain("json"))
        return json.dumps({
                "length": len(self.get_chain()),
                "hash": sha.hexdigest()
                })

    def create_quant(self, data):
        """
            Public method to add new quatn to QBC
        """
        new_quant = Chain.__create_next_quant(self.current_quant, data)
        self.qbc.append(new_quant)
        self.current_quant = self.qbc[len(self.qbc) - 1]
        Chain.save(self)
        return new_quant

    def add_quant(self, quant):
        """
            Add Quant to QBC
        """
        self.qbc.append(quant)
        self.current_quant = self.qbc[len(self.qbc) - 1]
        Chain.save(self)

    def get_chain(self, format="default"):
        return {
            "json": json.dumps([{
                        "index": str(quant.index),
                        "timestamp": str(quant.timestamp),
                        "data": str(quant.data),
                        "hash": quant.hash,
                        "proof": str(quant.proof)
                        } for quant in self.qbc]),
            "serialized": pickle.dumps(self.qbc)
        }.get(format, self.qbc)

    def save(self):
        """
            Storing QBC on disc serialized using pickle
            TODO: introduce encryption
        """
        with open(os.path.join(os.getcwd(),'storage', 'q.bc'), 'wb') as fp:
            pickle.dump(self.qbc, fp)
    def load(self):
        self.qbc = self.__read_chain_from_disc()

    def get_remote_node_chain(self, host):
        """
            Downloads chain in bickle format and sets it into qbc

            TODO: In order to develop and test I need to first finish dockerizing
            and preset for 2 or 3 node testing setup to emulate different lengths
            and chain diverging events.
        """
        remote_chain = QBCN.read_chain(host)
        self.qbc = pickle.loads(remote_chain)
        self.save()