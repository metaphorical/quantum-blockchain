from lib.hash import hash_block
from lib.proof import proof

class Quant:
  """
  Smallest piece of QBC is quant of data - a block in the blockchain
  """
  def __init__(self, index, timestamp, data, previous_hash, previous_proof):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.proof = proof(previous_proof)
    self.hash = hash_block(self)
  
  