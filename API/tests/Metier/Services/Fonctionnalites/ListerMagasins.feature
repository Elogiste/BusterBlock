# language: fr

Fonctionnalité: Lister les magasins

    Scénario: Lister tous les magasins existants
        Étant donné un ensemble de magasins
        Lorsque je liste les magasins
        Alors la liste retournée contient tous les magasins
        Et chaque magasin doit être converti en réponse valide

    Scénario: Lister les magasins quand il n’y en a aucune
        Étant donné aucun magasin
        Lorsque je liste les magasins
        Alors la liste retournée doit être vide
