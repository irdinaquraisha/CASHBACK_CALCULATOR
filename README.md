
# 🚀 High-Volume Cashback Calculator

<p align="center">
  <img src="logo.png" width="600">
</p>

> **Audit Professional:** Quraisha Irdina Binti Hazimin  
> **Course:** ITT440-Individual Assignment  
> **Student ID:** 2025479998  

---
### *Performance Analysis: Sequential vs. Concurrent vs. Parallel*


## 📌 1. Project Overview
This application is a high-performance auditing tool designed to simulate an E-Wallet cashback system. It calculates a 5% cashback (capped at RM5.00) for thousands of transactions. The project demonstrates the practical execution differences between three major computing architectures:
* **Sequential:** Traditional one-by-one processing.
* **Concurrent (Threading):** Task overlapping to hide latency.
* **Parallel (Multiprocessing):** True simultaneous execution using multiple CPU cores.

---

## 💻 2. System Requirements
| Requirement | Minimum Specification |
| :--- | :--- |
| **OS** | Windows 10+, macOS, or Linux |
| **Language** | Python 3.7+ |
| **Libraries** | `matplotlib`, `pandas`, `numpy` |
| **Hardware** | Multi-core CPU (recommended for Parallel testing) |

---

## 🛠️ 3. Installation Steps
1. **Install Python:** Ensure Python is installed on your system via [python.org](https://www.python.org/).
2. **Install dependencies:** 
   ```bash
   pip install matplotlib pandas numpy
3. **Setup Workspace:** Create a main folder: CASHBACK_PROJECT
4. **Create a sub-folder:** CASHBACK_PROJECT/receipt
5. **Save Script:** Save the project code as importmultiprocessing.py inside the main folder.

## 🏃 4. How to Run the Program
1. Open your terminal or IDE and navigate to the CASHBACK_PROJECT directory.
2. Launch the application:
```Bash
python importmultiprocessing.py
```
3. **Follow the Prompts:**
   Enter Merchant, Username and amount.
5. **View Results:** The system will display two graphs. Close the graph window to see the option to run another audit or exit.

## 📊 5. Performance Logic Explained
| Architecture | Implementation | Best For... | Behavior |
| :--- | :--- | :--- | :--- |
| **Sequential** | Standard Loop | Small tasks | Processes one item at a time; moves to the next only when the current one finishes. |
| **Concurrent** | `threading` | IO-Bound tasks | Tasks "overlap." While one task waits for a simulated server response, another begins. |
| **Parallel** | `multiprocessing` | CPU-Bound tasks | Tasks run at the exact same physical moment by utilizing multiple CPU cores simultaneously. |

## 📝 6. Sample Input/Output
### User Input Example:
* **Merchant:** Grab
* **Username:** Quraisha
* **Amount:** 5000
* **Count:** 500000
 
**Generated Audit Receipt**
```text
=============================================
           OFFICIAL CASHBACK RECEIPT
=============================================
Merchant:           SHEIN
Customer Name:      irdina
Single Amount:      $7,500.00
Transaction Count:  8,000,000
---------------------------------------------
TOTAL CASHBACK:     $3,000,000,000.00
---------------------------------------------
PERFORMANCE METRICS:
Sequential Time:    20.7122s
Threading Time:     17.5272s
Parallel Time:      9.9721s
=============================================
```
# 🖼️ 7. Screenshots & Visuals
**Staircase Performance Benchmark**
<img src="Result_Quraisha.png" width="600">
### Results & Performance Analysis

| Metric | Sequential (Baseline) | Concurrent (Threading) | Parallel (Multiprocessing) |
| :--- | :--- | :--- | :--- |
| **Execution Time** | **66.725s** | **55.293s** | **25.815s** |
| **Speedup Factor** | 1.0x (Reference) | ~1.19x Faster | **~2.58x Faster** |
| **CPU Utilization** | Single Core (100%) | Single Core (Shared) | **Multiple Cores (4x 100%)** |
| **Efficiency** | Lowest | Moderate | **Highest** |

---

### 🔍 Key Findings

#### **1. Architecture Performance**
The bar chart demonstrates a massive performance jump when switching to **Parallel** processing:
* **The Problem:** Sequential processing creates a bottleneck, requiring 66.725 seconds to complete the 5,000-item audit.
* **The Solution:** By bypassing the Python Global Interpreter Lock (GIL) and distributing the workload across 4 physical CPU cores, the **Parallel** mode finishes in just **25.815 seconds**.
* **Observation:** Achieved a **2.58x speedup**. While Python's overhead prevents a perfect 4x speedup, this parallel implementation is nearly 3 times more efficient than standard sequential execution.

#### **2. Cashback Distribution Insights**
The pie chart reveals the financial behavior of the simulated dataset:
* **67.7% (Max RM5):** The majority of transactions were high-value (RM100+), hitting the cashback ceiling.
* **32.3% (Below RM5):** These represent smaller "micro-transactions" where the 5% reward was less than RM5.

---

# 📂 8. Source Code Technical Breakdown
The core of this project lies in how the AuditManager class handles data across three different execution patterns:

**A. Sequential Logic**
Uses a simple for loop. This is the baseline for performance comparison.
```
for transaction in data:
    self.calculate_cashback(transaction)
```
**B. Concurrent (Threading) Logic**
Uses ```threading.Thread.```It manages multiple tasks by switching between them quickly. While it doesn't run code simultaneously (due to Python's GIL), it is excellent for overlapping "wait times."

**C. Parallel (Multiprocessing) Logic**
Uses the ```multiprocessing``` module to bypass the Global Interpreter Lock (GIL). It creates a pool of workers that run on separate CPU cores, allowing for true simultaneous calculation.
```# Distributes workload across 4 CPU cores
with multiprocessing.Pool(processes=4) as pool:
    results = pool.map(self.calculate_cashback, data)
```
🔗 Source Code Files
The complete implementation can be found in the following file within this repository:
* [**importmultiprocessing.py**](importmultiprocessing.py)

### 💡 Conclusion for Auditor Report
The data confirms that for a real-world E-Wallet system, **Parallel Architecture** is the only viable solution for processing millions of transactions. Using standard Sequential loops would cause significant system lag and delay audit generation.
