# Importation des bibliothèques nécessaires
import mesa
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def safe_show():
    """Affiche les figures uniquement si le backend est interactif."""
    backend = plt.get_backend().lower()
    if backend == "agg":
        plt.close('all')
    else:
        plt.show()


class CitizenAgent(mesa.Agent):
    """Un individu ayant une opinion qui évolue selon ses voisins."""

    def __init__(self, model, alpha):
        # Initialisation de l'agent (l'enregistrement dans le modèle est automatique dans Mesa 3)
        super().__init__(model)

        # Opinion initiale tirée aléatoirement entre 0 et 1
        self.opinion = self.model.random.random()
        # Niveau d'influence sociale
        self.alpha = alpha

    def step(self):
        # Récupération des voisins (Moore = 8 voisins alentours, sans inclure le centre)
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)

        if len(neighbors) > 0:
            # Calcul de l'opinion moyenne des voisins
            mean_opinion = np.mean([neighbor.opinion for neighbor in neighbors])

            # Mise à jour de l'opinion selon la formule mathématique du TD
            self.opinion = self.opinion + self.alpha * (mean_opinion - self.opinion)


class OpinionModel(mesa.Model):
    """Modèle simulant la formation de l'opinion publique sur une grille."""

    def __init__(self, width, height, alpha=0.2, seed=None):
        super().__init__(seed=seed)

        # Espace discret (grille) avec bords communicants (torus=True)
        self.grid = mesa.space.MultiGrid(width, height, torus=True)
        self.alpha = alpha

        # Initialisation de la population : on place un agent par case
        for _, (x, y) in self.grid.coord_iter():
            agent = CitizenAgent(self, self.alpha)
            self.grid.place_agent(agent, (x, y))

        # Mise en place du collecteur de données pour l'observation
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Opinion Moyenne": lambda m: np.mean([a.opinion for a in m.agents]),
                "Variance (Dispersion)": lambda m: np.var([a.opinion for a in m.agents]),
            },
            agent_reporters={"Opinion": "opinion"},
        )

    def step(self):
        # 1. Collecter les données de l'état actuel
        self.datacollector.collect(self)
        # 2. Activer tous les agents dans un ordre aléatoire (Syntaxe Mesa 3)
        self.agents.shuffle_do("step")


def run_simulation(alpha, width=10, height=10, steps=50, seed=42):
    """Exécute la simulation pour une valeur de alpha donnée."""
    model = OpinionModel(width=width, height=height, alpha=alpha, seed=seed)
    for _ in range(steps):
        model.step()

    model_data = model.datacollector.get_model_vars_dataframe()
    agent_data = model.datacollector.get_agent_vars_dataframe()
    return model_data, agent_data


def convergence_time(model_data, threshold=0.01):
    """Retourne le premier tick où la variance descend sous le seuil."""
    variance = model_data["Variance (Dispersion)"]
    indices = np.where(variance <= threshold)[0]
    return indices[0] if len(indices) > 0 else None


# Paramètres du modèle
WIDTH = 10
HEIGHT = 10
ALPHA_VALUES = [0.1, 0.3, 0.5, 0.8, 1.0]
STEPS = 50

# 1) Analyse comparative sur plusieurs valeurs de alpha
results = {}
summary = []

for alpha in ALPHA_VALUES:
    model_data, agent_data = run_simulation(alpha=alpha, width=WIDTH, height=HEIGHT, steps=STEPS, seed=42)
    results[alpha] = (model_data, agent_data)
    summary.append(
        {
            "alpha": alpha,
            "moyenne_finale": float(model_data["Opinion Moyenne"].iloc[-1]),
            "variance_finale": float(model_data["Variance (Dispersion)"].iloc[-1]),
            "temps_convergence": convergence_time(model_data),
        }
    )

print("\n=== Synthèse comparative du paramètre alpha ===")
for item in summary:
    print(
        f"alpha={item['alpha']:.1f} | moyenne finale={item['moyenne_finale']:.4f} | "
        f"variance finale={item['variance_finale']:.4f} | temps convergence={item['temps_convergence']} ticks"
    )

# 2) Graphique 1 : évolution de la moyenne pour différents alpha
plt.figure(figsize=(12, 5))
for alpha, (model_data, _) in results.items():
    plt.plot(model_data.index, model_data["Opinion Moyenne"], label=f"alpha = {alpha}", linewidth=2)

plt.title("Impact de alpha sur la moyenne globale de l'opinion")
plt.xlabel("Ticks (Temps)")
plt.ylabel("Opinion moyenne")
plt.ylim(0, 1)
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
safe_show()

# 3) Graphique 2 : évolution de la variance pour différents alpha
plt.figure(figsize=(12, 5))
for alpha, (model_data, _) in results.items():
    plt.plot(model_data.index, model_data["Variance (Dispersion)"], label=f"alpha = {alpha}", linewidth=2)

plt.title("Impact de alpha sur la dispersion des opinions")
plt.xlabel("Ticks (Temps)")
plt.ylabel("Variance (dispersion)")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
safe_show()

# 4) Graphique 3 : vitesse de convergence (temps pour atteindre une variance faible)
threshold = 0.01
x = [item["alpha"] for item in summary]
y = [item["temps_convergence"] if item["temps_convergence"] is not None else STEPS for item in summary]

plt.figure(figsize=(8, 5))
plt.plot(x, y, marker='o', linewidth=2, color='tab:green')
plt.title("Vitesse de convergence en fonction de alpha")
plt.xlabel("alpha")
plt.ylabel("Nombre de ticks pour atteindre variance < 0.01")
plt.grid(alpha=0.3)
plt.tight_layout()
safe_show()

# 5) Affichage des trajectoires individuelles pour alpha très faible et très fort
for alpha in [0.1, 0.8]:
    model_data, agent_data = results[alpha]
    agent_opinions = agent_data.unstack(level=1)["Opinion"]
    sample_agents = agent_opinions.columns[:20]

    plt.figure(figsize=(10, 5))
    for agent_id in sample_agents:
        plt.plot(agent_opinions.index, agent_opinions[agent_id], alpha=0.7)

    plt.title(f"Trajectoires individuelles (alpha = {alpha})")
    plt.xlabel("Ticks (Temps)")
    plt.ylabel("Opinion [0, 1]")
    plt.ylim(0, 1)
    plt.tight_layout()
    safe_show()

# 6) Réponses synthétiques aux questions d'analyse et de compréhension
print("\n=== Réponses synthétiques ===")
print("1) Impact de alpha :")
print("   - alpha proche de 0 : les opinions changent très peu à chaque tick, donc la convergence est lente et la variance reste élevée longtemps.")
print("   - alpha proche de 1 : chaque agent se rapproche fortement de la moyenne de ses voisins, donc la convergence est rapide et la dispersion diminue plus vite.")
print("   - Visuellement, les courbes de variance chutent plus vite quand alpha est grand.")

print("\n2) Pourquoi le système converge vers un consensus :")
print("   - La mise à jour o_i^{t+1} = o_i^t + alpha*(moyenne_voisins - o_i^t) est une moyenne pondérée entre l'opinion actuelle et celle de ses voisins.")
print("   - Cela correspond à une moyenne locale répétée sur la grille, et la matrice de mise à jour est stochastique / doubly stochastic.")
print("   - En conséquence, la variance décroît globalement et le système tend vers un état plus homogène, sans seuil d'écart ni biais de confirmation.")
print("   - Sans mécanisme de polarisation ou de seuil de tolérance, la création de groupes stables est donc limitée dans ce modèle.")

print("\n3) Emergence :")
print("   - L'émergence apparaît parce que des interactions locales simples produisent un comportement global cohérent, visible sur les courbes de moyenne/variance.")
print("   - Les individus n'ont pas de plan global, mais la dynamique locale conduit à des structures collectives comme le consensus ou la baisse de dispersion.")

print("\n4) Activation des agents dans Mesa 3 :")
print("   - self.agents.shuffle_do('step') active tous les agents dans un ordre aléatoire, contrairement à une simple boucle sur une liste.")
print("   - L'aléatoire évite les biais d'ordre et reflète mieux un système social où les interactions sont désynchronisées.")

print("\n5) model_reporters vs agent_reporters :")
print("   - model_reporters mesurent des statistiques globales du modèle (moyenne, variance totale).")
print("   - agent_reporters suivent l'état de chaque agent (ex. opinion individuelle).")
print("   - Les deux sont nécessaires pour étudier à la fois le consensus global et les trajectoires individuelles.")

print("\n6) Effet de torus=True :")
print("   - Un agent situé au bord n'est pas isolé : ses voisins sont 'reliés' de l'autre côté de la grille.")
print("   - Ainsi, get_neighbors(...) récupère les cellules voisines en continu, sans rupture au bord.")

print("\n7) Biais de confirmation :")
print("   - On peut imposer qu'un agent ne soit influencé que si |o_i - o_j| < epsilon.")
print("   - Cela crée des zones localement homogènes, mais aussi des clusters persistants, ce qui peut produire une polarisation ou des communautés distinctes.")
print()

print("\n8) Réseau social au lieu d'une grille :")
print("   - On utiliserait une structure de type NetworkGrid ou un graphe social de Mesa, avec des nœuds et des liens.")
print("   - Les influenceurs très connectés peuvent être représentés par des nœuds de degré élevé, tandis que les utilisateurs isolés auront peu de liens.")

# Paramètre unique du TP (version plus simple si l'on veut exécuter un seul alpha)
# Pour une seule valeur de alpha, on peut toujours faire :
# model = OpinionModel(width=WIDTH, height=HEIGHT, alpha=0.5, seed=42)
# for _ in range(STEPS):
#     model.step()
# model_data = model.datacollector.get_model_vars_dataframe()
# agent_data = model.datacollector.get_agent_vars_dataframe()


# Version minimale d'affichage d'un seul modèle comme dans le TP initial
# Cette section est volontairement commentée pour garder le script analytique principal.
# ALPHA = 0.5
# model = OpinionModel(width=WIDTH, height=HEIGHT, alpha=ALPHA, seed=42)
# for i in range(STEPS):
#     model.step()
# model_data = model.datacollector.get_model_vars_dataframe()
# agent_data = model.datacollector.get_agent_vars_dataframe()
# fig, ax1 = plt.subplots(figsize=(10, 5))
# color = 'tab:blue'
# ax1.set_xlabel('Ticks (Temps)')
# ax1.set_ylabel('Opinion Moyenne', color=color)
# ax1.plot(model_data.index, model_data['Opinion Moyenne'], color=color, label='Moyenne')
# ax1.tick_params(axis='y', labelcolor=color)
# ax1.set_ylim(0, 1)
# ax2 = ax1.twinx()
# color = 'tab:red'
# ax2.set_ylabel('Variance (Dispersion)', color=color)
# ax2.plot(model_data.index, model_data['Variance (Dispersion)'], color=color, linestyle='--', label='Variance')
# ax2.tick_params(axis='y', labelcolor=color)
# plt.title('Évolution globale de l\'opinion (Moyenne et Dispersion)')
# fig.tight_layout()
# safe_show()

