# language: fr

Fonctionnalité: Consulter le répertoire des films
  En tant qu'utilisateur de BusterBlock
  Je veux consulter le répertoire des films
  Afin de savoir si le choix est suffisant pour répondre à mes besoins

  Scénario: Consulter le répertoire complet des films
    Étant donné des films existent dans le système
    Lorsque je consulte le répertoire des films
    Alors le code de retour est 200
    Et la réponse contient la liste complète du répertoire des films

  Scénario: Consulter le répertoire filtré par genre
    Étant donné des films existent dans le système
    Lorsque je recherche les films du genre "Science-Fiction"
    Alors le code de retour est 200
    Et la réponse contient au moins un film
    Et tous les films retournés ont le genre "Science-Fiction"

  Scénario: Consulter le répertoire lorsque aucun film ne correspond
    Étant donné des films existent dans le système
    Lorsque je recherche les films avec le titre "Titre totalement inexistant"
    Alors le code de retour est 200
    Et la liste des films retournée est vide
