*Introduction
This repository contains the codebase for implementing proximity marketing using various consensus algorithms. Consensus algorithms are fundamental in distributed systems for achieving reliability and fault-tolerance. In the context of proximity marketing, they ensure consistency and coordination among distributed marketing nodes.

*Algorithms
-Paxos
Paxos is a family of protocols for solving consensus in a network of unreliable processors. It is designed to be fault-tolerant and ensures that a single value is chosen and agreed upon by the majority of nodes.

-Raft
Raft is a consensus algorithm that is designed to be more understandable than Paxos. It achieves consensus by electing a leader among the nodes, which then manages the replication of log entries.

-PBFT
Practical Byzantine Fault Tolerance (PBFT) is an algorithm designed to tolerate Byzantine faults, where nodes may behave arbitrarily or maliciously. It ensures consensus even in the presence of faulty nodes.

*Usage
Each consensus algorithm implementation can be found in its respective directory. 
