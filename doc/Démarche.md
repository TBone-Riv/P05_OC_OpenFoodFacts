#Démarche

Une explication succincte des problèmes rencontrés des questions
posées durant le projet et des solutions et réponses apportées.

## Version 1 initialisation
Phase de réflexion sur la structure de la base de données et du programme.

---

Q : Sur quels critères le système se base pour la sélection du substitue ?

R : Un poids est associé aux attribues Label et Origine, le programme appellera
une méthode de la classe Produit qui prend en paramètre les préférences de
l’utilisateur et utilise les label, l’origine, la notation NOVA et le
nutri-score pour calculer la valeur du produit.

---

Q : Comment est attribué le poids des labels et des origines ?

R : De manière arbitraire pour les labels et en fonction de la distance à 
la France pour les origines.

---

Q : Command reconnaitre un produit similaire pour le substitue ?

R : En utilisant les catégories. Deux produits sont considérés substituable
s’ils partagent un certain nombre de catégorie. En cas de nombre de catégorie
enseigner insuffisant (les produit sont parfois incomplet) un autre critère
de sélection est encore à choisir.

---

Q : La base Open Food Fact a beaucoup de doublon (ex : un pot de Nutella de
500g et un autre de 900g). Le programme traite-t-il ces cas ?

R : Il est important que le programme détecte les doublons sinon il est
possible que les doublons se retrouve dans les propositions de substitue.

---

Q : Comment repérer les doublons ?

R : La question est encor à la réflexion mais si l’utilisation du nom coupler
à une correspondance parfaite des catégories. Mais si l’un des deux produits
n’a pas des informations complètes le problème risque d’être compliqué.

---