def proof_of_work(last_proof):
    """
        Simple proof of work implementation:
        last proof of work gets incremented until next number divisable by last proof and 19 appears
    """
    theproof = int(last_proof) + 1
    print theproof
    while not (theproof % 19 == 0 and theproof % int(last_proof) == 0):
        theproof += 1
    return theproof

def validate_pow(last_proof, theproof):
    """
        Confirm that provided proof is actually the next block
    """
    return (theproof % 19 == 0 and theproof % int(last_proof) == 0)

def delegated_block_creation(last_proof):
    """
        This is no proof system since it just returns order number of block.
        Private chain implementation is considered to be in place.
    """
    return last_proof + 1

def proof(last_param):
    """
    Applies selected proof algorythm 
    Currently just uses Proof of work.
    TODO: Implement
        * DBC - delegated block creation
        * POS - proof of stake
        * DPOS - delegated proof of stake
        * POA - proof of authority
    TODO: Implement configurable proof model.
    """
    return proof_of_work(last_param)
  
def validate(last_proof, theproof):
    """
        Implement validation switching based on which consensus system is used
    """
    return validate_pow(last_proof, theproof)