import subprocess
import os
import time
import psutil
from generate_dataset import generate_graph
import matplotlib.pyplot as plt
import numpy as np
# Create folder for empirical testing
os.makedirs('empiricaltestinggraph', exist_ok=True)

def run_karger_cpp(G):
    """Run C++ Karger and return (result, time, memory in MB)."""
    V = len(G)
    # Calculate edge count without building a list
    E = sum(1 for i in range(V) for j in range(i + 1, V) if G[i][j] > 0)
    trials = 1

    proc = subprocess.Popen(
        ["karger.exe"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Write directly to the process stdin to avoid creating a huge string
    try:
        proc.stdin.write(f"{V} {E} {trials}\n")
        for i in range(V):
            for j in range(i + 1, V):
                if G[i][j] > 0:
                    proc.stdin.write(f"{i} {j} {G[i][j]}\n")
        proc.stdin.close() # Close stdin to signal end of input
    except (IOError, BrokenPipeError):
        # Handle cases where the process exits before all data is written
        pass

    out, err = proc.communicate()
    
    # Parse the new output: mincut, time, and memory
    mincut, elapsed, memory = out.strip().split()

    return int(mincut), float(elapsed), float(memory)

# Compile C++ binary
print("Compiling C++ Karger...")
os.system("g++ -O3 -o karger.exe kargercppver.cpp -lpsapi")

# Generate and test graphs
print("\nGenerating graphs and testing...\n")
vertices = [x for x in range(1500,2000,100)]
times = []
memories = []

for v in vertices:
    G = generate_graph(v, 'complete')
    result, t, m = run_karger_cpp(G)
    times.append(t)
    memories.append(m)
    print(f"V={v:3d} | Time: {t:.4f}s | Memory: {m:.2f}MB")

# Save dataset
f = open('empiricaltestinggraph/kargerdataset.txt', 'w')

f.write("Vertices,Time(s),Memory(MB)\n")
for v, t, m in zip(vertices, times, memories):
    f.write(f"{v},{t:.6f},{m:.4f}\n")

slope, intercept = np.polyfit(np.log(vertices), np.log(times), 1)
print(f"Slope found is m = {slope}")
f.write(f"Time slope = {slope}")
slope, intercept = np.polyfit(np.log(vertices), np.log(memories), 1)
print(f"Slope found is m = {slope}")
f.write(f"Memory slope = {slope}")

# Plot Time (separate graph)
plt.figure(figsize=(8, 5))

plt.plot(vertices, times, 'o-', linewidth=2, markersize=8, color='blue')
plt.xlabel('Input Size (Vertices)', fontsize=12)
plt.ylabel('Time (seconds)', fontsize=12)
plt.title('Karger: Time vs Input Size', fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.savefig('empiricaltestinggraph/karger_time.png', dpi=150)
plt.close()

# Plot Memory (separate graph)
plt.figure(figsize=(8, 5))
plt.plot(vertices, memories, 's-', linewidth=2, markersize=8, color='red')
plt.xlabel('Input Size (Vertices)', fontsize=12)
plt.ylabel('Memory (MB)', fontsize=12)
plt.title('Karger: Memory vs Input Size', fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.savefig('empiricaltestinggraph/Karger_memory.png', dpi=150)
plt.close()


