# The First Quantum Computer Benchmarks
The First Quantum Computer Benchmarks

![](https://automatski.com/wp-content/uploads/2025/05/Automatski-New-Logo.svg)

## About

TFQCB is a Quantum Computer Benchmark created by [Automatski](https://automatski.com). It is part of a larger suite of benchmarks used by Automatski to evaluate its quantum computers, which have not yet been released publicly. These benchmarks are used to validate correct operation after each engineering cycle, including changes and upgrades.

### Intellectual Property
All rights are reserved by Automatski for Automatski-authored components of this codebase. Rights to third-party or upstream components remain with their respective original authors and licensors.

## Installation

TFQCB requires Python v3.11+ to run.
Install dependencies:

```sh
pip install requests qiskit==1.4.2 qiskit-aer==0.16 mqt.bench pandas matplotlib tqdm
```

Run All The Benchmarks
```sh
python run_all_benchmarks.py
```

Run One Benchmark (Examples)
```sh
python run_one_benchmark.py --algorithm qft --qubits 20
python run_one_benchmark.py --algorithm ghz --qubits 20
python run_one_benchmark.py --algorithm shor --N 18
.
.
.
```
possible --N values for shors 18, 42, 58, 74

## The Complete List Of Benchmark Algorithms

![](https://raw.githubusercontent.com/adityayadav76/the-first-quantum-computer-benchmarks/refs/heads/main/Complete-List-Of-Benchmark-Algorithms.png)

## Results

### CX Count

![](https://raw.githubusercontent.com/adityayadav76/the-first-quantum-computer-benchmarks/refs/heads/main/benchmark_results/cx_count.png)

### Depth

![](https://raw.githubusercontent.com/adityayadav76/the-first-quantum-computer-benchmarks/refs/heads/main/benchmark_results/depth.png)

### Execution Time

![](https://raw.githubusercontent.com/adityayadav76/the-first-quantum-computer-benchmarks/refs/heads/main/benchmark_results/execution_time.png)

### Memory (MB)

![](https://raw.githubusercontent.com/adityayadav76/the-first-quantum-computer-benchmarks/refs/heads/main/benchmark_results/memory_mb.png)
