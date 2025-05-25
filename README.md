# VRPpp: Imitation Improvement Learning for Large-Scale Capacitated Vehicle Routing Problems

This repository contains the official implementation for the paper: "Imitation Improvement Learning for Large-Scale Capacitated Vehicle Routing Problems", published at the 33rd International Conference on Automated Planning and Scheduling (ICAPS 2023).

## Description

This work introduces a novel deep reinforcement learning (RL) framework for solving large-scale capacitated vehicle routing problems (CVRP). The core idea is an **Imitation Improvement Learning (IIL)** approach where classical heuristics act as "experts" to guide the RL policy model. This encourages the model to mimic and generate solutions that are similar to or better than those produced by the heuristics. To address scalability, especially for large problem instances (up to 30,000 nodes), we propose **Clockwise Clustering**, an augmented framework that decomposes large CVRPs into smaller subproblems by sequentially clustering nodes in a clockwise order. These subproblems are then learned and solved simultaneously.

Our approach aims to combine the strengths of heuristic methods (stability, high-quality solutions for large instances) with RL (exploration, escaping local optima). The synergy between Clockwise Clustering, heuristic methods, and imitation learning allows for efficient processing and scaling, leading to competitive solution quality and new state-of-the-art results on several well-known CVRP datasets and real-world instances.

## Key Features and Contributions

* **Imitation Improvement Learning (IIL):** A learning-based framework using policy gradient where heuristic methods serve as experts to correct, improve, and guide the policy to generate high-quality, feasible solutions.
* **Clockwise Clustering (CC):** A recursive subproblem decomposition framework designed to handle large-scale CVRP instances effectively by breaking them down into more manageable, similarly distributed sub-instances.
* **State-of-the-Art Performance:** Achieved new state-of-the-art solutions for several large-scale CVRP instances.
* **Scalability and Generalizability:** Demonstrated effectiveness in solving very large-scale real-world instances (up to 30,000 nodes) and generalizability across various CVRP variants and solvers.
* **New Datasets and Results:** Contributed new datasets and results for testing the generalizability of deep RL algorithms for CVRP.

## Methodology Overview

### Clockwise Clustering
The Clockwise Clustering framework operates as follows:
1.  An initial solution is generated using a "clock-hand initializer," which arranges nodes in clockwise order and groups them into tours respecting capacity constraints.
2.  A subset of these tours is selected to form a sub-instance.
3.  This sub-instance is solved using the Imitation Improvement Learning framework.
4.  A portion of the solved sub-solution is stored, and the remaining unprocessed tours/nodes are fed back into the cycle for further processing.
5.  This iterative process continues until all nodes are processed, and the best overall solution is returned.

### Imitation Improvement Learning
The IIL framework is an iterative process:
1.  A sub-solution is fed into an encoder-decoder neural network which approximates a stochastic policy.
2.  The RL policy (student) generates a solution (e.g., using k-opt moves).
3.  This "student solution" is then improved by a classical heuristic method (expert), resulting in an "expert solution".
4.  The IIL model uses Generative Adversarial Imitation Learning (GAIL) to encourage the RL policy's encoder to produce feature representations similar to those from the expert's solutions.
5.  Rewards are calculated based on the improvement between the input and the expert solution, and the RL policy is updated using policy gradient with both RL and imitation losses.

## Datasets

The frameworks were benchmarked on several large-scale CVRP and constrained electrical vehicle routing (CEVRP) datasets, including:
* Uchoa et al. (2017) 
* Li, Yan, and Wu (2021) 
* DIMACS 
* Arnold, Gendreau, and Sörensen (2019) 
* Mavrovouniotis et al. (2020) 
* Newly generated CEVRP instances by the authors 

## Results Highlights

* The IIL framework, particularly when combined with HGS (Hybrid Genetic Search) as the expert, consistently outperformed standalone heuristics like VNS and HGS on various datasets.
* Achieved better average costs compared to previous state-of-the-art methods (e.g., L2D) on Dataset 2 (Li, Yan, and Wu 2021) for instances of sizes 500, 1000, and 2000 nodes.
* Obtained a new state-of-the-art result for the Loggi-n501-k24 instance from the DIMACS dataset.
* Demonstrated strong performance on very-large-scale instances (up to 30,000 nodes) from Dataset 4 (Arnold, Gendreau, and Sörensen 2019), outperforming classical HGS.
* Showcased superior performance on CEVRP datasets, achieving new state-of-the-art results with IIL+HGS.

## Usage

```python
# python main.py
```
The Jupyter notebooks in the repository (`experiments_CVRP.ipynb`, `experiments_CVRP_Uniform.ipynb`, `experiments_DIMACS.ipynb`, `experiments_EVRP.ipynb`, `experiments_EVRP_generation.ipynb`, `experiments_Realworld.ipynb`) provide examples of how to run experiments.

## Citation

If you use this code or ideas from the paper in your research, please cite:

```bibtex
@inproceedings{bui2023imitation,
  title={Imitation improvement learning for large-scale capacitated vehicle routing problems},
  author={Bui, The Viet and Mai, Tien},
  booktitle={Proceedings of the International Conference on Automated Planning and Scheduling},
  volume={33},
  pages={50--58},
  year={2023},
  organization={AAAI Press}
}
```
Or:
BUI, The Viet and MAI, Tien. Imitation improvement learning for large-scale capacitated vehicle routing problems. (2023). Proceedings of the 33rd International Conference on Automated Planning and Scheduling (ICAPS 2023): Prague, July 8-13. 1-9. Available at: https://ink.library.smu.edu.sg/sis_research/8025 

## Acknowledgements

This research/project is supported by the National Research Foundation Singapore and DSO National Laboratories under the AI Singapore Programme (AISG Award No: AISG2-RP-2020-017).
