# Distributed systems' class project

The objective of the project is to create a _middleware_ distributed system
capable of communicating itself through different machines.

The system MUST:
1. be able to continue working after any of the nodes is disconnected
2. always have a working master node
3. if there's more than one master node at once, the system must kill on of'em

## Setup
[virtualenv](https://pypi.python.org/pypi/virtualenv) is encouraged for ease of
installation. Also [pip](https://pypi.python.org/pypi/pip/), python 3 (tested
with 3.5) is required. After cloning the repo, run the following commands.

```bash
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
# Then just run the program
$ ./nier.py
```
