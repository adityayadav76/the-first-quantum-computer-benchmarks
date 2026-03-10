'''
Example Command(s)

python run_one_benchmark.py --algorithm qft --qubits 20
python run_one_benchmark.py --algorithm ghz --qubits 20
python run_one_benchmark.py --algorithm shor --N 18
possible --N values for shors 18, 42, 58, 74
'''


import time
import argparse

from mqt.bench import get_benchmark, BenchmarkLevel
from qiskit import transpile
import sys
sys.path.append('../../python/')

from AutomatskiKomencoQiskit import AutomatskiKomencoQiskit

backend = AutomatskiKomencoQiskit(
    host="xxx.xxx.xxx.xxx",
    port=xx
)

# -------------------------------
# Benchmark runner
# -------------------------------

def generate_benchmark(algorithm, num_qubits=None, shor_N=None):

    if algorithm == "shor":
        if shor_N is None:
            raise ValueError("Shor benchmark requires parameter N (number to factor).")

        # MQT Shor benchmark uses N instead of circuit_size
        qc = get_benchmark(
            benchmark="shor",
            level=BenchmarkLevel.ALG,
            circuit_size=shor_N
        )

        return qc

    else:
        if num_qubits is None:
            raise ValueError("You must provide --qubits for this algorithm.")

        qc = get_benchmark(
            benchmark=algorithm,
            level=BenchmarkLevel.ALG,
            circuit_size=num_qubits
        )

        return qc


# -------------------------------
# Execute circuit
# -------------------------------

def run_benchmark(qc, shots=100000):

    # Add measurement if missing
    if qc.num_clbits == 0:
        qc = qc.copy()
        qc.measure_all()

    print("\nTranspiling...")
    t0 = time.time()
    safe_basis = ['ccx', 'ccz', 'cp', 'crz', 'cs', 'cswap', 'cu', 'cx', 'cy', 'cz', 'h', 'id', 'measure', 'reset', 'p', 'rx', 'ry', 'rz', 's', 'sdg', 'swap', 'sx', 'sxdg', 't', 'tdg', 'u', 'x', 'y', 'z']
    compiled = transpile( qc, basis_gates=safe_basis,optimization_level=3)
    t1 = time.time()

    print("Executing...")
    counts = backend.run(compiled, repetitions=shots,topK=1000).get_counts(None)

    t2 = time.time()

    print("\n----- Benchmark Result -----")
    print("Qubits:", qc.num_qubits)
    print("Depth:", qc.depth())
    print("Gate count:", qc.size())

    print("\nTiming")
    print("Transpile time:", t1 - t0)
    print("Execution time:", t2 - t1)

    print("\nSample Counts:")
    print(dict(sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]))

    return counts


# -------------------------------
# Main CLI
# -------------------------------

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--algorithm",
        type=str,
        required=True,
        help="MQT algorithm (qft, grover, ghz, qaoa, shor, etc.)"
    )

    parser.add_argument(
        "--qubits",
        type=int,
        help="Number of qubits"
    )

    parser.add_argument(
        "--N",
        type=int,
        help="Number to factor (for Shor)"
    )

    parser.add_argument(
        "--shots",
        type=int,
        default=100000
    )

    args = parser.parse_args()

    print("\nGenerating benchmark circuit...")

    qc = generate_benchmark(
        algorithm=args.algorithm,
        num_qubits=args.qubits,
        shor_N=args.N
    )

    print("\nCircuit summary")
    print("Qubits:", qc.num_qubits)
    print("Depth:", qc.depth())

    run_benchmark(qc, shots=args.shots)


if __name__ == "__main__":
    main()