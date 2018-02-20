import hashlib as hasher

def hash_block(quant):
    """
        Method to generate fingerprint for the next block.
        It is ideal for fingerprint to be the hash of some combination of all the blocks comonents
    """
    sha = hasher.sha256()
    sha.update(str(quant.index) + 
               str(quant.timestamp) + 
               str(quant.data) + 
               str(quant.previous_hash))
    return sha.hexdigest()