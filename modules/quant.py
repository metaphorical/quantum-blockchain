from modules.hash import hash_block

class Quant:
  """
  Smallest piece of QBC is quant of data - a block in the blockchain
  """
  def __init__(self, index, timestamp, data, previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = hash_block(self)
  
  