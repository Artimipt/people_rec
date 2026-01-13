import time
import argparse
import psutil
import GPUtil
import cv2
import numpy as np
from pathlib import Path
import ultralytics
import src  

def test_performance(function_to_test, results_file="performance_results.json", num_runs=10, **kwargs):

    # Track metrics
    times = []
    cpu_usages = []
    gpu_usages = []
    memory_usages = []
    
    print(f"Testing {num_runs} runs on: {function_to_test.__name__}")
    print("-" * 50)
    
    # Warm-up run (not counted)
    print("Warm-up run...")
    function_to_test(**kwargs)
    
    # Main test loop
    for run in range(num_runs):
        # Track resource usage before
        cpu_before = psutil.cpu_percent(interval=None)
        gpus_before = GPUtil.getGPUs()
        gpu_before = gpus_before[0].load if gpus_before else 0
        memory_before = psutil.virtual_memory().percent
        
        # Time the detection
        start_time = time.perf_counter()
        
        # Run detection
        function_to_test(**kwargs)
        
        end_time = time.perf_counter()
        
        # Track resource usage after
        cpu_after = psutil.cpu_percent(interval=None)
        gpus_after = GPUtil.getGPUs()
        gpu_after = gpus_after[0].load if gpus_after else 0
        memory_after = psutil.virtual_memory().percent
        
        # Calculate metrics
        run_time = end_time - start_time
        times.append(run_time)
        cpu_usages.append((cpu_before + cpu_after) / 2)
        gpu_usages.append((gpu_before + gpu_after) / 2)
        memory_usages.append((memory_before + memory_after) / 2)
        
        print(f"Run {run+1}: {run_time:.3f}s, FPS: {1/run_time:.1f}")
    
    # Calculate statistics
    print("\n" + "="*50)
    print("PERFORMANCE REPORT")
    print("="*50)
    
    avg_time = np.mean(times)
    std_time = np.std(times)
    fps = 1 / avg_time
    
    print(f"\nSpeed Metrics:")
    print(f"  Average time: {avg_time:.3f}s (±{std_time:.3f})")
    print(f"  FPS: {fps:.1f} frames per second")
    print(f"  Min time: {np.min(times):.3f}s")
    print(f"  Max time: {np.max(times):.3f}s")
    
    print(f"\nResource Usage:")
    print(f"  CPU: {np.mean(cpu_usages):.1f}% average")
    print(f"  GPU: {np.mean(gpu_usages):.1f}% average" if gpu_usages[0] > 0 else "  GPU: Not available")
    print(f"  Memory: {np.mean(memory_usages):.1f}% average")
    
    # Save results
    results = {
        "function": function_to_test.__name__,
        "avg_time": avg_time,
        "std_time": std_time,
        "fps": fps,
        "cpu_usage": np.mean(cpu_usages),
        "gpu_usage": np.mean(gpu_usages) if gpu_usages[0] > 0 else None,
        "memory_usage": np.mean(memory_usages),
        "times": times
    }
    
    # Save to file
    import json
    results_file = Path("performance_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {results_file}")
    return results
