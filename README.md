# Distributed systems' class project

The objective of the project is to create a _middleware_ distributed system
capable of communicating itself through different machines.

The system MUST:
1. be able to continue working after any of the nodes is disconnected
2. always have a working master node
3. if there's more than one master node at once, the system must kill on of'em
