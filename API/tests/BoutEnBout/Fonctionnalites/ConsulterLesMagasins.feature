# language: fr

Fonctionnalité: Consultation de la liste des magasins
  En tant qu'utilisateur,
  Je veux consulter la liste des magasins avec leurs détails (id, nom, adresse, téléphone, status),
  Afin de savoir où un film est disponible.

  Scénario: Consulter la liste des magasins existants
    Étant donné un utilisateur
    Quand il demande la liste des magasins
    Alors le système retourne tous les magasins avec leurs informations (id, nom, adresse, téléphone, status)

  Scénario: Consulter la liste lorsqu'aucun magasin n'existe
    Étant donné qu'il n'existe aucun magasin
    Quand l'utilisateur demande la liste des magasins
    Alors le système retourne une liste vide
    Et un message indiquant qu'aucun magasin n'est disponible

  Scénario: Accès à la liste des magasins par un utilisateur non-authentifié
    Étant donné un utilisateur non-authentifié
    Quand il consulte la liste des magasins
    Alors l'accès est possible avec un statut 200 OK si la liste est publique
    Et le système renvoie un statut 401 Unauthorized si la liste est protégée
