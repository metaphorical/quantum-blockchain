import datetime as date
from modules.quant import Quant

def bang():
  """Bang starts new blockchain creating what is known as 'genesis block'"""
  return Quant(0, date.datetime.now(), "Small Bang", "0", "1")

def create_next_quant(last_quant, data):
  this_index = last_quant.index + 1
  this_timestamp = date.datetime.now()
  this_data = data
  last_hash = last_quant.hash
  last_proof = last_quant.proof
  return Quant(this_index, this_timestamp, this_data, last_hash, last_proof)