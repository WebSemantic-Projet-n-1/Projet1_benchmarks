#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère des graphiques de comparaison de benchmarks à partir de benchmark_results.csv
Compare les temps d'exécution entre Web 1.0, RDFa et SPARQL Endpoint
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# Charger les résultats des benchmarks
df = pd.read_csv('benchmark_results.csv', sep=';')

# Nettoyer les noms de méthodes pour un meilleur affichage
df['method'] = df['method'].replace({'Knowledge Graph': 'Knowledge Graph'})

# Définir la palette de couleurs pour la cohérence
COLORS = {
    'Web 1.0': '#FF6B6B',
    'RDFa': '#4ECDC4',
    'SPARQL Endpoint': '#45B7D1'
}

REQUESTS = [f'R{i}' for i in range(1, 11)]

print("="*80)
print("GÉNÉRATION DES GRAPHIQUES DE COMPARAISON DES BENCHMARKS")
print("="*80)

# ============================================================================
# GRAPHIQUE 1: Comparaison du temps de traitement côté serveur (server_ms)
# ============================================================================
fig1, ax1 = plt.subplots(figsize=(14, 7))

server_data = df[df['metric'] == 'server_ms']
pivot_server = server_data.pivot(index='question', columns='method', values='mean_ms')
pivot_server = pivot_server.reindex(REQUESTS)

x = np.arange(len(REQUESTS))
width = 0.2

for i, method in enumerate(['Web 1.0', 'RDFa', 'SPARQL Endpoint']):
    if method in pivot_server.columns:
        offset = (i - 1) * width
        bars = ax1.bar(x + offset, pivot_server[method], width, 
                      label=method, color=COLORS[method], alpha=0.85)
        
        # Ajouter les étiquettes de valeur sur les barres (seulement si < 50ms pour la lisibilité)
        for bar in bars:
            height = bar.get_height()
            if height < 50:
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}',
                        ha='center', va='bottom', fontsize=7, rotation=0)

ax1.set_xlabel('Requête', fontsize=12, fontweight='bold')
ax1.set_ylabel('Temps de traitement serveur (ms)', fontsize=12, fontweight='bold')
ax1.set_title('Comparaison du temps de traitement côté serveur par requête', 
             fontsize=14, fontweight='bold', pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(REQUESTS)
ax1.legend(loc='upper left', fontsize=10)
ax1.grid(axis='y', alpha=0.3, linestyle='--')
ax1.set_yscale('log')  # Échelle logarithmique car R9 est beaucoup plus lent
ax1.set_ylabel('Temps de traitement serveur (ms) - Échelle log', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('benchmark_server_time.png', dpi=300, bbox_inches='tight')
print("[OK] Graphique 1: benchmark_server_time.png (Traitement côté serveur)")

# ============================================================================
# GRAPHIQUE 2: Comparaison du temps aller-retour côté client (client_ms)
# ============================================================================
fig2, ax2 = plt.subplots(figsize=(14, 7))

client_data = df[df['metric'] == 'client_ms']
pivot_client = client_data.pivot(index='question', columns='method', values='mean_ms')
pivot_client = pivot_client.reindex(REQUESTS)

for i, method in enumerate(['Web 1.0', 'RDFa', 'SPARQL Endpoint']):
    if method in pivot_client.columns:
        offset = (i - 1) * width
        bars = ax2.bar(x + offset, pivot_client[method], width,
                      label=method, color=COLORS[method], alpha=0.85)
        
        for bar in bars:
            height = bar.get_height()
            if height < 50:
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}',
                        ha='center', va='bottom', fontsize=7)

ax2.set_xlabel('Requête', fontsize=12, fontweight='bold')
ax2.set_ylabel('Temps aller-retour client (ms) - Échelle log', fontsize=12, fontweight='bold')
ax2.set_title('Comparaison du temps aller-retour côté client par requête',
             fontsize=14, fontweight='bold', pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels(REQUESTS)
ax2.legend(loc='upper left', fontsize=10)
ax2.grid(axis='y', alpha=0.3, linestyle='--')
ax2.set_yscale('log')

plt.tight_layout()
plt.savefig('benchmark_client_time.png', dpi=300, bbox_inches='tight')
print("[OK] Graphique 2: benchmark_client_time.png (Aller-retour client)")

# ============================================================================
# GRAPHIQUE 3: Comparaison du temps de rendu navigateur (render_ms)
# ============================================================================
fig3, ax3 = plt.subplots(figsize=(14, 7))

render_data = df[df['metric'] == 'render_ms']
pivot_render = render_data.pivot(index='question', columns='method', values='mean_ms')
pivot_render = pivot_render.reindex(REQUESTS)

for i, method in enumerate(['Web 1.0', 'RDFa', 'SPARQL Endpoint']):
    if method in pivot_render.columns:
        offset = (i - 1) * width
        bars = ax3.bar(x + offset, pivot_render[method], width,
                      label=method, color=COLORS[method], alpha=0.85)

ax3.set_xlabel('Requête', fontsize=12, fontweight='bold')
ax3.set_ylabel('Temps de rendu navigateur (ms)', fontsize=12, fontweight='bold')
ax3.set_title('Comparaison du temps de rendu navigateur par requête',
             fontsize=14, fontweight='bold', pad=20)
ax3.set_xticks(x)
ax3.set_xticklabels(REQUESTS)
ax3.legend(loc='upper left', fontsize=10)
ax3.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('benchmark_render_time.png', dpi=300, bbox_inches='tight')
print("[OK] Graphique 3: benchmark_render_time.png (Rendu navigateur)")

# ============================================================================
# GRAPHIQUE 4: Performance moyenne sur toutes les requêtes
# ============================================================================
fig4, (ax4a, ax4b, ax4c) = plt.subplots(1, 3, figsize=(18, 6))

# Calculer les moyennes pour chaque métrique
metrics = ['server_ms', 'client_ms', 'render_ms']
metric_labels = ['Traitement serveur', 'Aller-retour client', 'Rendu navigateur']
axes = [ax4a, ax4b, ax4c]

for idx, (metric, label, ax) in enumerate(zip(metrics, metric_labels, axes)):
    metric_data = df[df['metric'] == metric]
    avg_by_method = metric_data.groupby('method')['mean_ms'].mean()
    
    methods = ['Web 1.0', 'RDFa', 'SPARQL Endpoint']
    values = [avg_by_method.get(m, 0) for m in methods]
    colors_list = [COLORS[m] for m in methods]
    
    bars = ax.bar(range(len(methods)), values, color=colors_list, alpha=0.85)
    
    # Ajouter les étiquettes de valeur
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.1f}',
               ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_ylabel('Temps moyen (ms)', fontsize=11, fontweight='bold')
    ax.set_title(f'{label}\nTemps moyen', fontsize=12, fontweight='bold')
    ax.set_xticks(range(len(methods)))
    ax.set_xticklabels(methods, rotation=15, ha='right')
    ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.suptitle('Temps d\'exécution moyen par métrique et moteur', 
            fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('benchmark_averages.png', dpi=300, bbox_inches='tight')
print("[OK] Graphique 4: benchmark_averages.png (Moyennes générales)")

# ============================================================================
# GRAPHIQUE 5: Carte thermique des temps de traitement serveur
# ============================================================================
fig5, ax5 = plt.subplots(figsize=(12, 8))

server_data = df[df['metric'] == 'server_ms']
heatmap_data = server_data.pivot(index='question', columns='method', values='mean_ms')
heatmap_data = heatmap_data.reindex(REQUESTS)
heatmap_data = heatmap_data[['Web 1.0', 'RDFa', 'SPARQL Endpoint']]

# Utiliser une échelle logarithmique pour une meilleure visualisation
heatmap_data_log = np.log10(heatmap_data + 1)

sns.heatmap(heatmap_data_log, annot=heatmap_data, fmt='.1f', cmap='YlOrRd',
           cbar_kws={'label': 'Log10(Temps de traitement + 1)'}, ax=ax5,
           linewidths=0.5, linecolor='gray')

ax5.set_title('Carte thermique du temps de traitement serveur (ms)\nColoration en échelle log, valeurs réelles affichées',
             fontsize=14, fontweight='bold', pad=20)
ax5.set_xlabel('Moteur', fontsize=12, fontweight='bold')
ax5.set_ylabel('Requête', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('benchmark_heatmap.png', dpi=300, bbox_inches='tight')
print("[OK] Graphique 5: benchmark_heatmap.png (Carte thermique de performance)")

# ============================================================================
# GRAPHIQUE 6: Variabilité de la performance (écart-type)
# ============================================================================
fig6, ax6 = plt.subplots(figsize=(14, 7))

server_stdev = df[df['metric'] == 'server_ms']
pivot_stdev = server_stdev.pivot(index='question', columns='method', values='stdev_ms')
pivot_stdev = pivot_stdev.reindex(REQUESTS)

for i, method in enumerate(['Web 1.0', 'RDFa', 'SPARQL Endpoint']):
    if method in pivot_stdev.columns:
        offset = (i - 1) * width
        ax6.bar(x + offset, pivot_stdev[method], width,
               label=method, color=COLORS[method], alpha=0.85)

ax6.set_xlabel('Requête', fontsize=12, fontweight='bold')
ax6.set_ylabel('Écart-type (ms)', fontsize=12, fontweight='bold')
ax6.set_title('Cohérence de la performance (Écart-type du temps serveur)',
             fontsize=14, fontweight='bold', pad=20)
ax6.set_xticks(x)
ax6.set_xticklabels(REQUESTS)
ax6.legend(loc='upper left', fontsize=10)
ax6.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('benchmark_variability.png', dpi=300, bbox_inches='tight')
print("[OK] Graphique 6: benchmark_variability.png (Cohérence de la performance)")

# ============================================================================
# GRAPHIQUE 7: Comparaison d'accélération (relatif à la référence Web 1.0)
# ============================================================================
fig7, ax7 = plt.subplots(figsize=(14, 7))

server_pivot = df[df['metric'] == 'server_ms'].pivot(
    index='question', columns='method', values='mean_ms'
).reindex(REQUESTS)

# Calculer l'accélération relative à Web 1.0
speedup_data = {}
for method in ['RDFa', 'SPARQL Endpoint']:
    if method in server_pivot.columns:
        # Accélération = référence / méthode (>1 signifie plus rapide, <1 signifie plus lent)
        speedup_data[method] = server_pivot['Web 1.0'] / server_pivot[method]

speedup_df = pd.DataFrame(speedup_data, index=REQUESTS)

for i, method in enumerate(['RDFa', 'SPARQL Endpoint']):
    if method in speedup_df.columns:
        offset = (i - 0.5) * width
        bars = ax7.bar(x + offset, speedup_df[method], width,
                      label=method, color=COLORS[method], alpha=0.85)
        
        # Ajouter les étiquettes de valeur
        for bar in bars:
            height = bar.get_height()
            ax7.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}x',
                    ha='center', va='bottom' if height > 1 else 'top', 
                    fontsize=8)

# Ajouter une ligne horizontale à y=1 (référence)
ax7.axhline(y=1, color='red', linestyle='--', linewidth=2, 
           label='Référence Web 1.0', alpha=0.7)

ax7.set_xlabel('Requête', fontsize=12, fontweight='bold')
ax7.set_ylabel('Facteur d\'accélération (relatif à Web 1.0)', fontsize=12, fontweight='bold')
ax7.set_title('Accélération de la performance relative à la référence Web 1.0\n(>1 = plus rapide, <1 = plus lent)',
             fontsize=14, fontweight='bold', pad=20)
ax7.set_xticks(x)
ax7.set_xticklabels(REQUESTS)
ax7.legend(loc='upper right', fontsize=10)
ax7.grid(axis='y', alpha=0.3, linestyle='--')
ax7.set_yscale('log')
ax7.set_ylabel('Facteur d\'accélération (échelle log)', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('benchmark_speedup.png', dpi=300, bbox_inches='tight')
print("[OK] Graphique 7: benchmark_speedup.png (Accélération relative)")

# ============================================================================
# RÉSUMÉ DES STATISTIQUES
# ============================================================================
print("\n" + "="*80)
print("RÉSUMÉ DES STATISTIQUES DES BENCHMARKS")
print("="*80)

for metric, label in [('server_ms', 'Traitement serveur'), 
                      ('client_ms', 'Aller-retour client'),
                      ('render_ms', 'Rendu navigateur')]:
    print(f"\nTemps de {label} (ms):")
    print("-" * 80)
    
    metric_data = df[df['metric'] == metric]
    avg_by_method = metric_data.groupby('method')['mean_ms'].mean().sort_values()
    
    for method, avg_time in avg_by_method.items():
        print(f"  {method:20s}: {avg_time:8.2f} ms (moyenne)")
    
    fastest = avg_by_method.index[0]
    slowest = avg_by_method.index[-1]
    ratio = avg_by_method[slowest] / avg_by_method[fastest]
    
    print(f"\n  Plus rapide: {fastest} ({avg_by_method[fastest]:.2f} ms)")
    print(f"  Plus lent: {slowest} ({avg_by_method[slowest]:.2f} ms)")
    print(f"  Ratio de vitesse: {ratio:.2f}x plus lent")

# Requêtes les plus problématiques
print("\n" + "="*80)
print("REQUÊTES LES PLUS LENTES (Temps de traitement serveur)")
print("="*80)

server_data = df[df['metric'] == 'server_ms']
for method in ['Web 1.0', 'RDFa', 'SPARQL Endpoint']:
    method_data = server_data[server_data['method'] == method]
    slowest_3 = method_data.nlargest(3, 'mean_ms')[['question', 'mean_ms']]
    
    print(f"\n{method}:")
    for _, row in slowest_3.iterrows():
        print(f"  {row['question']}: {row['mean_ms']:.2f} ms")

print("\n" + "="*80)
print("Tous les graphiques ont été générés avec succès!")
print("="*80)
