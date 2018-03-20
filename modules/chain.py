import datetime as date
from modules.quant import Quant

class Chain:
    """
    QBC structure implementation
    """
    def __init__(self):
        self.qbc = [Chain.__bang()]
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
    
    def create_quant(self, data):
        """
            Public method to add new quatn to QBC
        """
        self.qbc.append(Chain.__create_next_quant(self.current_quant, data))
        self.current_quant = self.qbc[len(self.qbc) - 1]

    def get_chain(self):
        return self.qbc
