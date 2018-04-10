# Quantum blockchain (QBC)

Blockchain solution for everyday multi service application. 

## Purpose

Main purpose of QBC is to be as generelly useful to anyone wanting to remove single point of failure and strengten data security by having decentralized and secure database. Idealy, this solution should reduce throughput of the system as little as possible.

QBC is built with integration and decoupling possibilities in mind, with idea to provide nice APIs and multi variant configurable solution. 

## What is general purpose blockchain

**In short:** It is general purpose database that is fully replicated across arbitrary number of nodes.

For more detailed answer we got to look at long list of resources I prepared [here](). Just a glance at content of given document tells you that world is still figuring out what is blockchain and what exactly this new piece of tech is able to solve for us.

On the other hand, what is basic set of features general purpose blockchain should have?

## Base set of features needed to be generally applicable

### It should be a tool, not a star of the system

Obviously, if we are building something to be generally used as a suplement to applications, we should have something that is:
* Easy to deploy
* Highly configurable (it should adopt to needs of a system, not vice versa)
* Integration into the system should be super simple (e.g. you deploy and configure it and after that it all goes through simple RESTful API)

### It should have multiple consensus algorythms

Consensus algorythms (AKA proof systems) are important for blockchain to function properly. They ensure proper work distribution, provide security to data storage, and are responsible for data integrity. 

General purpose blockchain should provide set of initial, selectable methods to find consensus. 

**I suggest following set of algorythms**

* **PBFT** - Practical Byzantine Fault Tolerance algorithm
* **PoW** - Proof-of-work algorithm
* **Pos** - Proof-of-stake algorithm
* **DPoS** - Delegated proof-of-stake algorithm

It should additionally provide a way to write and use new algorythm.

