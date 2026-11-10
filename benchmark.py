import platform
import statistics
import sys
import time
from rule_engine.classifier import classify


def run_benchmark():
    sample_patient = {
        "tuoi": 25,
        "huyet_ap_tam_thu": 110,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
    }

    # Warm-up 100 lan
    for _ in range(100):
        classify(sample_patient)

    # Benchmark 1.000 lan sau warm-up
    latencies = []
    for _ in range(1000):
        start = time.perf_counter()
        classify(sample_patient)
        end = time.perf_counter()
        latencies.append((end - start) * 1000)

    p50 = statistics.median(latencies)
    p95 = statistics.quantiles(latencies, n=100)[94]

    print(f"Machine : {platform.platform()} | {platform.processor()}")
    print(f"Python  : {sys.version.split()[0]}")
    print("Runs    : 1000 (after 100 warm-up)")
    print(f"p50     : {p50:.4f} ms")
    print(f"p95     : {p95:.4f} ms")
    print("Result  :", "PASSED (< 100 ms)" if p95 < 100 else "FAILED (>= 100 ms)")


if __name__ == "__main__":
    run_benchmark()