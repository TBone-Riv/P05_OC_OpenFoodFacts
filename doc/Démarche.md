#User story

En tant qu'utilisateur je veux trouver rapidement un substitue.
-	Recherche produit
-	Navigation 

En tant qu'utilisateur je veux pouvoir acheter les substitues.
-	Affichage du lieu de vente du substitue

En tant qu'utilisateur je pouvoir retrouver un substitue énergisé.
-	Sauvegarde des substitues
-	Affichage des substitues sauvegardés

#Démarche

Une explication succincte des problèmes rencontrés des questions
posées durant le projet et des solutions et réponses apportées.


---

Q : Sur quels critères le système se base pour la sélection du substitue ?

R : Une note utilisant les Labels est associée aux produits. La requête SQL
récupère les produits en les triant par nova puit pas nutrie-score et enfin
par score associé au label (L’ordre nova > nurie-score > label peut être
changé dans les constantes). 

---

Q : Command reconnaitre un produit similaire pour le substitue ?

R : En utilisant les catégories. Deux produits sont considérés substituable
s’ils partagent un certain nombre de catégorie.

---

Q : La base Open Food Fact a beaucoup de doublon (ex : un pot de Nutella de
500g et un autre de 900g). Le programme traite-t-il ces cas ?

R : Les doublon sont l’imité par l’ajout de l’attribue unique à la colonne
nom des produits.

---
