# # language: fr

# Fonctionnalité: Conversion Magasin vers MagasinReponse
  # Objectif : Vérifier que la conversion est correcte pour les magasins avec et sans films

  # Scénario: Conversion d'un magasin contenant des films
    # Étant donné un magasin contenant 5 films
    # Lorsque je le convertis en réponse
    # Alors le nombre de films disponibles doit être 5
    # Et les autres champs doivent être identiques

  # Scénario: Conversion d'un magasin sans film
    # Étant donné un magasin sans film
    # Lorsque je la convertis en réponse
    # Alors le nombre de films disponibles doit être 0
    # Et les autres champs doivent être identiques

