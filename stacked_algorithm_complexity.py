import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

# Complexity data from function_comparison_metrics.md
# Complexity = number of branching statements (if, else, elif, for loops with conditions, try/except, etc.)
complexity_data = {
    'R1': {'Web 1.0': 1, 'RDFa': 3, 'SPARQL': 1},
    'R2': {'Web 1.0': 1, 'RDFa': 2, 'SPARQL': 1},
    'R3': {'Web 1.0': 1, 'RDFa': 2, 'SPARQL': 1},
    'R4': {'Web 1.0': 5, 'RDFa': 3, 'SPARQL': 1},
    'R5': {'Web 1.0': 4, 'RDFa': 4, 'SPARQL': 1},
    'R6': {'Web 1.0': 3, 'RDFa': 3, 'SPARQL': 1},
    'R7': {'Web 1.0': 2, 'RDFa': 2, 'SPARQL': 1},
    'R8': {'Web 1.0': 3, 'RDFa': 2, 'SPARQL': 1},
    'R9': {'Web 1.0': 5, 'RDFa': 4, 'SPARQL': 3},
    'R10': {'Web 1.0': 9, 'RDFa': 8, 'SPARQL': 5},
}

requests = [f'R{i}' for i in range(1, 11)]
methods = ['Web 1.0', 'RDFa', 'SPARQL']
colors = {'Web 1.0': '#FF6B6B', 'RDFa': '#4ECDC4', 'SPARQL': '#45B7D1'}


fig4, ax4 = plt.subplots(figsize=(12, 7))

# Calculate total complexity per engine
total_complexity = {}
for method in methods:
    total_complexity[method] = sum([complexity_data[req][method] for req in requests])

# Create stacked bar showing contribution of each request
bottoms = {method: 0 for method in methods}
x_pos = np.arange(len(methods))

for req in requests:
    values = [complexity_data[req][method] for method in methods]
    bars = ax4.bar(x_pos, values, 0.6,
                   bottom=[bottoms[method] for method in methods],
                   label=req, alpha=0.85)
    
    # Update bottoms for next stack
    for i, method in enumerate(methods):
        bottoms[method] += values[i]

ax4.set_ylabel('Nombre de branchements', fontsize=12, fontweight='bold')
ax4.set_title('Complexité Algorithique par Moteur\nAccumulé par moteur',
             fontsize=14, fontweight='bold', pad=20)
ax4.set_xticks(x_pos)
ax4.set_xticklabels(methods)
ax4.legend(title='Request', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
ax4.grid(axis='y', alpha=0.3, linestyle='--')

# Add total labels on top
for i, method in enumerate(methods):
    ax4.text(i, total_complexity[method], f'{total_complexity[method]}',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('complexity_cumulative.png', dpi=300, bbox_inches='tight')
print("[OK] Chart 4: complexity_cumulative.png")
