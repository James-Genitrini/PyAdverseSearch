#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de validation complète de l'implémentation PN-Search.
Exécute tous les tests et affiche un rapport de statut.
"""

import sys
import unittest

def print_header(title):
    """Affiche un en-tête formaté"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_section(title):
    """Affiche une section"""
    print(f"\n>>> {title}")
    print("-" * 70)

def run_tests(test_module):
    """Exécute les tests d'un module et retourne le résultat"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_module)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful(), result.testsRun

def main():
    """Fonction principale de validation"""
    print_header("VALIDATION COMPLÈTE DE L'IMPLÉMENTATION PN-SEARCH")

    print("\nCe script valide que l'implémentation PN-Search est complète et fonctionnelle.")

    all_success = True
    total_tests = 0

    # 1. Tests unitaires
    print_section("1. Tests unitaires de PN-Search")
    success, count = run_tests('PyAdverseSearch.test.test_pnsearch')
    all_success = all_success and success
    total_tests += count

    # 2. Tests d'intégration
    print_section("2. Tests d'intégration avec le système existant")
    success, count = run_tests('PyAdverseSearch.test.test_integration_pnsearch')
    all_success = all_success and success
    total_tests += count

    # 3. Import du module
    print_section("3. Vérification des imports")
    try:
        from PyAdverseSearch.classes.pnsearch import PNSearch, PNNode, ProofStatus
        from PyAdverseSearch.classes.algorithm import choose_best_move
        print("✅ Tous les imports fonctionnent correctement")
    except ImportError as e:
        print(f"❌ Erreur d'import : {e}")
        all_success = False

    # 4. Test rapide fonctionnel
    print_section("4. Test fonctionnel rapide")
    try:
        from PyAdverseSearch.classes.pnsearch import PNSearch
        from PyAdverseSearch.classes.game import Game
        from PyAdverseSearch.test.state_tictactoe import TicTacToeState

        board = [['X', 'X', ' '], ['O', 'O', ' '], [' ', ' ', ' ']]
        state = TicTacToeState(board)
        game = Game(
            initial_state=state,
            possible_actions=lambda s: s.get_possible_moves(),
            is_terminal=lambda s: s.is_game_over(),
            winner_function=lambda s: s.get_winner(),
            utility=lambda s: s.get_utility(),
            heuristic=lambda s: s.evaluate(),
            isMaxStarting=True
        )
        state.game = game
        state.player = "MAX"

        pn = PNSearch(game=game, max_nodes=1000)
        best_move = pn.choose_best_move(state)

        if best_move:
            print("✅ Test fonctionnel réussi : PN-Search trouve un coup")
            stats = pn.get_statistics()
            print(f"   Nœuds explorés : {stats['nodes_explored']}")
            print(f"   Table de transposition : {stats['transposition_table_size']} entrées")
        else:
            print("⚠️  Aucun coup trouvé (peut arriver selon max_nodes)")
    except Exception as e:
        print(f"❌ Erreur lors du test fonctionnel : {e}")
        all_success = False

    # 5. Vérification de l'API unifiée
    print_section("5. Vérification de l'API unifiée")
    try:
        from PyAdverseSearch.classes.algorithm import choose_best_move

        best_move = choose_best_move('pnsearch', game, state, max_nodes=1000)
        print("✅ Intégration avec choose_best_move() réussie")
    except Exception as e:
        print(f"❌ Erreur avec l'API unifiée : {e}")
        all_success = False

    # Rapport final
    print_header("RAPPORT FINAL")

    print(f"\nNombre total de tests exécutés : {total_tests}")

    if all_success:
        print("\n" + "🎉" * 35)
        print("\n✅ SUCCÈS : Tous les tests passent !")
        print("\n   L'implémentation PN-Search est COMPLÈTE et FONCTIONNELLE")
        print("\n" + "🎉" * 35)
        print("\n")
        print("Prochaines étapes :")
        print("  1. Consultez QUICKSTART_PNSEARCH.md pour l'utilisation")
        print("  2. Lisez PNSEARCH_README.md pour la théorie")
        print("  3. Examinez les exemples dans PyAdverseSearch/test/")
        print("  4. Lancez : python -m PyAdverseSearch.test.demo_pnsearch_simple")
        return 0
    else:
        print("\n" + "❌" * 35)
        print("\n❌ ÉCHEC : Certains tests ont échoué")
        print("\n" + "❌" * 35)
        return 1

if __name__ == "__main__":
    sys.exit(main())

