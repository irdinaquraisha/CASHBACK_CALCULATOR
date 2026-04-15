import multiprocessing
import threading
import time
import random
import csv
import matplotlib.pyplot as plt

# --- 1. THE CALCULATION LOGIC ---
def process_data(amount):
    """The simple math shared by both methods."""
    cashback = amount * 0.05
    return 5.0 if cashback >= 5.0 else round(cashback, 2)

# --- 2. PARALLEL WORKER ---
def parallel_worker(chunk_info):
    data_chunk, proc_id = chunk_info
    start_time = time.time()
    
    results = []
    over_limit = 0
    under_limit = 0
    
    for _, amount in data_chunk:
        res = process_data(amount)
        if res == 5.0: over_limit += 1
        else: under_limit += 1
        results.append(res)
        
    end_time = time.time()
    return (proc_id, start_time, end_time), (over_limit, under_limit)

# --- 3. SEQUENTIAL CALCULATION ---
def run_sequential(data):
    print(f"\n[1/2] Starting Sequential Calculation (1 Core)...")
    start = time.time()
    results = []
    for _, amount in data:
        results.append(process_data(amount))
    end = time.time()
    return end - start

# --- 4. THE PLOTTING FUNCTION ---
def generate_graphs(gantt_data, pie_data, s_time, p_time):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Pie Chart
    ax1.pie(pie_data, labels=['Max RM5', 'Below RM5'], autopct='%1.1f%%', colors=['#4CAF50', '#FFC107'])
    ax1.set_title(f"Results Distribution\n(Total Time: {p_time:.2f}s)")

    # Gantt Chart (Parallel Proof)
    gantt_data.sort() 
    for proc_id, start, end in gantt_data:
        ax2.barh(f"Core {proc_id}", end - start, left=start, color='skyblue')
    ax2.set_xlabel("Time (Seconds)")
    ax2.set_title(f"Gantt Chart: Parallel Execution\nSequential was {s_time/p_time:.2f}x Slower")
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("=== E-Wallet Cashback Performance Auditor ===")
    try:
        total_input = int(input("Enter number of transactions (e.g. 2000000): "))
        num_cores = int(input(f"Enter cores (Max {multiprocessing.cpu_count()}): "))
    except:
        total_input, num_cores = 1000000, 4

    # Generate data
    data = [(i, random.uniform(10, 200)) for i in range(total_input)]
    
    # 1. RUN SEQUENTIAL (For Comparison)
    seq_time = run_sequential(data)
    print(f"Sequential Time: {seq_time:.4f} seconds")

    # 2. RUN PARALLEL
    print(f"\n[2/2] Starting Parallel Calculation ({num_cores} Cores)...")
    avg = len(data) // num_cores
    chunks = [(data[idx*avg : (idx+1)*avg if idx < num_cores-1 else len(data)], idx) for idx in range(num_cores)]

    start_p = time.time()
    with multiprocessing.Pool(processes=num_cores) as pool:
        output = pool.map(parallel_worker, chunks)
    end_p = time.time()
    par_time = end_p - start_p
    
    print(f"Parallel Time: {par_time:.4f} seconds")
    print(f"--- SPEEDUP: {seq_time / par_time:.2f}x Faster ---")

    # Metadata for graphs
    gantt_times = [item[0] for item in output]
    pie_counts = [sum(x) for x in zip(*[item[1] for item in output])]
    
    # Start background logging thread (Concurrency)
    threading.Thread(target=lambda: print("[Thread] Logged to memory."), daemon=True).start()

    generate_graphs(gantt_times, pie_counts, seq_time, par_time)