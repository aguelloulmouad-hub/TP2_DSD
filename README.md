<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter" />
  <img src="https://img.shields.io/badge/Status-Terminé-success?style=for-the-badge" alt="Status" />
</p>

# TP2 - Simulation Multi-Agent avec Mesa

## 1. Introduction

Ce TP a pour objectif d’étudier comment des opinions individuelles évoluent au fil du temps lorsqu’elles sont influencées par leurs voisins. On utilise un modèle multi-agent sur une grille, où chaque agent représente une personne et a une opinion comprise entre 0 et 1.

Le principe est simple : chaque individu regarde les opinions de ses voisins, calcule une moyenne, puis se rapproche légèrement de cette moyenne selon un coefficient appelé alpha.

Ce type de modèle permet de comprendre comment un comportement local simple peut produire un résultat global, comme un consensus ou une baisse de dispersion dans la population.

---

## 2. Objectif du projet

Le but du modèle est de répondre à plusieurs questions :

- comment l’opinion d’un agent évolue avec le temps ?
- quel est l’impact du paramètre alpha ?
- la population finit-elle par se rapprocher d’un consensus ?
- comment mesurer la dispersion entre les opinions ?
- quels sont les effets d’une activation aléatoire des agents ?

---

## 3. Modèle utilisé

On travaille avec un système de type SMA (Système Multi-Agent) où :

- chaque agent a une opinion initiale aléatoire,
- chaque agent interagit avec ses voisins dans une grille,
- la mise à jour suit la formule :

$$
O_i^{t+1} = O_i^t + \alpha \times (\overline{O}_{\mathcal{N}_i}^t - O_i^t)
$$

Où :

- $O_i^t$ : opinion de l’agent i à l’instant t,
- $\overline{O}_{\mathcal{N}_i}^t$ : moyenne des opinions de ses voisins,
- $\alpha$ : force de l’influence sociale.

Si alpha est petit, l’agent change peu d’opinion à chaque pas. Si alpha est grand, il se rapproche rapidement de la moyenne de son environnement.

---

## 4. Fichiers du projet

- `Script_global.py` : script principal de base, utilisé pour visualiser l’évolution globale de l’opinion et de la variance.
- `Comparaison_alpha.py` : script avancé qui compare plusieurs valeurs de alpha et permet d’analyser leur influence.
- `TP2Mesa_Simulation_MA.ipynb` : version notebook du TP avec explications et questions d’analyse.
- `captures/` : dossier contenant les captures des figures générées.

---

## 5. Analyse du script global

Le script `Script_global.py` montre la dynamique globale de la population : la moyenne des opinions et la variance de dispersion.

### Figure globale 1 : évolution de la moyenne et de la variance

![Figure globale 1](captures/fig%20global%201.png)

Cette figure montre l’évolution de la moyenne générale de l’opinion dans le temps ainsi que la dispersion globale. On observe que la moyenne reste autour d’un niveau proche de 0,5, ce qui est normal car les opinions initiales sont distribuées aléatoirement. La variance, elle, diminue progressivement, ce qui traduit un rapprochement entre les individus.

### Figure globale 2 : trajectoires des opinions individuelles

![Figure globale 2](captures/fig%20global%202.png)

Cette figure présente un échantillon des trajectoires de plusieurs agents. On remarque que les opinions ont tendance à se rapprocher les unes des autres au cours du temps. Cela montre que les interactions locales suffisent à faire émerger une dynamique collective d’uniformisation.

### Interprétation

Le modèle montre qu’un système social très simple, basé uniquement sur des interactions locales, peut produire un comportement global cohérent : les opinions ne restent pas dispersées indéfiniment, elles tendent à converger.

---

## 6. Analyse du paramètre alpha

Le script `Comparaison_alpha.py` a pour but d’étudier l’effet de la variation de alpha. Cette partie est très importante car alpha représente la force d’influence sociale.

### Figure 1 : impact de alpha sur la moyenne globale

![Figure 1](captures/fig%201.png)

Cette première image montre l’évolution de la moyenne globale pour plusieurs valeurs de alpha. La moyenne reste dans une zone proche de 0,5, mais l’allure du graphique varie selon la vitesse de convergence. On remarque que plus alpha est élevé, plus la dynamique est rapide.

### Figure 2 : impact de alpha sur la dispersion

![Figure 2](captures/fig%202.png)

Ici, on observe la variance pour différentes valeurs de alpha. La variance diminue plus vite lorsque alpha est grand. Cela signifie que les opinions se rapprochent plus rapidement entre elles.

### Figure 3 : vitesse de convergence

![Figure 3](captures/fig%203.png)

Cette figure résume le temps nécessaire pour que la variance tombe en dessous d’un seuil fixé. On voit clairement que :

- alpha faible : convergence lente,
- alpha élevé : convergence rapide.

C’est la preuve que le coefficient alpha contrôle directement la vitesse d’ajustement entre les agents.

### Figure 4 : trajectoires pour alpha = 0.1

![Figure 4](captures/fig%204.png)

Pour alpha petit, les agents se déplacent doucement vers la moyenne de leurs voisins. Les courbes restent plus étalées longtemps, car la modification est faible à chaque étape. Cela donne une dynamique plus lente et plus progressive.

### Figure 5 : trajectoires pour alpha = 0.8

![Figure 5](captures/fig%205.png)

Pour alpha élevé, la progression est beaucoup plus rapide. Les opinions convergent plus vite, et les trajectoires se regroupent plus rapidement. On observe donc une forte influence sociale qui accélère le rapprochement entre individus.

### Conclusion de cette partie

Le paramètre alpha est le moteur de la vitesse de convergence du modèle. Il transforme le comportement global du système :

- alpha proche de 0 : interactions faibles, évolution lente,
- alpha proche de 1 : interactions fortes, convergence rapide.

---

## 7. Interprétation générale du système

Ce modèle montre qu’un phénomène complexe peut émerger à partir de règles simples. Les agents n’ont pas d’information globale sur l’ensemble de la population, mais en interagissant localement, ils produisent un comportement collectif cohérent.

On parle ici d’émergence : une propriété globale apparaît sans qu’aucun agent ne la décide directement. C’est le cas du consensus, qui résulte de la somme des interactions entre voisins.

---

## 8. Réponses aux questions d’analyse et de compréhension

### 1) Quel est l’impact précis du paramètre alpha sur la vitesse de convergence ?

Le paramètre alpha détermine combien un agent se rapproche de la moyenne de ses voisins. Plus alpha est grand, plus le changement est important à chaque étape.

- si alpha est petit, l’agent change peu et le système converge lentement ;
- si alpha est proche de 1, l’agent suit très fortement son voisinage et le consensus apparaît plus rapidement.

C’est exactement ce que montrent les figures de comparaison.

### 2) Pourquoi le système finit-il par converger vers un consensus ?

La mise à jour des opinions suit une moyenne pondérée :

$$
O_i^{t+1} = O_i^t + \alpha (\overline{O}_{\mathcal{N}_i}^t - O_i^t)
$$

Cette formule ramène chaque opinion vers la moyenne de ses voisins. Comme les agents se mettent à jour de manière répétée dans la grille, la différence entre opinion individuelle et opinion de voisinage diminue progressivement. Sans mécanisme de tolérance ou de polarisation, le système tend naturellement vers un état plus homogène.

### 3) Que signifie l’émergence dans ce modèle ?

L’émergence est le fait qu’un comportement global apparaisse à partir de règles locales. Ici, chaque agent suit une règle simple, mais au niveau de la population, on voit apparaître une dynamique collective : rapprochement, réduction de la variance et convergence vers un état commun.

On ne voit pas de plan global, mais les interactions locales produisent des effets globaux visibles sur les courbes.

### 4) Comment fonctionne l’activation des agents dans Mesa 3 ?

Dans Mesa 3, on n’utilise plus une boucle classique sur une liste de manière explicite. Les agents sont activés via :

- `self.agents.shuffle_do("step")`

Cela signifie que tous les agents sont appelés dans un ordre aléatoire. Cela évite les biais liés à l’ordre d’activation et correspond mieux à une dynamique sociale réelle où les individus ne se mettent pas tous à jour dans un ordre fixe.

### 5) Quelle est la différence entre `model_reporters` et `agent_reporters` ?

- `model_reporters` : collectent des valeurs globales du modèle, comme la moyenne et la variance de toutes les opinions.
- `agent_reporters` : collectent des informations pour chaque agent individuellement, comme son opinion au fil du temps.

Les deux sont nécessaires pour comprendre à la fois le comportement global du système et les changements de chaque individu.

### 6) Que se passe-t-il sur les bords de la grille ?

Le paramètre `torus=True` permet à la grille d’être circulaire. Un agent situé au bord a des voisins de l’autre côté de la grille. Cela évite les effets de bord et permet d’avoir un voisinage plus régulier et plus réaliste.

### 7) Comment introduire un biais de confirmation ?

On peut modifier la règle d’influence pour qu’un agent n’écoute un voisin que si l’écart entre leurs opinions est inférieur à un seuil epsilon. Autrement dit :

- si `|Oi - Oj| < epsilon`, l’agent se rapproche du voisin ;
- sinon, il ignore cette influence.

Ce mécanisme peut créer des clusters, des groupes de personnes proches les unes des autres, et favoriser la polarisation ou le maintien de communautés distinctes.

### 8) Si on devait utiliser un réseau social au lieu d’une grille, quelle structure utiliser ?

On pourrait utiliser une structure de type `NetworkGrid`, ou un graphe social où chaque nœud représente un individu et chaque arête représente une relation entre deux personnes. Les influenceurs très connectés seraient alors des nœuds avec beaucoup de liens, tandis que les individus isolés auraient moins de connexions.

Cela permettrait de modéliser des réseaux sociaux beaucoup plus réalistes que la grille classique.

---

## 9. Conclusion

Ce TP a permis de comprendre qu’une dynamique sociale peut être simulée à partir de règles très simples. La grille, les voisins et le coefficient alpha suffisent à produire des comportements collectifs intéressants : convergence, réduction de la variance, et même l’émergence de cohérence globale.

Le modèle montre aussi que la force d’influence sociale est un paramètre clé. Il détermine la vitesse à laquelle les opinions se rapprochent, et donc la vitesse à laquelle le système atteint un équilibre.

En résumé, ce projet illustre bien le principe central des systèmes multi-agents : des comportements locaux simples peuvent produire des phénomènes globaux complexes.

---

<p align="center">
  <strong>Réalisé par : Aguelloul Mouad</strong><br>
  <strong>Encadré par : Lhoussaine Daoudi</strong>
</p>

