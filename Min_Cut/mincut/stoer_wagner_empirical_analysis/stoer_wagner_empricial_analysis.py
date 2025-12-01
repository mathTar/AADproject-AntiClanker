import subprocess
import os
import time
from generate_dataset import generate_graph
import matplotlib.pyplot as plt
import numpy as np
# Create folder for empirical testing
os.makedirs('empiricaltestinggraph', exist_ok=True)

def run_stoer_wagner_cpp(G):
    """Run C++ Stoer-Wagner and return (result, time, memory in MB)."""
    V = len(G)
    edges = [(i, j, G[i][j]) for i in range(V) for j in range(i + 1, V) if G[i][j] > 0]
    E = len(edges)

    input_data = f"{V} {E}\n" + "\n".join(f"{s} {d} {w}" for s, d, w in edges)

    proc = subprocess.Popen(
        ["stoer_wagner.exe"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    out, err = proc.communicate(input=input_data)
    
    # Parse the new output: mincut, time, and memory
    mincut, elapsed, memory = out.strip().split()

    return int(mincut), float(elapsed), float(memory)

# Compile C++ binary
print("Compiling C++ Stoer-Wagner...")
os.system("g++ -O3 -o stoer_wagner.exe stoer_wagner.cpp -lpsapi")

# Generate and test graphs
print("\nGenerating graphs and testing...\n")
vertices = [x for x in range(1000, 1500, 100)]
times = []
memories = []

for v in vertices:
    G = generate_graph(v, 'complete')
    result, t, m = run_stoer_wagner_cpp(G)
    times.append(t)
    memories.append(m)
    print(f"V={v:3d} | Time: {t:.4f}s | Memory: {m:.2f}MB")

# Save dataset
f = open('empiricaltestinggraph/stoerwagnerdataset.txt', 'w')
f.write("Vertices,Time(s),Memory(MB)\n")
for v, t, m in zip(vertices, times, memories):
    f.write(f"{v},{t:.6f},{m:.4f}\n")

slope, intercept = np.polyfit(np.log(vertices), np.log(times), 1)
print(f"Slope found is m = {slope}")
f.write(f"Time Slope = {slope}\n")
slope, intercept = np.polyfit(np.log(vertices), np.log(memories), 1)
print(f"Slope found is m = {slope}")
f.write(f"Memroy slope = {slope}")
# Plot Time (separate graph)
plt.figure(figsize=(8, 5))

plt.plot(vertices, times, 'o-', linewidth=2, markersize=8, color='blue')
plt.xlabel('Input Size (Vertices)', fontsize=12)
plt.ylabel('Time (seconds)', fontsize=12)
plt.title('Stoer-Wagner: Time vs Input Size', fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.savefig('empiricaltestinggraph/stoer_wagner_time.png', dpi=150)
plt.close()

# Plot Memory (separate graph)
plt.figure(figsize=(8, 5))
plt.plot(vertices, memories, 's-', linewidth=2, markersize=8, color='red')
plt.xlabel('Input Size (Vertices)', fontsize=12)
plt.ylabel('Memory (MB)', fontsize=12)
plt.title('Stoer-Wagner: Memory vs Input Size', fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.savefig('empiricaltestinggraph/stoer_wagner_memory.png', dpi=150)
plt.close()

f.close()

