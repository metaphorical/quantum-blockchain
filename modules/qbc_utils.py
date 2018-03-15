import json

def json_serialize_chain(qbc):
    """
        Getting json serialized QBC
    """
    return json.dumps([{
				"index": str(quant.index),
				"timestamp": str(quant.timestamp),
				"data": str(quant.data),
				"hash": quant.hash,
				"proof": str(quant.proof)
				} for quant in qbc])