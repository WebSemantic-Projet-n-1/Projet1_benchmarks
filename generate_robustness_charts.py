#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate DOM Robustness Analysis Charts
Analyzes how fragile each function is to DOM structure/text changes
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# Robustness scoring system (0-10 scale)
# 10 = Highly robust (semantic properties, no structure dependency)
# 5 = Moderate (some structure dependency)
# 0 = Extremely fragile (hardcoded indices, text matching, etc.)

robustness_analysis = {
    'R1': {
        'Web 1.0': {
            'score': 2,
            'structural_deps': ['td[1]', 'first row position', 'table structure'],
            'text_deps': [],
            'breaks_if': 'Add/remove table column, reorder rows',
            'severity': 'HIGH'
        },
        'RDFa': {
            'score': 8,
            'structural_deps': [],
            'text_deps': [],
            'breaks_if': 'Remove RDFa properties (unlikely)',
            'severity': 'LOW'
        }
    },
    'R2': {
        'Web 1.0': {
            'score': 1,
            'structural_deps': ['stat-box div', 'div[0]', 'p[0]', 'strong tag'],
            'text_deps': ['Specific text format with strong tag'],
            'breaks_if': 'Change div order, modify text format',
            'severity': 'CRITICAL'
        },
        'RDFa': {
            'score': 3,
            'structural_deps': ['stat-box class', 'first box'],
            'text_deps': ['"Nombre total de matchs" string'],
            'breaks_if': 'Change French text, modify class structure',
            'severity': 'HIGH'
        }
    },
    'R3': {
        'Web 1.0': {
            'score': 1,
            'structural_deps': ['stat-box div', 'div[0]', 'p[1]', 'strong tag'],
            'text_deps': ['Specific text format with strong tag'],
            'breaks_if': 'Change paragraph order, modify text format',
            'severity': 'CRITICAL'
        },
        'RDFa': {
            'score': 3,
            'structural_deps': ['stat-box class', 'first box'],
            'text_deps': ['"Nombre total de buts" string'],
            'breaks_if': 'Change French text, modify class structure',
            'severity': 'HIGH'
        }
    },
    'R4': {
        'Web 1.0': {
            'score': 1,
            'structural_deps': ['stat-box div', 'div[1]', 'p[0] and p[1]', 'strong tags'],
            'text_deps': ['Colon separator', 'specific paragraph structure'],
            'breaks_if': 'Reorder divs, change paragraph indices',
            'severity': 'CRITICAL'
        },
        'RDFa': {
            'score': 8,
            'structural_deps': [],
            'text_deps': [],
            'breaks_if': 'Remove RDFa properties',
            'severity': 'LOW'
        }
    },
    'R5': {
        'Web 1.0': {
            'score': 2,
            'structural_deps': ['table', 'td[1] for name', 'td[7] for goals', 'rows[1:]'],
            'text_deps': [],
            'breaks_if': 'Add/remove columns, reorder columns',
            'severity': 'HIGH'
        },
        'RDFa': {
            'score': 8,
            'structural_deps': [],
            'text_deps': [],
            'breaks_if': 'Remove RDFa properties',
            'severity': 'LOW'
        }
    },
    'R6': {
        'Web 1.0': {
            'score': 2,
            'structural_deps': ['table rows', 'td[0,1,2,3]', 'score class'],
            'text_deps': ['"/11/2008" date format'],
            'breaks_if': 'Change column order, modify date format',
            'severity': 'HIGH'
        },
        'RDFa': {
            'score': 7,
            'structural_deps': [],
            'text_deps': ['"/11/2008" date format'],
            'breaks_if': 'Change date format (minor risk)',
            'severity': 'MEDIUM'
        }
    },
    'R7': {
        'Web 1.0': {
            'score': 3,
            'structural_deps': ['specific filename', 'div structure'],
            'text_deps': ['"Domicile" and "Victoire" strings'],
            'breaks_if': 'Change French text, modify div structure',
            'severity': 'HIGH'
        },
        'RDFa': {
            'score': 3,
            'structural_deps': ['div structure'],
            'text_deps': ['"Domicile" and "Victoire" strings'],
            'breaks_if': 'Change French text (same as Web 1.0)',
            'severity': 'HIGH'
        }
    },
    'R8': {
        'Web 1.0': {
            'score': 3,
            'structural_deps': ['h1 tag', 'specific filenames', 'div structure'],
            'text_deps': ['"Extérieur" and "Victoire" strings'],
            'breaks_if': 'Change h1 location, modify text',
            'severity': 'HIGH'
        },
        'RDFa': {
            'score': 5,
            'structural_deps': ['div structure'],
            'text_deps': ['"Extérieur" and "Victoire" strings'],
            'breaks_if': 'Change French text (but has semantic name)',
            'severity': 'MEDIUM'
        }
    },
    'R9': {
        'Web 1.0': {
            'score': 2,
            'structural_deps': ['rows[:6] slice', 'td[1]', 'td[2] and td[3]', 'score class'],
            'text_deps': ['Score format "x-y"'],
            'breaks_if': 'Reorder rows, change column indices',
            'severity': 'HIGH'
        },
        'RDFa': {
            'score': 7,
            'structural_deps': ['rows[:6] slice order'],
            'text_deps': ['Score format "x-y"'],
            'breaks_if': 'Change row order (minor), score format',
            'severity': 'MEDIUM'
        }
    },
    'R10': {
        'Web 1.0': {
            'score': 2,
            'structural_deps': ['rows[0] and rows[2]', 'td[1]', 'td[0,1,2,3]', 'score class'],
            'text_deps': ['Score format "x-y"'],
            'breaks_if': 'Reorder ranking, change columns',
            'severity': 'HIGH'
        },
        'RDFa': {
            'score': 7,
            'structural_deps': ['rows[0] and rows[2] order'],
            'text_deps': ['Score format "x-y"'],
            'breaks_if': 'Change ranking order (minor risk)',
            'severity': 'MEDIUM'
        }
    }
}

requests = [f'R{i}' for i in range(1, 11)]
methods = ['Web 1.0', 'RDFa']
colors = {'Web 1.0': '#FF6B6B', 'RDFa': '#4ECDC4'}

print("="*80)
print("GENERATING DOM ROBUSTNESS ANALYSIS CHARTS")
print("="*80)

# Extract scores
robustness_scores = {}
for req in requests:
    robustness_scores[req] = {
        'Web 1.0': robustness_analysis[req]['Web 1.0']['score'],
        'RDFa': robustness_analysis[req]['RDFa']['score']
    }

# ============================================================================
# CHART 1: Robustness Scores per Request (Higher is better)
# ============================================================================
fig1, ax1 = plt.subplots(figsize=(14, 7))

x = np.arange(len(requests))
width = 0.35

for i, method in enumerate(methods):
    scores = [robustness_scores[req][method] for req in requests]
    offset = (i - 0.5) * width
    bars = ax1.bar(x + offset, scores, width,
                   label=method, color=colors[method], alpha=0.85)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

# Add color zones
ax1.axhspan(0, 3, alpha=0.15, color='red', label='CRITICAL (0-3)')
ax1.axhspan(3, 6, alpha=0.15, color='orange', label='HIGH RISK (3-6)')
ax1.axhspan(6, 10, alpha=0.15, color='green', label='ROBUST (6-10)')

ax1.set_xlabel('Request', fontsize=12, fontweight='bold')
ax1.set_ylabel('Robustness Score (0-10)', fontsize=12, fontweight='bold')
ax1.set_title('DOM Robustness Score by Request\nHigher = More Resistant to Structure/Text Changes',
             fontsize=14, fontweight='bold', pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(requests)
ax1.legend(loc='upper left', fontsize=10)
ax1.grid(axis='y', alpha=0.3, linestyle='--')
ax1.set_ylim(0, 10)

plt.tight_layout()
plt.savefig('robustness_scores.png', dpi=300, bbox_inches='tight')
print("[OK] Chart 1: robustness_scores.png")

# ============================================================================
# CHART 2: Average Robustness per Engine
# ============================================================================
fig2, ax2 = plt.subplots(figsize=(10, 7))

avg_robustness = {}
for method in methods:
    avg_robustness[method] = np.mean([robustness_scores[req][method] for req in requests])

bars = ax2.bar(methods, [avg_robustness[m] for m in methods],
              color=[colors[m] for m in methods], alpha=0.85, width=0.5)

# Add value labels
for bar, method in zip(bars, methods):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}/10',
            ha='center', va='bottom', fontsize=14, fontweight='bold')
    
    # Add percentage above
    percentage = (height / 10) * 100
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
            f'({percentage:.0f}% robust)',
            ha='center', va='bottom', fontsize=11, style='italic')

# Add color zones
ax2.axhspan(0, 3, alpha=0.1, color='red')
ax2.axhspan(3, 6, alpha=0.1, color='orange')
ax2.axhspan(6, 10, alpha=0.1, color='green')

ax2.set_ylabel('Average Robustness Score', fontsize=12, fontweight='bold')
ax2.set_title('Average DOM Robustness by Engine',
             fontsize=14, fontweight='bold', pad=20)
ax2.grid(axis='y', alpha=0.3, linestyle='--')
ax2.set_ylim(0, 10)

plt.tight_layout()
plt.savefig('robustness_average.png', dpi=300, bbox_inches='tight')
print("[OK] Chart 2: robustness_average.png")

# ============================================================================
# CHART 3: Robustness Heatmap
# ============================================================================
fig3, ax3 = plt.subplots(figsize=(8, 10))

heatmap_data = pd.DataFrame(robustness_scores).T
heatmap_data = heatmap_data[methods]

sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='RdYlGn',
           cbar_kws={'label': 'Robustness Score'}, ax=ax3,
           linewidths=0.5, linecolor='gray', vmin=0, vmax=10)

ax3.set_title('DOM Robustness Heatmap\nGreen = Robust, Red = Fragile',
             fontsize=14, fontweight='bold', pad=20)
ax3.set_xlabel('Engine', fontsize=12, fontweight='bold')
ax3.set_ylabel('Request', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('robustness_heatmap.png', dpi=300, bbox_inches='tight')
print("[OK] Chart 3: robustness_heatmap.png")

# ============================================================================
# CHART 4: Dependency Count Analysis
# ============================================================================
fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(16, 7))

# Count structural dependencies
structural_dep_counts = {}
text_dep_counts = {}

for method in methods:
    structural_dep_counts[method] = [
        len(robustness_analysis[req][method]['structural_deps']) 
        for req in requests
    ]
    text_dep_counts[method] = [
        len(robustness_analysis[req][method]['text_deps'])
        for req in requests
    ]

# Chart 4a: Structural Dependencies
x = np.arange(len(requests))
width = 0.35

for i, method in enumerate(methods):
    offset = (i - 0.5) * width
    bars = ax4a.bar(x + offset, structural_dep_counts[method], width,
                    label=method, color=colors[method], alpha=0.85)

ax4a.set_xlabel('Request', fontsize=11, fontweight='bold')
ax4a.set_ylabel('Number of Structural Dependencies', fontsize=11, fontweight='bold')
ax4a.set_title('Structural Dependencies Count\n(HTML structure, column indices, order)',
              fontsize=12, fontweight='bold')
ax4a.set_xticks(x)
ax4a.set_xticklabels(requests)
ax4a.legend(loc='upper left', fontsize=10)
ax4a.grid(axis='y', alpha=0.3, linestyle='--')

# Chart 4b: Text Dependencies
for i, method in enumerate(methods):
    offset = (i - 0.5) * width
    bars = ax4b.bar(x + offset, text_dep_counts[method], width,
                    label=method, color=colors[method], alpha=0.85)

ax4b.set_xlabel('Request', fontsize=11, fontweight='bold')
ax4b.set_ylabel('Number of Text Dependencies', fontsize=11, fontweight='bold')
ax4b.set_title('Text Dependencies Count\n(Hardcoded strings, date formats)',
              fontsize=12, fontweight='bold')
ax4b.set_xticks(x)
ax4b.set_xticklabels(requests)
ax4b.legend(loc='upper left', fontsize=10)
ax4b.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('robustness_dependencies.png', dpi=300, bbox_inches='tight')
print("[OK] Chart 4: robustness_dependencies.png")

# ============================================================================
# CHART 5: Risk Severity Distribution
# ============================================================================
fig5, axes = plt.subplots(1, 2, figsize=(14, 6))

severity_colors = {'CRITICAL': '#D32F2F', 'HIGH': '#FF6F00', 'MEDIUM': '#FFA726', 'LOW': '#66BB6A'}

for idx, method in enumerate(methods):
    severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
    
    for req in requests:
        severity = robustness_analysis[req][method]['severity']
        severity_counts[severity] += 1
    
    # Filter out zero counts
    filtered_severities = {k: v for k, v in severity_counts.items() if v > 0}
    
    wedges, texts, autotexts = axes[idx].pie(
        filtered_severities.values(),
        labels=filtered_severities.keys(),
        autopct='%1.0f%%',
        startangle=90,
        colors=[severity_colors[s] for s in filtered_severities.keys()],
        textprops={'fontsize': 11, 'fontweight': 'bold'}
    )
    
    axes[idx].set_title(f'{method}\nRisk Severity Distribution',
                       fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig('robustness_risk_severity.png', dpi=300, bbox_inches='tight')
print("[OK] Chart 5: robustness_risk_severity.png")

# ============================================================================
# CHART 6: Robustness Improvement (RDFa vs Web 1.0)
# ============================================================================
fig6, ax6 = plt.subplots(figsize=(14, 7))

improvements = []
for req in requests:
    web1_score = robustness_scores[req]['Web 1.0']
    rdfa_score = robustness_scores[req]['RDFa']
    improvement = rdfa_score - web1_score
    improvements.append(improvement)

bar_colors = ['green' if imp > 0 else 'gray' if imp == 0 else 'red' for imp in improvements]
bars = ax6.bar(x, improvements, color=bar_colors, alpha=0.85, width=0.6)

# Add value labels
for bar, imp in zip(bars, improvements):
    height = bar.get_height()
    label = f'+{int(imp)}' if imp > 0 else f'{int(imp)}' if imp < 0 else '0'
    va = 'bottom' if imp >= 0 else 'top'
    offset = 0.2 if imp >= 0 else -0.2
    ax6.text(bar.get_x() + bar.get_width()/2., height + offset,
            label,
            ha='center', va=va, fontsize=10, fontweight='bold')

ax6.axhline(y=0, color='black', linestyle='-', linewidth=1.5)
ax6.set_xlabel('Request', fontsize=12, fontweight='bold')
ax6.set_ylabel('Robustness Improvement (RDFa - Web 1.0)', fontsize=12, fontweight='bold')
ax6.set_title('Robustness Improvement with RDFa\nPositive = RDFa is More Robust',
             fontsize=14, fontweight='bold', pad=20)
ax6.set_xticks(x)
ax6.set_xticklabels(requests)
ax6.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('robustness_improvement.png', dpi=300, bbox_inches='tight')
print("[OK] Chart 6: robustness_improvement.png")

# ============================================================================
# CHART 7: Breaking Point Analysis
# ============================================================================
fig7, ax7 = plt.subplots(figsize=(14, 10))

# Create break scenarios matrix
break_scenarios = {
    'Add/Remove Column': [],
    'Reorder Columns': [],
    'Change Text': [],
    'Modify Classes': [],
    'Reorder Rows': []
}

scenario_impacts = {
    'Web 1.0': {
        'Add/Remove Column': ['R1', 'R5', 'R6', 'R9', 'R10'],
        'Reorder Columns': ['R1', 'R5', 'R6', 'R9', 'R10'],
        'Change Text': ['R2', 'R3', 'R6', 'R7', 'R8'],
        'Modify Classes': ['R2', 'R3', 'R4', 'R6'],
        'Reorder Rows': ['R1', 'R5', 'R9', 'R10']
    },
    'RDFa': {
        'Add/Remove Column': [],
        'Reorder Columns': [],
        'Change Text': ['R2', 'R3', 'R6', 'R7', 'R8'],
        'Modify Classes': ['R2', 'R3'],
        'Reorder Rows': ['R9', 'R10']
    }
}

# Create impact matrix
impact_matrix = []
scenarios_list = list(break_scenarios.keys())

for scenario in scenarios_list:
    web1_impacts = len(scenario_impacts['Web 1.0'][scenario])
    rdfa_impacts = len(scenario_impacts['RDFa'][scenario])
    impact_matrix.append([web1_impacts, rdfa_impacts])

impact_df = pd.DataFrame(impact_matrix, 
                         index=scenarios_list,
                         columns=methods)

sns.heatmap(impact_df, annot=True, fmt='d', cmap='YlOrRd',
           cbar_kws={'label': 'Number of Affected Functions'}, ax=ax7,
           linewidths=0.5, linecolor='gray')

ax7.set_title('Breaking Point Analysis\nNumber of Functions Affected by Each DOM Change Type',
             fontsize=14, fontweight='bold', pad=20)
ax7.set_xlabel('Engine', fontsize=12, fontweight='bold')
ax7.set_ylabel('DOM Modification Type', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('robustness_breaking_points.png', dpi=300, bbox_inches='tight')
print("[OK] Chart 7: robustness_breaking_points.png")

# ============================================================================
# Statistics Summary
# ============================================================================
print("\n" + "="*80)
print("DOM ROBUSTNESS STATISTICS")
print("="*80)

print("\nAverage Robustness Scores (0-10 scale):")
print("-" * 80)
for method in methods:
    avg = avg_robustness[method]
    percentage = (avg / 10) * 100
    print(f"{method:15s}: {avg:.2f}/10 ({percentage:.0f}% robust)")

print("\nRobustness Improvement (RDFa vs Web 1.0):")
print("-" * 80)
improvement_avg = avg_robustness['RDFa'] - avg_robustness['Web 1.0']
improvement_pct = (improvement_avg / avg_robustness['Web 1.0']) * 100
print(f"Average improvement: +{improvement_avg:.2f} points ({improvement_pct:.1f}% better)")
print(f"Best improvements:")
for req in requests:
    imp = robustness_scores[req]['RDFa'] - robustness_scores[req]['Web 1.0']
    if imp >= 5:
        print(f"  - {req}: +{imp} points (Web 1.0: {robustness_scores[req]['Web 1.0']}, RDFa: {robustness_scores[req]['RDFa']})")

print("\nRisk Severity Breakdown:")
print("-" * 80)
for method in methods:
    print(f"\n{method}:")
    severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
    for req in requests:
        severity = robustness_analysis[req][method]['severity']
        severity_counts[severity] += 1
    
    for severity, count in severity_counts.items():
        if count > 0:
            print(f"  {severity:10s}: {count} functions ({count*10}%)")

print("\nMost Fragile Functions (Score <= 2):")
print("-" * 80)
for method in methods:
    print(f"\n{method}:")
    fragile = [(req, robustness_scores[req][method]) 
               for req in requests 
               if robustness_scores[req][method] <= 2]
    for req, score in sorted(fragile, key=lambda x: x[1]):
        breaks = robustness_analysis[req][method]['breaks_if']
        print(f"  {req} (score={score}): Breaks if {breaks}")

print("\nDependency Analysis:")
print("-" * 80)
for method in methods:
    avg_struct = np.mean(structural_dep_counts[method])
    avg_text = np.mean(text_dep_counts[method])
    total_struct = sum(structural_dep_counts[method])
    total_text = sum(text_dep_counts[method])
    print(f"\n{method}:")
    print(f"  Structural dependencies: {avg_struct:.1f} avg, {total_struct} total")
    print(f"  Text dependencies: {avg_text:.1f} avg, {total_text} total")

print("\n" + "="*80)
print("KEY INSIGHTS:")
print("="*80)

print("\n1. RDFa provides 2.5x better robustness on average:")
print(f"   - RDFa: {avg_robustness['RDFa']:.1f}/10 ({(avg_robustness['RDFa']/10)*100:.0f}% robust)")
print(f"   - Web 1.0: {avg_robustness['Web 1.0']:.1f}/10 ({(avg_robustness['Web 1.0']/10)*100:.0f}% robust)")

print("\n2. Web 1.0 critical vulnerabilities:")
most_fragile_web1 = min(requests, key=lambda r: robustness_scores[r]['Web 1.0'])
print(f"   - {sum(1 for r in requests if robustness_scores[r]['Web 1.0'] <= 2)}/10 functions critically fragile")
print(f"   - Most fragile: {most_fragile_web1} (score={robustness_scores[most_fragile_web1]['Web 1.0']})")
print(f"   - Total structural deps: {sum(structural_dep_counts['Web 1.0'])}")

print("\n3. RDFa semantic properties eliminate structural coupling:")
print(f"   - {sum(1 for r in requests if robustness_scores[r]['RDFa'] >= 7)}/10 functions highly robust (>= 7/10)")
print(f"   - Only {sum(structural_dep_counts['RDFa'])} structural dependencies vs {sum(structural_dep_counts['Web 1.0'])} for Web 1.0")

print("\n4. Biggest robustness gains (RDFa vs Web 1.0):")
improvements_sorted = sorted(
    [(req, robustness_scores[req]['RDFa'] - robustness_scores[req]['Web 1.0']) 
     for req in requests],
    key=lambda x: x[1],
    reverse=True
)
for req, imp in improvements_sorted[:5]:
    if imp > 0:
        print(f"   - {req}: +{imp} points improvement")

print("\n5. Remaining vulnerabilities in RDFa:")
rdfa_vulnerable = [req for req in requests if robustness_scores[req]['RDFa'] <= 5]
print(f"   - {len(rdfa_vulnerable)} functions still have medium risk")
for req in rdfa_vulnerable:
    reason = robustness_analysis[req]['RDFa']['breaks_if']
    print(f"   - {req}: {reason}")

print("\n" + "="*80)
print("All robustness charts generated successfully!")
print("="*80)
