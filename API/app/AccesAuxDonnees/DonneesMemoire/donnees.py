from app.Metier.Modele.Magasin import Magasin
from app.Metier.Modele.Film import Film

films = [
    Film(
        id=1,
        id_magasin=1,
        titre="Le Dernier Combat",
        genre="Action",
        resume="Un soldat tente de survivre dans un monde post-apocalyptique.",
        nbr_exemplaires_disponible=5
    ),
    Film(
        id=2,
        id_magasin=1,
        titre="Amour de Neige",
        genre="Romance",
        resume="Deux inconnus se rencontrent dans un chalet isolé.",
        nbr_exemplaires_disponible=0
    ),
    Film(
        id=3,
        id_magasin=2,
        titre="L’Ombre du Passé",
        genre="Thriller",
        resume="Un détective découvre un secret de famille bouleversant.",
        nbr_exemplaires_disponible=7
    ),
    Film(
        id=4,
        id_magasin=3,
        titre="Rires et Larmes",
        genre="Comédie dramatique",
        resume="Une mère célibataire apprend à rire à nouveau.",
        nbr_exemplaires_disponible=3
    ),
    Film(
        id=5,
        id_magasin=4,
        titre="L’Étoile du Nord",
        genre="Science-fiction",
        resume="Un équipage spatial se perd dans une galaxie lointaine.",
        nbr_exemplaires_disponible=4
    ),
    Film(
        id=6,
        id_magasin=5,
        titre="Sous la Pluie",
        genre="Drame",
        resume="Un musicien lutte contre sa dépendance et son passé.",
        nbr_exemplaires_disponible=0
    ),
    Film(
        id=7,
        id_magasin=6,
        titre="L’Invasion des Chats Zombies",
        genre="Horreur",
        resume="Des chats mutants attaquent une petite ville.",
        nbr_exemplaires_disponible=1
    ),
    Film(
        id=8,
        id_magasin=7,
        titre="Réalité Virtuelle",
        genre="Science-fiction",
        resume="Un programmeur est piégé dans son propre jeu.",
        nbr_exemplaires_disponible=9
    ),
    Film(
        id=9,
        id_magasin=8,
        titre="Cuisine en Folie",
        genre="Comédie",
        resume="Un chef maladroit essaie de sauver son restaurant.",
        nbr_exemplaires_disponible=6
    ),
    Film(
        id=10,
        id_magasin=9,
        titre="Les Rivages du Temps",
        genre="Fantastique",
        resume="Une jeune femme voyage à travers les époques.",
        nbr_exemplaires_disponible=0
    ),
]

# --- Création d’un dictionnaire films par magasin ---
films_par_magasin = {}
for film in films:
    films_par_magasin.setdefault(film.id_magasin, []).append(film)

# --- Liste des magasins avec leurs films ---
magasins = [
    Magasin(
        id=1,
        nom="BusterBlock Montréal",
        adresse="145 Rue Sainte-Catherine, Montréal, QC",
        telephone="514-890-1234",
        status=True,
        films=films_par_magasin.get(1, []),
    ),
    Magasin(
        id=2,
        nom="BusterBlock Laval",
        adresse="2100 Boulevard Le Corbusier, Laval, QC",
        telephone="450-322-8877",
        status=False,
        films=films_par_magasin.get(2, []),
    ),
    Magasin(
        id=3,
        nom="BusterBlock Québec",
        adresse="84 Rue Saint-Jean, Québec, QC",
        telephone="418-652-0911",
        status=True,
        films=films_par_magasin.get(3, []),
    ),
    Magasin(
        id=4,
        nom="BusterBlock Gatineau",
        adresse="200 Boulevard Gréber, Gatineau, QC",
        telephone="819-777-4321",
        status=True,
        films=films_par_magasin.get(4, []),
    ),
    Magasin(
        id=5,
        nom="BusterBlock Sherbrooke",
        adresse="91 Rue King Ouest, Sherbrooke, QC",
        telephone="819-563-2233",
        status=False,
        films=films_par_magasin.get(5, []),
    ),
    Magasin(
        id=6,
        nom="BusterBlock Trois-Rivières",
        adresse="50 Rue des Forges, Trois-Rivières, QC",
        telephone="819-370-9955",
        status=True,
        films=films_par_magasin.get(6, []),
    ),
    Magasin(
        id=7,
        nom="BusterBlock Longueuil",
        adresse="123 Rue Saint-Charles Ouest, Longueuil, QC",
        telephone="450-677-0910",
        status=True,
        films=films_par_magasin.get(7, []),
    ),
    Magasin(
        id=8,
        nom="BusterBlock Repentigny",
        adresse="79 Boulevard Brien, Repentigny, QC",
        telephone="450-581-1222",
        status=True,
        films=films_par_magasin.get(8, []),
    ),
    Magasin(
        id=9,
        nom="BusterBlock Drummondville",
        adresse="15 Rue Lindsay, Drummondville, QC",
        telephone="819-478-3344",
        status=True,
        films=films_par_magasin.get(9, []),
    ),
    Magasin(
        id=10,
        nom="BusterBlock Lévis",
        adresse="44 Route du Président-Kennedy, Lévis, QC",
        telephone="418-835-5566",
        status=False,
        films=films_par_magasin.get(10, []),  # Aucun film dans ta liste
    ),
]
