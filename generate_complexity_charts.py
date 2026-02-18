#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate algorithmic complexity analysis charts
Measures control flow complexity (if, else, for, while, try/except, etc.)
"""
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

print("="*80)
print("GENERATING ALGORITHMIC COMPLEXITY CHARTS")
print("="*80)

# ============================================================================
# CHART 1: Complexity per Request (Bar Chart)
# ============================================================================
fig1, ax1 = plt.subplots(figsize=(14, 7))

x = np.arange(len(requests))
width = 0.25

for i, method in enumerate(methods):
    complexities = [complexity_data[req][method] for req in requests]
    offset = (i - 1) * width
    bars = ax1.bar(x + offset, complexities, width,
                   label=method, color=colors[method], alpha=0.85)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

ax1.set_xlabel('Request', fontsize=12, fontweight='bold')
ax1.set_ylabel('Number of Branching Statements', fontsize=12, fontweight='bold')
ax1.set_title('Algorithmic Complexity: Branching Statements per Request\n(if, else, elif, for, while, try/except, filters)',
             fontsize=14, fontweight='bold', pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(requests)
ax1.legend(loc='upper left', fontsize=11)
ax1.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('complexity_by_request.png', dpi=300, bbox_inches='tight')
print("[OK] Chart 1: complexity_by_request.png")

# ============================================================================
# CHART 2: Average Complexity per Engine
# ============================================================================
fig2, ax2 = plt.subplots(figsize=(10, 7))

avg_complexity = {}
for method in methods:
    avg_complexity[method] = np.mean([complexity_data[req][method] for req in requests])

bars = ax2.bar(methods, [avg_complexity[m] for m in methods],
              color=[colors[m] for m in methods], alpha=0.85, width=0.6)

# Add value labels
for bar, method in zip(bars, methods):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}',
            ha='center', va='bottom', fontsize=14, fontweight='bold')

ax2.set_ylabel('Average Branching Statements', fontsize=12, fontweight='bold')
ax2.set_title('Average Algorithmic Complexity per Engine',
             fontsize=14, fontweight='bold', pad=20)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# Add reference line
avg_all = np.mean(list(avg_complexity.values()))
ax2.axhline(y=avg_all, color='gray', linestyle='--', linewidth=1.5, alpha=0.5,
           label=f'Overall Average: {avg_all:.1f}')
ax2.legend(fontsize=10)

plt.tight_layout()
plt.savefig('complexity_average.png', dpi=300, bbox_inches='tight')
print("[OK] Chart 2: complexity_average.png")

# ============================================================================
# CHART 3: Complexity Heatmap
# ============================================================================
fig3, ax3 = plt.subplots(figsize=(10, 8))

# Convert to DataFrame for heatmap
heatmap_data = pd.DataFrame(complexity_data).T
heatmap_data = heatmap_data[methods]  # Reorder columns

sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd',
           cbar_kws={'label': 'Number of Branches'}, ax=ax3,
           linewidths=0.5, linecolor='gray', vmin=0, vmax=10)

ax3.set_title('Algorithmic Complexity Heatmap\nHigher = More Branching Logic',
             fontsize=14, fontweight='bold', pad=20)
ax3.set_xlabel('Engine', fontsize=12, fontweight='bold')
ax3.set_ylabel('Request', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('complexity_heatmap.png', dpi=300, bbox_inches='tight')
print("[OK] Chart 3: complexity_heatmap.png")

# ============================================================================
# CHART 4: Cumulative Complexity (Stacked Bar)
# ============================================================================
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

# ============================================================================
# CHART 5: Complexity Distribution (Box Plot)
# ============================================================================
fig5, ax5 = plt.subplots(figsize=(10, 7))

data_for_boxplot = []
labels_for_boxplot = []

for method in methods:
    complexities = [complexity_data[req][method] for req in requests]
    data_for_boxplot.append(complexities)
    labels_for_boxplot.append(method)

bp = ax5.boxplot(data_for_boxplot, labels=labels_for_boxplot, patch_artist=True,
                 showmeans=True, meanline=True)

# Color the boxes
for patch, method in zip(bp['boxes'], methods):
    patch.set_facecolor(colors[method])
    patch.set_alpha(0.7)

ax5.set_ylabel('Number of Branching Statements', fontsize=12, fontweight='bold')
ax5.set_title('Complexity Distribution per Engine\nBox plot showing median, quartiles, and outliers',
             fontsize=14, fontweight='bold', pad=20)
ax5.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('complexity_distribution.png', dpi=300, bbox_inches='tight')
print("[OK] Chart 5: complexity_distribution.png")

# ============================================================================
# CHART 6: Complexity vs Request Type (Categorized)
# ============================================================================
fig6, ax6 = plt.subplots(figsize=(14, 7))

# Categorize requests by complexity level
simple_requests = ['R1', 'R2', 'R3']  # 1-2 branches
medium_requests = ['R4', 'R5', 'R6', 'R7', 'R8']  # 3-5 branches
complex_requests = ['R9', 'R10']  # 6+ branches

categories = {
    'Simple\n(R1-R3)': simple_requests,
    'Medium\n(R4-R8)': medium_requests,
    'Complex\n(R9-R10)': complex_requests
}

x_pos = np.arange(len(categories))
width = 0.25

for i, method in enumerate(methods):
    avg_by_category = []
    for category, reqs in categories.items():
        avg = np.mean([complexity_data[req][method] for req in reqs if req in complexity_data])
        avg_by_category.append(avg)
    
    offset = (i - 1) * width
    bars = ax6.bar(x_pos + offset, avg_by_category, width,
                   label=method, color=colors[method], alpha=0.85)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

ax6.set_ylabel('Average Branching Statements', fontsize=12, fontweight='bold')
ax6.set_title('Complexity by Request Category\nGrouped by algorithmic complexity level',
             fontsize=14, fontweight='bold', pad=20)
ax6.set_xticks(x_pos)
ax6.set_xticklabels(categories.keys())
ax6.legend(loc='upper left', fontsize=11)
ax6.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('complexity_by_category.png', dpi=300, bbox_inches='tight')
print("[OK] Chart 6: complexity_by_category.png")

# ============================================================================
# CHART 7: Complexity Reduction Factor
# ============================================================================
fig7, ax7 = plt.subplots(figsize=(14, 7))

# Calculate complexity reduction relative to Web 1.0
reduction_data = {}
for req in requests:
    reduction_data[req] = {}
    baseline = complexity_data[req]['Web 1.0']
    for method in ['RDFa', 'SPARQL']:
        if baseline > 0:
            reduction_data[req][method] = (baseline - complexity_data[req][method]) / baseline * 100
        else:
            reduction_data[req][method] = 0

x = np.arange(len(requests))
width = 0.35

for i, method in enumerate(['RDFa', 'SPARQL']):
    reductions = [reduction_data[req][method] for req in requests]
    offset = (i - 0.5) * width
    bars = ax7.bar(x + offset, reductions, width,
                   label=f'{method} vs Web 1.0', color=colors[method], alpha=0.85)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        if abs(height) > 5:  # Only show labels for significant differences
            ax7.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.0f}%',
                    ha='center', va='bottom' if height > 0 else 'top', 
                    fontsize=8, fontweight='bold')

ax7.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax7.set_xlabel('Request', fontsize=12, fontweight='bold')
ax7.set_ylabel('Complexity Reduction (%)', fontsize=12, fontweight='bold')
ax7.set_title('Algorithmic Complexity Reduction vs Web 1.0 Baseline\nPositive = Simpler, Negative = More Complex',
             fontsize=14, fontweight='bold', pad=20)
ax7.set_xticks(x)
ax7.set_xticklabels(requests)
ax7.legend(loc='lower right', fontsize=11)
ax7.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('complexity_reduction.png', dpi=300, bbox_inches='tight')
print("[OK] Chart 7: complexity_reduction.png")

# ============================================================================
# Statistics Summary
# ============================================================================
print("\n" + "="*80)
print("ALGORITHMIC COMPLEXITY STATISTICS")
print("="*80)

print("\nAverage Branching Statements per Engine:")
print("-" * 80)
for method in methods:
    avg = avg_complexity[method]
    total = total_complexity[method]
    min_val = min([complexity_data[req][method] for req in requests])
    max_val = max([complexity_data[req][method] for req in requests])
    
    print(f"{method:15s}: {avg:.2f} avg, {total} total, range [{min_val}-{max_val}]")

print("\nComplexity Ranking (Lower is Better):")
print("-" * 80)
sorted_methods = sorted(methods, key=lambda m: avg_complexity[m])
for rank, method in enumerate(sorted_methods, 1):
    medal = ['[1st]', '[2nd]', '[3rd]'][rank-1] if rank <= 3 else '     '
    print(f"{medal} {rank}. {method:15s} - {avg_complexity[method]:.2f} avg branches")

print("\nComplexity Reduction vs Web 1.0:")
print("-" * 80)
web1_avg = avg_complexity['Web 1.0']
for method in ['RDFa', 'SPARQL']:
    reduction = (web1_avg - avg_complexity[method]) / web1_avg * 100
    sign = "simpler" if reduction > 0 else "more complex"
    print(f"{method:15s}: {abs(reduction):.1f}% {sign} than Web 1.0")

print("\nMost Complex Functions:")
print("-" * 80)
for method in methods:
    most_complex = max(requests, key=lambda r: complexity_data[r][method])
    complexity = complexity_data[most_complex][method]
    print(f"{method:15s}: {most_complex} ({complexity} branches)")

print("\nComplexity Distribution:")
print("-" * 80)
for method in methods:
    complexities = [complexity_data[req][method] for req in requests]
    median = np.median(complexities)
    std = np.std(complexities)
    print(f"{method:15s}: median={median:.1f}, std={std:.2f}")

print("\n" + "="*80)
print("KEY INSIGHTS:")
print("="*80)

sparql_simpler = (avg_complexity['Web 1.0'] - avg_complexity['SPARQL']) / avg_complexity['Web 1.0'] * 100
print(f"\n1. SPARQL is {sparql_simpler:.1f}% simpler than Web 1.0")
print(f"   - SPARQL: {avg_complexity['SPARQL']:.1f} avg branches (declarative queries)")
print(f"   - Web 1.0: {avg_complexity['Web 1.0']:.1f} avg branches (procedural logic)")

print(f"\n2. Complexity scales with request difficulty:")
print(f"   - Simple requests (R1-R3): ~1-2 branches")
print(f"   - Medium requests (R4-R8): ~2-5 branches")
print(f"   - Complex requests (R9-R10): ~5-9 branches")

print(f"\n3. SPARQL maintains low complexity even for complex requests:")
print(f"   - R10 (most complex): Web 1.0=9, RDFa=8, SPARQL=5")
print(f"   - SPARQL pushes complexity to query engine (no explicit loops)")

print(f"\n4. Total complexity difference:")
print(f"   - Web 1.0: {total_complexity['Web 1.0']} total branches")
print(f"   - RDFa: {total_complexity['RDFa']} total branches")
print(f"   - SPARQL: {total_complexity['SPARQL']} total branches")
print(f"   - SPARQL has {total_complexity['Web 1.0'] - total_complexity['SPARQL']} fewer branches!")

print("\n" + "="*80)
print("All complexity charts generated successfully!")
print("="*80)
