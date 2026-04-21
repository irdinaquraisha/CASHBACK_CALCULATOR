import multiprocessing
import threading
import time
import random
import os  
import matplotlib.pyplot as plt
from decimal import Decimal, ROUND_HALF_UP

# --- 1. THE LOGIC (DYNAMIC WORKLOAD) ---
def calculate_cashback(amount, complexity):
    """
    Simulates server work. 
    Concurrency hides the sleep. 
    Parallelism crushes the math loop.
    """
    # 1. IO Wait (Simulated Database Call)
    time.sleep(0.001) 
    
    # 2. CPU Math (Complexity controlled by user)
    # Raising this value makes Parallelism much faster than the others.
    for _ in range(complexity): 
        _ = 12345.67 * 9876.54
        
    amt = Decimal(str(amount))
    rate = Decimal('0.05')
    limit = Decimal('5.00')
    cashback = (amt * rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return float(min(cashback, limit))

# --- 2. WORKERS ---
def parallel_worker(chunk, comp):
    return [calculate_cashback(p, comp) for _, p in chunk]

def concurrent_thread_task(chunk, results_list, index, comp):
    results_list[index] = [calculate_cashback(p, comp) for _, p in chunk]

# --- 3. RECEIPT GENERATOR ---
def generate_receipt(merchant, cust_id, total_saved, total_spent, num_cores, times, distribution, count):
    save_path = r"C:\Users\so - Personal\OneDrive\Documents\CASHBACK_PROJECT"
    folder_path = os.path.join(save_path, "receipt")
    
    try:
        if not os.path.exists(folder_path): os.makedirs(folder_path, exist_ok=True)
    except PermissionError:
        folder_path = os.path.join(os.getcwd(), "receipt_backup")
        if not os.path.exists(folder_path): os.makedirs(folder_path, exist_ok=True)

    full_path = os.path.join(folder_path, f"Audit_{cust_id}.txt")
    s_t, c_t, p_t = times
    
    receipt_text = (
        "\n==========================================\n"
        f"       {merchant.upper()} - SYSTEM AUDIT\n"
        "==========================================\n"
        f"Auditor ID:     {cust_id}\n"
        f"Date:           {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Processor Cores:{num_cores}\n"
        "------------------------------------------\n"
        "PERFORMANCE BENCHMARKS:\n"
        f"1. Sequential:  {s_t:.4f}s\n"
        f"2. Concurrent:  {c_t:.4f}s ({s_t/c_t:.2f}x Speedup)\n"
        f"3. Parallel:    {p_t:.4f}s ({s_t/p_t:.2f}x Speedup)\n"
        "------------------------------------------\n"
        "FINANCIAL TOTALS:\n"
        f"Total Processed: {count:,} items\n"
        f"Total Volume:    RM{total_spent:,.2f}\n"
        f"Total Cashback:  RM{total_saved:,.2f}\n"
        "------------------------------------------\n"
        "DISTRIBUTION:\n"
        f"Capped (RM5):    {distribution[0]:,}\n"
        f"Under Cap:       {distribution[1]:,}\n"
        "==========================================\n"
    )
    print(receipt_text)
    with open(full_path, "w") as f: f.write(receipt_text)
    print(f"[System] Audit saved to: {full_path}")

# --- 4. VISUALIZATION ---
def generate_graphs(times, pie_data, num_cores):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    ax1.pie(pie_data, labels=['Max RM5', 'Below RM5'], autopct='%1.1f%%', colors=['#2ecc71', '#3498db'], startangle=90)
    ax1.set_title("E-Wallet Cashback Distribution")
    
    labels = ['Sequential\n(1 Core)', 'Concurrent\n(Thread Mix)', f'Parallel\n({num_cores} Cores)']
    colors = ['#e74c3c', '#f1c40f', '#27ae60']
    bars = ax2.bar(labels, times, color=colors)
    ax2.set_ylabel("Execution Time (Seconds)")
    ax2.set_title("Architecture Performance Benchmark")
    
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height, f'{height:.3f}s', ha='center', va='bottom', fontweight='bold')
        
    plt.tight_layout()
    plt.show()

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    multiprocessing.freeze_support()
    auto_items = ["Groceries", "Petrol", "Coffee", "Bill Payment", "Dining Out", "E-Hailing"]
    
    running = True
    while running:
        print("\n--- E-Wallet Architecture Auditor ---")
        
        # USER INPUTS
        m_name = input("Enter Merchant Name: ")
        a_id = input("Enter Auditor/Student ID: ")
        
        try:
            total_count = int(input("Number of transactions (Recommended 5000): "))
            complexity = int(input("Simulation Complexity (Light: 1000, Heavy: 500000): "))
        except ValueError:
            total_count, complexity = 5000, 100000
            print("Invalid input. Using default Stress Test values.")

        cores = 4
        data = [(random.choice(auto_items), round(random.uniform(5.0, 300.0), 2)) for _ in range(total_count)]
        avg = len(data) // cores
        chunks = [data[i*avg : (i+1)*avg if i < cores-1 else len(data)] for i in range(cores)]

        # 1. SEQUENTIAL
        print(f"\n[1/3] Running Sequential Audit...")
        start = time.time()
        res_seq = [calculate_cashback(p, complexity) for _, p in data]
        s_time = time.time() - start

        # 2. CONCURRENT
        print("[2/3] Running Concurrent (Threading) Audit...")
        start = time.time()
        threads, res_con = [], [None] * cores
        for i in range(cores):
            t = threading.Thread(target=concurrent_thread_task, args=(chunks[i], res_con, i, complexity))
            threads.append(t)
            t.start()
        for t in threads: t.join()
        c_time = time.time() - start

        # 3. PARALLEL
        print("[3/3] Running Parallel (Multiprocessing) Audit...")
        start = time.time()
        with multiprocessing.Pool(processes=cores) as pool:
            # We use starmap to pass multiple arguments to the worker
            res_par_list = pool.starmap(parallel_worker, [(c, complexity) for c in chunks])
        p_time = time.time() - start
        
        # Results
        total_spent = sum(p for _, p in data)
        total_saved = sum(res_seq)
        over = sum(1 for r in res_seq if r == 5.0)
        under = len(res_seq) - over

        generate_receipt(m_name, a_id, total_saved, total_spent, cores, 
                         [s_time, c_time, p_time], (over, under), total_count)
        
        generate_graphs([s_time, c_time, p_time], [over, under], cores)

        if input("\nClose graphs to continue. Run again? (y/n): ").lower() not in ['y', 'yes']:
            print("System Shutdown. Audit Complete.")
            running = False