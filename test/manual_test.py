import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from modules.creation import bang, create_next_quant
from modules.quant import Quant

# Put the new chain there with a bang
blockchain = [bang()]
previous = blockchain[0]

# How many Quants should test add after the bang
quants_to_add = 10

# Add blocks to the chain
for i in range(0, quants_to_add):
  next_quant = create_next_quant(previous)
  blockchain.append(next_quant)
  previous = next_quant
  # Tell everyone about it!
  print "Quant #{} has been added to the QBC!".format(next_quant.index)
  print "Hash: {}\n".format(next_quant.hash) 