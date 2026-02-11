# Réalisation du projet en pseudo code python

# Importation des bibliothèques nécessaires
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
	with open(file, mode ='r', encoding='utf-8') as f:
		csvreader = csv.DictReader(f)
		for row in csvreader:
			try:
				name = row["Actions #"]
				cost = float(row["Coût par action (en euros)"])
				benefit_percent = float(row["Bénéfice (après 2 ans)"][0:-1])/100
				benefit = cost * benefit_percent
				actions.append({
					"name": name,
					"cost": cost,
                    "benefit": benefit
                })
				benefit = cost * benefit_percent
			except Exception:
				continue
	return actions

def generate_combinations(actions):
    """
    Génère toutes les combinaisons possibles d'une liste d'actions.

    Args:
    La liste des actions sous forme de dictionnaires.

    Returns:
    Une liste de combinaisons, chaque combinaison étant une liste d'actions (dictionnaires).
    """
    combinations = []
    n = len(actions)
    for i in range(1, 2 ** n):
        combination = []
        for j in range(n):
            if i & (1 << j):
                combination.append(actions[j])
        combinations.append(combination)
    return combinations


def find_best_investment(actions, budget):
    """
    Trouve la meilleure combinaison d'investissement pour un budget donné en maximisant le profit.

    Args:
    La liste des actions sous forme de dictionnaires (nom, coût, bénéfice).
    Le budget maximal.

    Returns:
    La meilleure combinaison d'actions (liste de dictionnaires), le bénéfice maximal et le coût total de la combinaison.
    """
    best_combination = []
    max_profit = 0
    min_cost = float('inf')

    all_combinations = generate_combinations(actions)

    for combination in all_combinations:
        total_cost = sum(action['cost'] for action in combination)
        if total_cost <= budget:
            profit = sum(action['benefit'] for action in combination)
            ratio = profit / total_cost if total_cost > 0 else 0
            if profit > max_profit or (profit == max_profit and total_cost < min_cost):
                max_profit = profit
                best_combination = combination
                min_cost = total_cost

    return best_combination, max_profit, min_cost

def WriteReport(selected_actions, total_cost, total_benefit, elapsed_time, current, peak):
    start_marker = "==== RAPPORT BRUTE FORCE ===="
    end_marker = "==== FIN RAPPORT BRUTE FORCE ===="
    rapport = f"\n{start_marker}\n"
    rapport += "Meilleure combinaison d'actions :\n"
    for action in selected_actions:
        rapport += f"- {action['name']} : coût = {action['cost']}€, bénéfice = {action['benefit']:.2f}€\n"
    rapport += f"\nCoût total : {total_cost:.2f}€\n"
    rapport += f"Bénéfice total après 2 ans : {total_benefit:.2f}€\n"
    rapport += "===============  Rapport temps et mémoire ===============\n"
    rapport += f"Durée d'execution: {elapsed_time:.4f} seconds\n"
    rapport +=f'La consommation actuelle de mémoire est de: {current/1024:.1f}Ko\n'
    rapport +=f'Le pic de mémoire utilisé est de : {peak/1048576:.1f}Mo\n'
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
    budget = 500
    actions = read_csv("Liste+d'actions+-+P7+Python+-+Feuille+1.csv")

    start_time = time.time()
    best, benefit, cost = find_best_investment(actions, budget)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("\n=============== Rapport ===============")
    print("\nMeilleure combinaison d'actions :")
    for action in best:
        print(f"- {action['name']} (coût : {action['cost']} €, bénéfice : {action['benefit']:.2f} €)")
    print(f"\nCoût total : {cost:.2f} €")
    print(f"Bénéfice total après 2 ans : {benefit:.2f} €")

    print("\n===============  Rapport temps et mémoire ===============")
    print(f"Durée d'éxecution: {elapsed_time:.4f}")
    tracemalloc.start()
    find_best_investment(actions, budget)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f'\nLa consommation actuelle de mémoire est de: {current/1024:.1f}Ko')
    print(f'Le pic de mémoire utilisé est de : {peak/1048576:.1f}Mo')
    WriteReport(best, cost, benefit, elapsed_time, current, peak)

