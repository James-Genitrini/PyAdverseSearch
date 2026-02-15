# FILE: PyAdverseSearch/test/example_pnsearch_usage.py

"""
Exemple d'utilisation de l'algorithme PN-Search (Proof-Number Search).

Ce fichier démontre comment utiliser PNSearch pour résoudre des fins de partie
au Tic-Tac-Toe et autres jeux.
"""

from PyAdverseSearch.classes.pnsearch import PNSearch
from PyAdverseSearch.classes.game import Game
from PyAdverseSearch.test.state_tictactoe import TicTacToeState


def display_board(board):
    """Affiche le plateau de jeu de manière lisible"""
    print("\n" + "=" * 13)
    for i, row in enumerate(board):
        print(f" {row[0]} | {row[1]} | {row[2]} ")
        if i < len(board) - 1:
            print("---+---+---")
    print("=" * 13 + "\n")


def example_1_winning_in_one_move():
    """
    Exemple 1 : Position où X (MAX) peut gagner en un coup.
    PN-Search devrait trouver le coup gagnant rapidement.
    """
    print("=" * 60)
    print("EXEMPLE 1 : Position gagnante en un coup pour X")
    print("=" * 60)

    # Configuration du plateau
    board = [
        ['X', 'X', ' '],  # X peut gagner en jouant en (0, 2)
        ['O', 'O', ' '],
        [' ', ' ', ' ']
    ]

    print("Position initiale :")
    display_board(board)

    # Création de l'état et du jeu
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

    # Création et exécution de PN-Search
    print("Lancement de PN-Search...")
    pn = PNSearch(game=game, max_nodes=10000, use_transposition_table=True)
    best_move = pn.choose_best_move(state)

    # Affichage des résultats
    if best_move:
        print("Meilleur coup trouvé :")
        display_board(best_move.board)
    else:
        print("Aucun coup trouvé.")

    # Statistiques
    stats = pn.get_statistics()
    print(f"Statistiques de recherche :")
    print(f"  - Nœuds explorés : {stats['nodes_explored']}")
    print(f"  - Taille table de transposition : {stats['transposition_table_size']}")
    print()


def example_2_complex_endgame():
    """
    Exemple 2 : Position de fin de partie plus complexe.
    Démontre la capacité de PN-Search à analyser plusieurs coups à l'avance.
    """
    print("=" * 60)
    print("EXEMPLE 2 : Fin de partie complexe")
    print("=" * 60)

    board = [
        ['X', ' ', 'O'],
        [' ', 'X', ' '],
        ['O', ' ', ' ']
    ]

    print("Position initiale :")
    display_board(board)

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

    print("Lancement de PN-Search avec analyse approfondie...")
    pn = PNSearch(game=game, max_nodes=50000, use_transposition_table=True)
    best_move = pn.choose_best_move(state)

    if best_move:
        print("Meilleur coup trouvé :")
        display_board(best_move.board)
    else:
        print("Aucun coup gagnant trouvé (position peut-être nulle).")

    stats = pn.get_statistics()
    print(f"Statistiques de recherche :")
    print(f"  - Nœuds explorés : {stats['nodes_explored']}")
    print(f"  - Taille table de transposition : {stats['transposition_table_size']}")
    print()


def example_3_defensive_play():
    """
    Exemple 3 : Position où X doit jouer défensivement.
    Montre comment PN-Search trouve les coups de blocage.
    """
    print("=" * 60)
    print("EXEMPLE 3 : Jeu défensif - X doit bloquer O")
    print("=" * 60)

    board = [
        ['X', ' ', ' '],
        ['O', 'O', ' '],  # O menace de gagner en (1, 2)
        [' ', ' ', ' ']
    ]

    print("Position initiale :")
    display_board(board)
    print("O menace de gagner ! X doit bloquer.")

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

    print("Lancement de PN-Search...")
    pn = PNSearch(game=game, max_nodes=20000, use_transposition_table=True)
    best_move = pn.choose_best_move(state)

    if best_move:
        print("Meilleur coup trouvé :")
        display_board(best_move.board)
    else:
        print("Aucun coup trouvé.")

    stats = pn.get_statistics()
    print(f"Statistiques de recherche :")
    print(f"  - Nœuds explorés : {stats['nodes_explored']}")
    print(f"  - Taille table de transposition : {stats['transposition_table_size']}")
    print()


def example_4_comparison_with_without_tt():
    """
    Exemple 4 : Comparaison des performances avec et sans table de transposition.
    Démontre l'importance de l'optimisation par table de transposition.
    """
    print("=" * 60)
    print("EXEMPLE 4 : Impact de la table de transposition")
    print("=" * 60)

    board = [
        ['X', ' ', ' '],
        [' ', 'O', ' '],
        [' ', ' ', ' ']
    ]

    print("Position initiale :")
    display_board(board)

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

    # AVEC table de transposition
    print("\n--- AVEC table de transposition ---")
    pn_with_tt = PNSearch(game=game, max_nodes=10000, use_transposition_table=True)
    _ = pn_with_tt.choose_best_move(state)
    stats_with = pn_with_tt.get_statistics()
    print(f"Nœuds explorés : {stats_with['nodes_explored']}")
    print(f"Taille table de transposition : {stats_with['transposition_table_size']}")

    # SANS table de transposition
    print("\n--- SANS table de transposition ---")
    pn_without_tt = PNSearch(game=game, max_nodes=10000, use_transposition_table=False)
    _ = pn_without_tt.choose_best_move(state)
    stats_without = pn_without_tt.get_statistics()
    print(f"Nœuds explorés : {stats_without['nodes_explored']}")
    print(f"Taille table de transposition : {stats_without['transposition_table_size']}")

    print("\n--- Analyse ---")
    print("La table de transposition permet de réutiliser les calculs pour")
    print("des positions identiques, réduisant ainsi le nombre de nœuds explorés.")
    print()


def main():
    """Fonction principale exécutant tous les exemples"""
    print("\n" + "=" * 60)
    print("DÉMONSTRATION DE PN-SEARCH (Proof-Number Search)")
    print("=" * 60)
    print()
    print("PN-Search est un algorithme de recherche spécialisé pour")
    print("la résolution de fins de partie. Il utilise des nombres de")
    print("preuve (phi) et de réfutation (delta) pour explorer")
    print("efficacement l'arbre de jeu.")
    print()

    # Exécution des exemples
    example_1_winning_in_one_move()
    input("Appuyez sur Entrée pour continuer vers l'exemple 2...")

    example_2_complex_endgame()
    input("Appuyez sur Entrée pour continuer vers l'exemple 3...")

    example_3_defensive_play()
    input("Appuyez sur Entrée pour continuer vers l'exemple 4...")

    example_4_comparison_with_without_tt()

    print("=" * 60)
    print("FIN DE LA DÉMONSTRATION")
    print("=" * 60)
    print()
    print("Points clés de PN-Search :")
    print("  1. Prouve mathématiquement les victoires/défaites forcées")
    print("  2. Utilise phi (preuve) et delta (réfutation)")
    print("  3. Table de transposition pour éviter recalculs")
    print("  4. Détection de cycles pour éviter boucles infinies")
    print("  5. Découplé de la logique du jeu (générique)")
    print()


if __name__ == "__main__":
    main()

