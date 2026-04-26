import time
import threading
import multiprocessing
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Cashback Rate
CASHBACK_RATE = 0.05 

def complex_cashback_logic(amount):
    """Heavy CPU task for processing comparison."""
    val = amount
    for _ in range(40):
        val = (val * CASHBACK_RATE) + (0.0001 * val)
    return val

# --- Processing Methods ---

def run_sequential(amount, iterations):
    print(f"Sequential: Processing {iterations:,} transactions...")
    start = time.time()
    [complex_cashback_logic(amount) for _ in range(iterations)]
    return time.time() - start

def run_threading(amount, iterations, num_threads=10):
    print(f"Threading: Running with {num_threads} threads...")
    start = time.time()
    
    # We split the total iterations into smaller pieces
    chunk_size = iterations // num_threads
    threads = []

    def worker():
        # Using a local variable inside the thread is slightly faster
        local_amt = amount
        for _ in range(chunk_size):
            # The actual math
            val = local_amt
            for _ in range(40):
                val = (val * 0.05) + (0.0001 * val)

    for _ in range(num_threads):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
        
    return time.time() - start

def run_parallel(amount, iterations, num_procs=4):
    print(f"Parallel: Using {num_procs} CPU cores...")
    start = time.time()
    chunk_size = iterations // num_procs
    args = [(amount, chunk_size)] * num_procs
    
    with multiprocessing.Pool(processes=num_procs) as pool:
        pool.starmap(parallel_worker_helper, args)
    
    return time.time() - start

def parallel_worker_helper(amt, count):
    return [complex_cashback_logic(amt) for _ in range(count)]

def main():
    print("--- Optimized High-Volume Cashback Calculator  ---")
    merchant = input("Merchant Name: ")
    user_name = input("User Name: ")
    user_amt = float(input("Transaction Amount: "))
    total_instances = int(input("Number of Transactions (e.g., 500000): "))

    # Execute and time them
    seq_time = run_sequential(user_amt, total_instances)
    thread_time = run_threading(user_amt, total_instances)
    parallel_time = run_parallel(user_amt, total_instances)

    # Calculate Total Reward for the receipt
    total_reward = (user_amt * CASHBACK_RATE) * total_instances

    # --- SAVE TO TXT FILE ---
    receipt_filename = "cashback_receipt.txt"
    with open(receipt_filename, "w") as f:
        f.write("=============================================\n")
        f.write("           OFFICIAL CASHBACK RECEIPT\n")
        f.write("=============================================\n")
        f.write(f"Merchant:           {merchant}\n")
        f.write(f"Customer Name:      {user_name}\n")
        f.write(f"Single Amount:      ${user_amt:,.2f}\n")
        f.write(f"Transaction Count:  {total_instances:,}\n")
        f.write("---------------------------------------------\n")
        f.write(f"TOTAL CASHBACK:     ${total_reward:,.2f}\n")
        f.write("---------------------------------------------\n")
        f.write("PERFORMANCE METRICS:\n")
        f.write(f"Sequential Time:    {seq_time:.4f}s\n")
        f.write(f"Threading Time:     {thread_time:.4f}s\n")
        f.write(f"Parallel Time:      {parallel_time:.4f}s\n")
        f.write("=============================================\n")
        f.write(f"Generated on: {time.ctime()}\n")

    print(f"\nSuccess! Receipt saved to {receipt_filename}")

    # --- Print to Console ---
    print("\n" + "="*45)
    print(f"Sequential: {seq_time:.4f}s")
    print(f"Threading:  {thread_time:.4f}s")
    print(f"Parallel:   {parallel_time:.4f}s")
    print("="*45)

    # --- Charts ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    ax1.bar(['Sequential', 'Threading', 'Parallel'], [seq_time, thread_time, parallel_time], color=['#ff4d4d', '#ffa64d', '#33cc33'])
    ax1.set_title(f'Performance Comparison ({total_instances:,} Trans.)')

    labels = ['Product Value', 'Tax', 'User Cashback']
    sizes = [user_amt * 0.85, user_amt * 0.10, user_amt * 0.05]
    ax2.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#4da6ff', '#bfbfbf', '#33cc33'])
    ax2.set_title(f'Breakdown of ${user_amt:,.2f}')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()