# svd-benchmarking

Assumptions
1. Since the platform will actually run on a AWS EMR Cluster and would use multiple nodes, hence using 4 node machines for benchmarking


Benchmarks shared at 
https://docs.google.com/spreadsheets/d/1hU29CpoGmf1lafESqD3F9Lk8S9uTM6b19GRByXnInPw/edit?usp=sharing


Explaining Deviations
1. Since upto 4 cores a single machine is used and from 8 cores 2 machines are used, the time taken to run on 8 nodes could be more than the time taken to run for 4 nodes.

AWS EMR Configuration used
1. m4.large(8 core 16 GB ram ) used for slave machines
2. m4.2xlarge(16 core 32 GB ram ) used for master machines

Data Creation
Used marlin to genrate the matrix and store in S3
https://github.com/PasaLab/marlin 

Forked and modified at https://github.com/KharbandaArush/marlin

 
