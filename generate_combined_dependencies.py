#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Combined Dependency Analysis Chart (French labels)
Shows structural + text dependencies in a single stacked bar chart
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Dependency data from robustness analysis
robustness_analysis = {
    'R1': {
        'Web 1.0': {
            'structural_deps': ['td[1]', 'first row position', 'table structure'],
            'text_deps': [],
        },
        'RDFa': {
            'structural_deps': [],
            'text_deps': [],
        }
    },
    'R2': {
        'Web 1.0': {
            'structural_deps': ['stat-box div', 'div[0]', 'p[0]', 'strong tag'],
            'text_deps': ['Specific text format with strong tag'],
        },
        'RDFa': {
            'structural_deps': ['stat-box class', 'first box'],
            'text_deps': ['"Nombre total de matchs" string'],
        }
    },
    'R3': {
        'Web 1.0': {
            'structural_deps': ['stat-box div', 'div[0]', 'p[1]', 'strong tag'],
            'text_deps': ['Specific text format with strong tag'],
        },
        'RDFa': {
            'structural_deps': ['stat-box class', 'first box'],
            'text_deps': ['"Nombre total de buts" string'],
        }
    },
    'R4': {
        'Web 1.0': {
            'structural_deps': ['stat-box div', 'div[1]', 'p[0] and p[1]', 'strong tags'],
            'text_deps': ['Colon separator', 'specific paragraph structure'],
        },
        'RDFa': {
            'structural_deps': [],
            'text_deps': [],
        }
    },
    'R5': {
        'Web 1.0': {
            'structural_deps': ['table', 'td[1] for name', 'td[7] for goals', 'rows[1:]'],
            'text_deps': [],
        },
        'RDFa': {
            'structural_deps': [],
            'text_deps': [],
        }
    },
    'R6': {
        'Web 1.0': {
            'structural_deps': ['table rows', 'td[0,1,2,3]', 'score class'],
            'text_deps': ['"/11/2008" date format'],
        },
        'RDFa': {
            'structural_deps': [],
            'text_deps': ['"/11/2008" date format'],
        }
    },
    'R7': {
        'Web 1.0': {
            'structural_deps': ['specific filename', 'div structure'],
            'text_deps': ['"Domicile" and "Victoire" strings'],
        },
        'RDFa': {
            'structural_deps': ['div structure'],
            'text_deps': ['"Domicile" and "Victoire" strings'],
        }
    },
    'R8': {
        'Web 1.0': {
            'structural_deps': ['h1 tag', 'specific filenames', 'div structure'],
            'text_deps': ['"Extérieur" and "Victoire" strings'],
        },
        'RDFa': {
            'structural_deps': ['div structure'],
            'text_deps': ['"Extérieur" and "Victoire" strings'],
        }
    },
    'R9': {
        'Web 1.0': {
            'structural_deps': ['rows[:6] slice', 'td[1]', 'td[2] and td[3]', 'score class'],
            'text_deps': ['Score format "x-y"'],
        },
        'RDFa': {
            'structural_deps': ['rows[:6] slice order'],
            'text_deps': ['Score format "x-y"'],
        }
    },
    'R10': {
        'Web 1.0': {
            'structural_deps': ['rows[0] and rows[2]', 'td[1]', 'td[0,1,2,3]', 'score class'],
            'text_deps': ['Score format "x-y"'],
        },
        'RDFa': {
            'structural_deps': ['rows[0] and rows[2] order'],
            'text_deps': ['Score format "x-y"'],
        }
    }
}

requests = [f'R{i}' for i in range(1, 11)]
methods = ['Web 1.0', 'RDFa']
colors_structural = {'Web 1.0': '#FF6B6B', 'RDFa': '#4ECDC4'}
colors_text = {'Web 1.0': '#C44569', 'RDFa': '#2C7A7B'}

print("="*80)
print("GÉNÉRATION DU GRAPHIQUE COMBINÉ DES DÉPENDANCES")
print("="*80)

# Count dependencies
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

# ============================================================================
# CHART: Combined Stacked Bar Chart
# ============================================================================
fig, ax = plt.subplots(figsize=(16, 8))

x = np.arange(len(requests))
width = 0.35

# For each method, create stacked bars
for i, method in enumerate(methods):
    offset = (i - 0.5) * width
    
    # Bottom bars: structural dependencies
    bars_structural = ax.bar(x + offset, structural_dep_counts[method], width,
                            label=f'{method} - Dépendances structurelles',
                            color=colors_structural[method], alpha=0.9,
                            edgecolor='black', linewidth=0.5)
    
    # Top bars: text dependencies (stacked on top)
    bars_text = ax.bar(x + offset, text_dep_counts[method], width,
                      bottom=structural_dep_counts[method],
                      label=f'{method} - Dépendances textuelles',
                      color=colors_text[method], alpha=0.9,
                      edgecolor='black', linewidth=0.5)
    
    # Add total count labels on top of stacked bars
    for j, (struct, text) in enumerate(zip(structural_dep_counts[method], 
                                           text_dep_counts[method])):
        total = struct + text
        if total > 0:
            ax.text(x[j] + offset, total + 0.2,
                   f'{total}',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')

# Customize chart
ax.set_xlabel('Requête', fontsize=13, fontweight='bold')
ax.set_ylabel('Nombre de dépendances', fontsize=13, fontweight='bold')
ax.set_title('Analyse Combinée des Dépendances DOM\nStructurelles (bas) + Textuelles (haut) par Requête',
            fontsize=15, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(requests, fontsize=11)
ax.legend(loc='upper left', fontsize=10, ncol=2)
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add summary statistics text box
total_structural_web1 = sum(structural_dep_counts['Web 1.0'])
total_text_web1 = sum(text_dep_counts['Web 1.0'])
total_structural_rdfa = sum(structural_dep_counts['RDFa'])
total_text_rdfa = sum(text_dep_counts['RDFa'])

summary_text = f"""TOTAL:
Web 1.0: {total_structural_web1 + total_text_web1} ({total_structural_web1} struct. + {total_text_web1} texte)
RDFa: {total_structural_rdfa + total_text_rdfa} ({total_structural_rdfa} struct. + {total_text_rdfa} texte)

Réduction: -{((total_structural_web1 + total_text_web1) - (total_structural_rdfa + total_text_rdfa))/(total_structural_web1 + total_text_web1)*100:.0f}%"""

ax.text(0.98, 0.97, summary_text,
       transform=ax.transAxes,
       fontsize=10,
       verticalalignment='top',
       horizontalalignment='right',
       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig('dependencies_combined_stacked.png', dpi=300, bbox_inches='tight')
print("[OK] Graphique sauvegardé: dependencies_combined_stacked.png")

# ============================================================================
# BONUS CHART: Comparison Bar Chart (Total Dependencies)
# ============================================================================
fig2, ax2 = plt.subplots(figsize=(14, 8))

# Calculate total dependencies per request per method
total_deps = {}
for method in methods:
    total_deps[method] = [
        structural_dep_counts[method][i] + text_dep_counts[method][i]
        for i in range(len(requests))
    ]

# Create grouped bars showing totals
for i, method in enumerate(methods):
    offset = (i - 0.5) * width
    bars = ax2.bar(x + offset, total_deps[method], width,
                  label=method,
                  color=colors_structural[method], alpha=0.85,
                  edgecolor='black', linewidth=0.8)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

ax2.set_xlabel('Requête', fontsize=13, fontweight='bold')
ax2.set_ylabel('Nombre total de dépendances', fontsize=13, fontweight='bold')
ax2.set_title('Comparaison du Total des Dépendances par Requête\n(Structurelles + Textuelles)',
             fontsize=15, fontweight='bold', pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels(requests, fontsize=11)
ax2.legend(loc='upper left', fontsize=12)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# Add reduction percentage annotations
for j in range(len(requests)):
    web1_total = total_deps['Web 1.0'][j]
    rdfa_total = total_deps['RDFa'][j]
    if web1_total > 0:
        reduction = ((web1_total - rdfa_total) / web1_total) * 100
        if reduction > 0:
            # Draw arrow and annotation
            mid_x = x[j]
            ax2.annotate(f'-{reduction:.0f}%',
                       xy=(mid_x, rdfa_total),
                       xytext=(mid_x, (web1_total + rdfa_total) / 2),
                       ha='center',
                       fontsize=8,
                       color='green',
                       fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', 
                               facecolor='lightgreen', alpha=0.7))

plt.tight_layout()
plt.savefig('dependencies_total_comparison.png', dpi=300, bbox_inches='tight')
print("[OK] Graphique bonus sauvegardé: dependencies_total_comparison.png")

# ============================================================================
# BONUS CHART 2: Pie Chart Comparison
# ============================================================================
fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(16, 7))

# Web 1.0 pie chart
web1_struct_total = sum(structural_dep_counts['Web 1.0'])
web1_text_total = sum(text_dep_counts['Web 1.0'])
web1_labels = [f'Structurelles\n({web1_struct_total})', f'Textuelles\n({web1_text_total})']
web1_sizes = [web1_struct_total, web1_text_total]
web1_colors_pie = ['#FF6B6B', '#C44569']

wedges1, texts1, autotexts1 = ax3a.pie(web1_sizes, labels=web1_labels, 
                                        autopct='%1.1f%%',
                                        startangle=90,
                                        colors=web1_colors_pie,
                                        textprops={'fontsize': 12, 'fontweight': 'bold'},
                                        explode=(0.05, 0))

ax3a.set_title(f'Web 1.0\nTotal: {web1_struct_total + web1_text_total} dépendances',
              fontsize=14, fontweight='bold', pad=20)

# RDFa pie chart
rdfa_struct_total = sum(structural_dep_counts['RDFa'])
rdfa_text_total = sum(text_dep_counts['RDFa'])
rdfa_labels = [f'Structurelles\n({rdfa_struct_total})', f'Textuelles\n({rdfa_text_total})']
rdfa_sizes = [rdfa_struct_total, rdfa_text_total]
rdfa_colors_pie = ['#4ECDC4', '#2C7A7B']

wedges2, texts2, autotexts2 = ax3b.pie(rdfa_sizes, labels=rdfa_labels,
                                        autopct='%1.1f%%',
                                        startangle=90,
                                        colors=rdfa_colors_pie,
                                        textprops={'fontsize': 12, 'fontweight': 'bold'},
                                        explode=(0.05, 0))

ax3b.set_title(f'RDFa\nTotal: {rdfa_struct_total + rdfa_text_total} dépendances',
              fontsize=14, fontweight='bold', pad=20)

plt.suptitle('Distribution des Types de Dépendances DOM',
            fontsize=16, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig('dependencies_pie_charts.png', dpi=300, bbox_inches='tight')
print("[OK] Graphique bonus 2 sauvegardé: dependencies_pie_charts.png")

# ============================================================================
# Statistics Summary (French)
# ============================================================================
print("\n" + "="*80)
print("STATISTIQUES DES DÉPENDANCES DOM")
print("="*80)

print("\nDépendances par moteur:")
print("-" * 80)
print(f"{'Moteur':<15} {'Structurelles':<15} {'Textuelles':<15} {'Total':<10} {'Moy/Req':<10}")
print("-" * 80)

for method in methods:
    struct_total = sum(structural_dep_counts[method])
    text_total = sum(text_dep_counts[method])
    total = struct_total + text_total
    avg = total / len(requests)
    print(f"{method:<15} {struct_total:<15} {text_total:<15} {total:<10} {avg:<10.1f}")

print("\nRéduction avec RDFa:")
print("-" * 80)

web1_struct = sum(structural_dep_counts['Web 1.0'])
web1_text = sum(text_dep_counts['Web 1.0'])
web1_total = web1_struct + web1_text

rdfa_struct = sum(structural_dep_counts['RDFa'])
rdfa_text = sum(text_dep_counts['RDFa'])
rdfa_total = rdfa_struct + rdfa_text

struct_reduction = ((web1_struct - rdfa_struct) / web1_struct) * 100 if web1_struct > 0 else 0
text_reduction = ((web1_text - rdfa_text) / web1_text) * 100 if web1_text > 0 else 0
total_reduction = ((web1_total - rdfa_total) / web1_total) * 100 if web1_total > 0 else 0

print(f"Dependances structurelles: -{struct_reduction:.1f}% ({web1_struct} -> {rdfa_struct})")
print(f"Dependances textuelles: -{text_reduction:.1f}% ({web1_text} -> {rdfa_text})")
print(f"TOTAL: -{total_reduction:.1f}% ({web1_total} -> {rdfa_total})")

print("\nRequêtes les plus dépendantes:")
print("-" * 80)
for method in methods:
    print(f"\n{method}:")
    total_by_req = [(req, total_deps[method][i]) 
                    for i, req in enumerate(requests)]
    top_3 = sorted(total_by_req, key=lambda x: x[1], reverse=True)[:3]
    for req, count in top_3:
        struct = structural_dep_counts[method][requests.index(req)]
        text = text_dep_counts[method][requests.index(req)]
        print(f"  {req}: {count} dépendances ({struct} struct. + {text} texte)")

print("\nRequêtes sans dépendances (RDFa):")
print("-" * 80)
zero_deps = [req for i, req in enumerate(requests) if total_deps['RDFa'][i] == 0]
if zero_deps:
    print(f"Requêtes totalement découplées: {', '.join(zero_deps)}")
    print(f"Pourcentage: {len(zero_deps)/len(requests)*100:.0f}% des requêtes")
else:
    print("Aucune requête totalement découplée")

print("\n" + "="*80)
print("INSIGHTS CLÉS:")
print("="*80)

print(f"\n1. RDFa élimine {struct_reduction:.0f}% des dépendances structurelles")
print(f"   - Web 1.0: {web1_struct} dépendances (indices, ordre, structure)")
print(f"   - RDFa: {rdfa_struct} dépendances (classes seulement)")

print(f"\n2. Dépendances textuelles réduites de {text_reduction:.0f}%")
print(f"   - Les deux moteurs souffrent de chaînes de texte codées en dur")
print(f"   - Solutions: propriétés sémantiques structurées, formats ISO")

print(f"\n3. Réduction totale: {total_reduction:.0f}% des dépendances")
print(f"   - De {web1_total} à {rdfa_total} dépendances")
print(f"   - {web1_total - rdfa_total} points de fragilité éliminés")

most_improved = max(requests, 
                   key=lambda r: total_deps['Web 1.0'][requests.index(r)] - 
                                total_deps['RDFa'][requests.index(r)])
improvement = (total_deps['Web 1.0'][requests.index(most_improved)] - 
              total_deps['RDFa'][requests.index(most_improved)])

print(f"\n4. Plus grande amélioration: {most_improved}")
print(f"   - Réduction de {improvement} dépendances")
web1_count = total_deps['Web 1.0'][requests.index(most_improved)]
rdfa_count = total_deps['RDFa'][requests.index(most_improved)]
print(f"   - Web 1.0: {web1_count} -> RDFa: {rdfa_count}")

print("\n" + "="*80)
print("Tous les graphiques ont été générés avec succès!")
print("="*80)
