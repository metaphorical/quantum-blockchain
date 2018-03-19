import datetime as date
from modules.quant import Quant

class Chain:
    """
    QBC structure implementation
    """
    def __init__(self):
        self.qbc = [__bang()]
        self.current_quant = self.qbc[0]

    def __bang():
        """Bang starts new blockchain creating what is known as 'genesis block'"""
        return Quant(0, date.datetime.now(), "Small Bang", "0", "1")

    def __create_next_quant(last_quant, data):
        this_index = last_quant.index + 1
        this_timestamp = date.datetime.now()
        this_data = data
        last_hash = last_quant.hash
        last_proof = last_quant.proof
        return Quant(this_index, this_timestamp, this_data, last_hash, last_proof)
    
    def create_quant(last_quant, data);
        self.qbc.append(__create_next_quant(last_quant, data))
        self.current_quant = self.qbc[len(self.qbc) - 1]
