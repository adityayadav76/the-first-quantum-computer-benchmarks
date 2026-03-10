import os
import time
import psutil
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from mqt.bench import get_benchmark, BenchmarkLevel
from qiskit import transpile


# ============================================================
# CONFIGURATION
# ============================================================

MIN_QUBITS = 5
MAX_QUBITS = 20
STEP = 5
SHOTS = 100000

OUTPUT_DIR = "benchmark_results"
CSV_FILE = os.path.join(OUTPUT_DIR, "benchmark_results.csv")


# ============================================================
# ALL MQT BENCHMARK ALGORITHMS
# ============================================================

ALGORITHMS = [
    "ae",
    "bmw_quark_cardinality",
    "bmw_quark_copula",
    "bv",
    "cdkm_ripple_carry_adder",
    "dj",
    "draper_qft_adder",
    "full_adder",
    "ghz",
    "graphstate",
    "grover",
    "half_adder",
    "hhl",
    "hrs_cumulative_multiplier",
    "modular_adder",
    "multiplier",
    "qaoa",
    "qft",
    "qftentangled",
    "qnn",
    "qpeexact",
    "qpeinexact",
    "qwalk",
    "randomcircuit",
    "rg_qft_multiplier",
    "seven_qubit_steane_code",
    #"shor",
    #"shors_nine_qubit_code",
    "vbe_ripple_carry_adder",
    "vqe_real_amp",
    "vqe_su2",
    "vqe_two_local",
    "wstate"
]


# ============================================================
# PREPARE OUTPUT DIRECTORY
# ============================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# BACKEND
# ============================================================

import sys
sys.path.append('../../python/')

from AutomatskiKomencoQiskit import AutomatskiKomencoQiskit

backend = AutomatskiKomencoQiskit(
    host="xxx.xxx.xxx.xxx",
    port=xx
)

# ============================================================
# MEMORY MONITOR
# ============================================================

def memory_usage_mb():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


# ============================================================
# GENERATE BENCHMARK CIRCUIT
# ============================================================

def generate_circuit(algorithm, qubits):

    try:

        qc = get_benchmark(
            benchmark=algorithm,
            level=BenchmarkLevel.ALG,
            circuit_size=qubits
        )

        return qc

    except Exception:
        return None


# ============================================================
# BENCHMARK EXECUTION
# ============================================================

results = []

qubit_range = list(range(MIN_QUBITS, MAX_QUBITS + 1, STEP))


for algo in ALGORITHMS:

    print("\n====================================")
    print("Running algorithm:", algo)
    print("====================================")

    for q in tqdm(qubit_range):

        qc = generate_circuit(algo, q)

        if qc is None:
            continue

        if qc.num_qubits > MAX_QUBITS:
            continue

        if qc.num_clbits == 0:
            qc = qc.copy()
            qc.measure_all()

        depth = qc.depth()
        gate_count = qc.size()

        cx_count = qc.count_ops().get("cx", 0)

        mem_before = memory_usage_mb()

        # --------------------------------
        # Transpile
        # --------------------------------

        t0 = time.time()

        safe_basis = ['ccx', 'ccz', 'cp', 'crz', 'cs', 'cswap', 'cu', 'cx', 'cy', 'cz', 'h', 'id', 'measure', 'reset', 'p', 'rx', 'ry', 'rz', 's', 'sdg', 'swap', 'sx', 'sxdg', 't', 'tdg', 'u', 'x', 'y', 'z']
        compiled = transpile( qc, basis_gates=safe_basis,optimization_level=3)

        t1 = time.time()

        # --------------------------------
        # Execute
        # --------------------------------

        counts = backend.run(compiled, repetitions=SHOTS,topK=1000).get_counts(None)

        t2 = time.time()

        mem_after = memory_usage_mb()

        results.append({
            "algorithm": algo,
            "qubits": qc.num_qubits,
            "depth": depth,
            "gate_count": gate_count,
            "cx_count": cx_count,
            "transpile_time": t1 - t0,
            "execution_time": t2 - t1,
            "memory_mb": mem_after - mem_before
        })


# ============================================================
# SAVE CSV
# ============================================================

df = pd.DataFrame(results)

df.to_csv(CSV_FILE, index=False)

print("\nResults saved to:", CSV_FILE)


# ============================================================
# PLOTS
# ============================================================

print("Generating plots...")
# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(CSV_FILE)

# Ensure numeric types
numeric_cols = [
    "qubits",
    "depth",
    "gate_count",
    "cx_count",
    "transpile_time",
    "execution_time",
    "memory_mb"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove invalid rows
df = df.dropna()

print("Rows available for plotting:", len(df))


# ============================================================
# PLOTS
# ============================================================

metrics = [
    "depth",
    "cx_count",
    "execution_time",
    "memory_mb"
]

for metric in metrics:

    plt.figure(figsize=(10,6))

    for algo in sorted(df["algorithm"].unique()):

        subset = df[df["algorithm"] == algo]

        if len(subset) == 0:
            continue

        subset = subset.sort_values("qubits")

        plt.plot(
            subset["qubits"].values,
            subset[metric].values,
            marker="o",
            linewidth=1,
            label=algo
        )

    plt.xlabel("Qubits")
    plt.ylabel(metric)
    plt.title(f"{metric} vs Qubits")

    plt.grid(True)

    plt.legend(
        fontsize=6,
        ncol=3
    )

    plot_file = os.path.join(OUTPUT_DIR, f"{metric}.png")

    plt.tight_layout()
    plt.savefig(plot_file, dpi=300)

    plt.close()

    print("Saved plot:", plot_file)


print("\nBenchmark complete.")