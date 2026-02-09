# language: fr

Fonctionnalité: Récupération des magasins en stockage
  Objectif : Vérifier la cohérence des accès aux données

  Scénario: Récupérer tous les magasins existants
    Étant donné un jeu de données initial de magasins
    Lorsque je récupère tous les magasins
    Alors la liste des magasins retournée contient tous les magasins

  Scénario: Récupérer les magasins quand la liste est vide
    Étant donné un jeu de données vide de magasins
    Lorsque je récupère tous les magasins
    Alors la liste des magasins doit être vide

