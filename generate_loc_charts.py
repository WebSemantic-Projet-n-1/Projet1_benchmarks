#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate bar charts comparing Lines of Code (LOC) across the three engines
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Data extracted from function_comparison_metrics.md
data = {
    'R1': {'Web 1.0': 14, 'RDFa': 22, 'SPARQL': 23},
    'R2': {'Web 1.0': 17, 'RDFa': 17, 'SPARQL': 18},
    'R3': {'Web 1.0': 17, 'RDFa': 17, 'SPARQL': 20},
    'R4': {'Web 1.0': 19, 'RDFa': 28, 'SPARQL': 22},
    'R5': {'Web 1.0': 31, 'RDFa': 30, 'SPARQL': 25},
    'R6': {'Web 1.0': 23, 'RDFa': 28, 'SPARQL': 33},
    'R7': {'Web 1.0': 12, 'RDFa': 13, 'SPARQL': 26},
    'R8': {'Web 1.0': 19, 'RDFa': 24, 'SPARQL': 30},
    'R9': {'Web 1.0': 58, 'RDFa': 55, 'SPARQL': 72},
    'R10': {'Web 1.0': 63, 'RDFa': 69, 'SPARQL': 61},
}

# Extract data for plotting
requests = list(data.keys())
web1_locs = [data[req]['Web 1.0'] for req in requests]
rdfa_locs = [data[req]['RDFa'] for req in requests]
sparql_locs = [data[req]['SPARQL'] for req in requests]

# Calculate averages
web1_avg = np.mean(web1_locs)
rdfa_avg = np.mean(rdfa_locs)
sparql_avg = np.mean(sparql_locs)

print(f"Average LOC - Web 1.0: {web1_avg:.1f}, RDFa: {rdfa_avg:.1f}, SPARQL: {sparql_avg:.1f}")

# Chart 1: LOC per request for each engine
fig1, ax1 = plt.subplots(figsize=(14, 7))

x = np.arange(len(requests))
width = 0.25

bars1 = ax1.bar(x - width, web1_locs, width, label='Web 1.0', color='#FF6B6B', alpha=0.8)
bars2 = ax1.bar(x, rdfa_locs, width, label='RDFa', color='#4ECDC4', alpha=0.8)
bars3 = ax1.bar(x + width, sparql_locs, width, label='SPARQL', color='#45B7D1', alpha=0.8)

ax1.set_xlabel('Request / Function', fontsize=12, fontweight='bold')
ax1.set_ylabel('Lines of Code (LOC)', fontsize=12, fontweight='bold')
ax1.set_title('Lines of Code Comparison by Request Across Three Engines', fontsize=14, fontweight='bold', pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(requests)
ax1.legend(loc='upper left', fontsize=11)
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels on bars
def add_value_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=8)

add_value_labels(bars1)
add_value_labels(bars2)
add_value_labels(bars3)

plt.tight_layout()
plt.savefig('loc_per_request_comparison.png', dpi=300, bbox_inches='tight')
print("[OK] Chart 1 saved: loc_per_request_comparison.png")

# Chart 2: Average LOC per engine
fig2, ax2 = plt.subplots(figsize=(10, 7))

engines = ['Web 1.0', 'RDFa', 'SPARQL']
averages = [web1_avg, rdfa_avg, sparql_avg]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

bars = ax2.bar(engines, averages, color=colors, alpha=0.8, width=0.6)

ax2.set_ylabel('Average Lines of Code (LOC)', fontsize=12, fontweight='bold')
ax2.set_title('Average Lines of Code per Function by Engine', fontsize=14, fontweight='bold', pad=20)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels on bars
for bar, avg in zip(bars, averages):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{avg:.1f}',
            ha='center', va='bottom', fontsize=14, fontweight='bold')

# Add a horizontal line for reference
ax2.axhline(y=np.mean(averages), color='gray', linestyle='--', linewidth=1, alpha=0.5, label=f'Overall Avg: {np.mean(averages):.1f}')
ax2.legend(fontsize=10)

plt.tight_layout()
plt.savefig('average_loc_per_engine.png', dpi=300, bbox_inches='tight')
print("[OK] Chart 2 saved: average_loc_per_engine.png")

# Chart 3: Bonus - Stacked comparison showing LOC distribution
fig3, ax3 = plt.subplots(figsize=(12, 7))

# Sort requests by total LOC for better visualization
total_locs = [(req, web1_locs[i] + rdfa_locs[i] + sparql_locs[i]) for i, req in enumerate(requests)]
sorted_indices = sorted(range(len(total_locs)), key=lambda i: total_locs[i])

sorted_requests = [requests[i] for i in sorted_indices]
sorted_web1 = [web1_locs[i] for i in sorted_indices]
sorted_rdfa = [rdfa_locs[i] for i in sorted_indices]
sorted_sparql = [sparql_locs[i] for i in sorted_indices]

x_pos = np.arange(len(sorted_requests))
width = 0.6

p1 = ax3.barh(x_pos, sorted_web1, width, label='Web 1.0', color='#FF6B6B', alpha=0.8)
p2 = ax3.barh(x_pos, sorted_rdfa, width, left=sorted_web1, label='RDFa', color='#4ECDC4', alpha=0.8)
p3 = ax3.barh(x_pos, sorted_sparql, width, 
              left=[sorted_web1[i] + sorted_rdfa[i] for i in range(len(sorted_requests))],
              label='SPARQL', color='#45B7D1', alpha=0.8)

ax3.set_yticks(x_pos)
ax3.set_yticklabels(sorted_requests)
ax3.set_xlabel('Total Lines of Code (LOC)', fontsize=12, fontweight='bold')
ax3.set_title('Stacked LOC Comparison: Total Code Required by Request', fontsize=14, fontweight='bold', pad=20)
ax3.legend(loc='lower right', fontsize=11)
ax3.grid(axis='x', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('stacked_loc_comparison.png', dpi=300, bbox_inches='tight')
print("[OK] Bonus Chart 3 saved: stacked_loc_comparison.png")

print("\n" + "="*60)
print("SUMMARY STATISTICS")
print("="*60)
print(f"Web 1.0   - Average: {web1_avg:.1f} LOC, Min: {min(web1_locs)}, Max: {max(web1_locs)}")
print(f"RDFa      - Average: {rdfa_avg:.1f} LOC, Min: {min(rdfa_locs)}, Max: {max(rdfa_locs)}")
print(f"SPARQL    - Average: {sparql_avg:.1f} LOC, Min: {min(sparql_locs)}, Max: {max(sparql_locs)}")
print(f"\nMost compact: Web 1.0 ({web1_avg:.1f} LOC avg)")
print(f"Most verbose: SPARQL ({sparql_avg:.1f} LOC avg)")
print(f"Difference: {sparql_avg - web1_avg:.1f} LOC (+{((sparql_avg - web1_avg)/web1_avg*100):.1f}%)")
print("="*60)
