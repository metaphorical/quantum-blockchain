# Basic general purpose blockchain in Python

> Purely building this to get the full scope of abilities and pitfalls of building general purpose blockchain. Would love it to grow to something useful but... 

## Idea (it will get analized in more depth in whitepaper)

Build general purpose blockchain system that can maintain and fork multiple blockchains for different purposes and accept different data for different blockchains.

Ideally apart of having abilit y to distribute data to different nodes, give it ability to distribute blockchains across same nodes as well.

I guess what would give value to idea of implementing it like this is that it would ideally be one service in your echosystem that has ability to provide you with blockchain database to server your needs for sequential immutable database(s).

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
**NOTE:** At this moment, for dev purposes, flask server will running in debug mode.

### Routes available

* **/quant** 
  * [POST] add the data to blockchain
* **/chain** 
  * [GET] get whole chain in the node
* **/discover** 
  * [POST] register one node on the system by sending it node host addres like host=address
  * [GET] get currently up to date list of live nodes known to this node

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