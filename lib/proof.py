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

def proof(last_param):
    """
    Applies selected proof algorythm 
    Currently just uses Proof of work.
    TODO: Implement
        * POS - proof of stake
        * DPOS - delegated proof of stake
        * PBFT - practical byzantine fault tolerance
        * POA - proof of authority
    TODO: Implement configurable proof model.
    """
    return proof_of_work(last_param)
  
