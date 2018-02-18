# Basic general purpose blockchain in Python

> Purely building this to get the full scope of abilities and pitfalls of building general purpose blockchain. Would love it to grow to something useful but... 

## Idea (it will get analized in more depth in whitepaper)

Build general purpose blockchain system that can maintain and fork multiple blockchains for different purposes and accept different data for different blockchains.

Ideally apart of having abilit y to distribute data to different nodes, give it ability to distribute blockchains across same nodes as well.

## Basic elements

* **Quantum blockchain (QBC)** - this blockcahain 
* **Quant** - block in QBC
* **Bang** - creation of new blockchain - genesis block.

## QBC Node server

Install dependencies from requirements.txt

Start server by running

```
python server.py
```

### Routes available

* **/quant** - [POST] add the data to blockchain
* **/chain** - [GET] get whole chain in the node

### To test server while running

Using [httpie](https://httpie.org/) :

Add block of data to blockchain:
```
http -v POST localhost:5000/quant this=is your="quant data"
```

Get blockchain in JSON format:
```
http -v GET localhost:5000/chain
```