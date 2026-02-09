import os
from pathlib import Path
from pytest_bdd import scenarios, given, when, then
from tests.AccesAuxDonnees.DAO.DonneesTest.donneesMagasins import magasins_test

cheminScenarios = Path(__file__).parent / "Fonctionnalites" / "ObtenirMagasins.feature"
scenarios(str(cheminScenarios))

@given("un jeu de données initial de magasins", target_fixture="attendues")
def définir_données(magasin_dao):
    magasin_dao.vider_tables(["magasins", "films"])
    for magasin in magasins_test:
        magasin_dao.ajouter_magasin(magasin)  # utiliser la DAO pour insérer
    return magasins_test

@given("un jeu de données vide de magasins")
def définir_données_vide(magasin_dao):
    magasin_dao.vider_tables(["magasins", "films"])
    return []

@when("je récupère tous les magasins", target_fixture="reçues")
def récupérer_données(magasin_dao):
    return magasin_dao.obtenir_tous_les_magasins()

@then("la liste des magasins retournée contient tous les magasins")
def vérifier_liste(attendues, reçues):
    # assert attendues == reçues
    assert len(attendues) == len(reçues)
    for m_att, m_rec in zip(attendues, reçues):
        assert m_att.id == m_rec.id
        assert m_att.nom == m_rec.nom
        assert m_att.adresse == m_rec.adresse
        assert m_att.telephone == m_rec.telephone
        assert m_att.status == m_rec.status

@then("la liste des magasins doit être vide")
def vérifier_vide(reçues):
    assert reçues == []
