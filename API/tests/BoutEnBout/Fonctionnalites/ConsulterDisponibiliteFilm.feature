# language: fr

Fonctionnalité: Consulter la disponibilité d'un film
  En tant qu'utilisateur
  Je veux voir uniquement les magasins où un film spécifique est disponible
  Afin de choisir facilement où le louer

  Scénario: Rechercher un film disponible dans des magasins
    Étant donné un utilisateur
    Lorsque je recherche le film avec le titre "Inception"
    Alors le système affiche uniquement les magasins où le film est disponible avec le nombre de copies restantes

  Scénario: Rechercher un film qui n'est disponible dans aucun magasin
    Étant donné un utilisateur
    Lorsque je recherche le film avec le titre "Film Inexistant"
    Alors le système indique que le film n'est disponible dans aucun magasin

  Scénario: Rechercher un film avec un identifiant invalide
    Étant donné un utilisateur
    Lorsque je recherche le film avec l'identifiant 9999
    Alors le système retourne une erreur 400 ou 404
