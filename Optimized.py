"""
budget <- 500
meilleur combi <- a trouver

debut
récuperer les données du csv
realsier les combinaisons
regarder les les combinaisons qui ont un budget en dessous de 500€
comparer la combinaison avec celle rensigner pour garder la meilleure.
afficher la meilleure combi
fin
"""
import csv
import time
import tracemalloc
import os

# lecture et récuperation des données csv
def read_csv(file):
    """
    Docstring pour read_csv
    
    :param file: csv des actions
    :return: action sous forme de dictionnaire

    Récupère chaque colonne du csv pour l'affecter à une clé
    """	
    actions = []
    with open(file, mode='r', encoding='utf-8') as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            try:
                name = row["Actions #"]
                cost = float(row["Coût par action (en euros)"])
                benefit_percent = float(row["Bénéfice (après 2 ans)"][0:-1]) / 100
                benefit = cost * benefit_percent
                actions.append({
                    "name": name,
                    "cost": cost,
                    "benefit": benefit
                })
            except Exception:
                continue
    return actions

def optimazed_strategy(actions, max_budget):
    """
    Calcule la meilleure combinaison d'actions à acheter sans dépasser le budget, en maximisant le bénéfice total.

    Utilise l'algorithme Knapsack (sac à dos).

    Args:
        actions (list of dict): Liste de dictionnaires représentant les actions, avec les clés 'name', 'cost', 'benefit'.
        max_budget (int): Budget maximal autorisé (en euros).

    Returns:
        list: Liste des indices (1-based) des actions sélectionnées dans la meilleure combinaison.
    """
    # Initialisation des valeur du tableau
    n = len(actions)
    dp = [[0] * (max_budget + 1) for _ in range(n + 1)]
    # Remplissage du tableau dp
    for i in range(1, n + 1):
        cost = int(actions[i - 1]["cost"])
        benefit = actions[i - 1]["benefit"]
        for c in range(max_budget + 1):
            if cost <= c:
                dp[i][c] = max(dp[i - 1][c], benefit + dp[i - 1][c - cost])
            else:
                dp[i][c] = dp[i - 1][c]
    c = max_budget
    
    # Récupération de la meilleure combinaison.
    best_combination = []
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            cost = int(actions[i - 1]["cost"])
            best_combination.append(i)
            c -= cost
    return list(reversed(best_combination))

def WriteReport(selected_actions, total_cost, total_benefit, elapsed_time, current, peak):
    start_marker = "==== RAPPORT OPTIMIZED ===="
    end_marker = "==== FIN RAPPORT OPTIMIZED ===="
    rapport = f"\n{start_marker}\n"
    rapport += "Meilleure combinaison d'actions :\n"
    for action in selected_actions:
        rapport += f"- {action['name']} : coût = {action['cost']}€, bénéfice = {action['benefit']:.2f}€\n"
    rapport += f"\nCoût total : {total_cost:.2f}€\n"
    rapport += f"Bénéfice total après 2 ans : {total_benefit:.2f}€\n"
    rapport += "===============  Rapport temps et mémoire ===============\n"
    rapport += f"Durée d'execution: {elapsed_time:.4f} seconds\n"
    rapport += f'La consommation actuelle de mémoire est de: {current/1024:.1f}Ko\n'
    rapport += f'Le pic de mémoire utilisé est de : {peak/1048576:.1f}Mo\n'
    rapport += f"{end_marker}\n"

    # Lire l'ancien rapport s'il existe
    if os.path.exists("rapport.txt"):
        with open("rapport.txt", "r", encoding="utf-8") as f:
            contenu = f.read()
        # Supprimer l'ancienne section brute force
        import re
        contenu = re.sub(f"{start_marker}.*?{end_marker}\\n?", "", contenu, flags=re.DOTALL)
    else:
        contenu = ""
    # Réécrire le fichier avec la nouvelle section brute force en tête
    with open("rapport.txt", "w", encoding="utf-8") as f:
        f.write(rapport + contenu)

if __name__ == "__main__":
    # Définir le budget et le CSV à lire
    budget = 500
    actions = read_csv("Liste+d'actions+-+P7+Python+-+Feuille+1.csv")

    # Execution des boucles et mesure du temps nécessaire
    start_time = time.time()
    tracemalloc.start()
    best_combination = optimazed_strategy(actions, budget)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Récupération des données et print du résultat
    selected_actions = [actions[i - 1] for i in best_combination]
    total_cost = sum(a["cost"] for a in selected_actions)
    total_benefit = sum(a["benefit"] for a in selected_actions)

    print("\n=============== Rapport ===============")
    print("\nMeilleure combinaison d'actions :")
    for action in selected_actions:
        print(f"- {action['name']} : coût = {action['cost']}€, bénéfice = {action['benefit']:.2f}€")
    print(f"\nCoût total : {total_cost:.2f}€")
    print(f"Bénéfice total après 2 ans : {total_benefit:.2f}€")

    print("\n===============  Rapport temps et mémoire ===============")
    print(f"\nDurée d'execution: {elapsed_time:.4f} seconds")
    tracemalloc.start()
    optimazed_strategy(actions, budget)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f'\nLa consommation actuelle de mémoire est de: {current/1024:.1f}Ko')
    print(f'Le pic de mémoire utilisé est de : {peak/1048576:.1f}Mo')
    WriteReport(selected_actions, total_cost, total_benefit, elapsed_time, current, peak)
