# Basic general purpose blockchain in Python

> Purely building this to get the full scope of abilities and pitfalls of building general purpose blockchain. Would love it to grow to something useful but...

## Idea (it will get analized in more depth in whitepaper)

Build general purpose blockchain system that can maintain and fork multiple blockchains for different purposes and accept different data for different blockchains. Build it as general purose solution that can be used as a service in multiservice system to provide blockchain functionality.

## Documentation

* [Whitepaper](documentation/whitepaper.md)
* [Blockchain Digest](documentation/blockchain-digest.md)

## How to contribute

You can fork this repo and work on it. When you create pull requests, I will make sure to review it and merge it as soon as possible.

**If this ever picks up as proper project, I want to give control over it ot group of people so it makes senese to contribute and work on it.

More detailed documentation about contributing and rules will come later, but you can review whitepaper, outline of planed features etc, and you can also review trello board:

[QBC trello](https://trello.com/b/IKDDvvC1/quantum-blockchain)

If you want to contribute, by either idea or doing some work in code (there is a need for lots of that), please ping me at rastko.vukasinovic@gmail.com so we can discuss and I can add you to board so we ca collect all the ideas and proposals and track any work.

Thanks you!

Read following part of docs for a way to run QBC and quickly start working on it.

## QBC Node server

> **NOTE:** At this moment, for dev purposes, flask server will be running in debug mode.

### Running for local development
Install dependencies from requirements.txt

Start server by running

```
python run.py
```
### Running it using Docker - basic
```
docker build -t qbc .
docker run -it -p 5000:5000 qbc
```

### List of basic features

* Accept transactions
* broadcast transactions to known nodes
* Create a block
* Get full chain for comparison
* Basic node registration on the network
* Basic node discovery and distributed registration
* Get chain stats
* Persist blockchain on disc
* Basic bootstrap of the node - when node boots up it reads from the disc and fetches chain stats from known nodes, getting longest chain, or keeping current if longest or same length
* Broadcast new block to all nodes
* [TODO] Check new block on all nodes (chain length check + all other checks)
* [TODO] Make chain stats for comparison (configurable/parametrized) (POW)
* [TODO] Network auth system


### List of additional features:
* [TODO] Multiple proof (consensus) systems
* [TODO] Fork new blockchain
* [TODO] Maintain multiple blockchains on network
* [TODO] Strong validation system
* [TODO] Zero knowledge proof access to data
* [TODO] Other auth / data lock methods

### Support features
* [TODO] Admin UI
* [TODO] Analytics dashboard


## Basic elements

* **Quantum blockchain (QBC)** - this blockcahain
* **Quant** - block in QBC
* **Bang** - creation of new blockchain - genesis block.
* **Transaction** - new data to be added to block
* **Leap** - creating new Quant containing transactions from the pool

### Routes available

* **/inject**
  * [POST] add transaction to transaction pool (transactions waiting ti be added to db)
* **/leap**
  * [GET] add the data to blockchain - mine a block putting all the transactions in transaction pool in.
* **/json-chain**
  * [GET] get whole chain in the node in JSON format
* **/chain**
  * [GET] get whole chain in the node serialized in pickle
* **/discover**
  * [POST] register one node on the system by sending it node host addres like host=address
  * [GET] get currently up to date list of live nodes known to this node
* **/stats**
  * [GET] Get chain stats

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
http -v GET localhost:5000/json-chain
```

## Used third party dependencies

* [Flask](http://flask.pocoo.org/docs/0.12/quickstart/)
* [Requests](http://docs.python-requests.org/en/latest/user/quickstart/)

