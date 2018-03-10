# Basic general purpose blockchain in Python

> Purely building this to get the full scope of abilities and pitfalls of building general purpose blockchain. Would love it to grow to something useful but... 

## Idea (it will get analized in more depth in whitepaper)

Build general purpose blockchain system that can maintain and fork multiple blockchains for different purposes and accept different data for different blockchains. Build it as general purose solution that can be used as a service in multiservice system to provide blockchain functionality.

List of basic features

* Accept transactions
* Create a block
* Get full chain for comparison
* [TODO] Get chain stats for comparison (POW)
* [TODO] Basic node discovery and node registration on the network
* [TODO] Basic bootstrap of the node
* [TODO] Broadcast new block to all nodes
* [TODO] Chack new block on all nodes (chain length check + all other checks)


List of additional features:
* [TODO] Multiple proof (consensus) systems
* [TODO] Fork new blockchain
* [TODO] Maintain multiple blockchains on network
* [TODO] Strong validation system
* [TODO] Zero knowledge proof access to data
* [TODO] Other auth / data lock methods


## Basic elements

* **Quantum blockchain (QBC)** - this blockcahain 
* **Quant** - block in QBC
* **Bang** - creation of new blockchain - genesis block.
* **Transaction** - new data to be added to block
* **Leap** - creating new Quant containing transactions from the pool

## QBC Node server

Install dependencies from requirements.txt

Start server by running

```
python server.py
```
**NOTE:** At this moment, for dev purposes, flask server will be running in debug mode.

### Routes available

* **/inject** 
  * [POST] add transaction to transaction pool (transactions waiting ti be added to db)
* **/leap** 
  * [GET] add the data to blockchain - mine a block putting all the transactions in transaction pool in.
* **/chain** 
  * [GET] get whole chain in the node
* **/discover** 
  * [POST] register one node on the system by sending it node host addres like host=address
  * [GET] get currently up to date list of live nodes known to this node

### To test server while running

Using [httpie](https://httpie.org/) :

Add transaction to node (put on waiting list aka transaction pool):

```
http -v POST localhost:5000/inject data="{\"test\":\"test2\"}"
```

Add block of data to blockchain:
```
http -v GET localhost:5000/leap
```

Get blockchain in JSON format:
```
http -v GET localhost:5000/chain
```