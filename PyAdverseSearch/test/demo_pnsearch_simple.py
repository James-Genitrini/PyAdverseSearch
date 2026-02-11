# FILE: PyAdverseSearch/test/demo_pnsearch_simple.py

"""
Démonstration simple de PN-Search sans interaction utilisateur.
"""

import sys
sys.path.insert(0, '.')

from PyAdverseSearch.classes.pnsearch import PNSearch
from PyAdverseSearch.classes.game import Game
from PyAdverseSearch.test.state_tictactoe import TicTacToeState


def display_board(board):
    """Affiche le plateau de jeu"""
    print("\n" + "=" * 13)
    for i, row in enumerate(board):
        print(f" {row[0]} | {row[1]} | {row[2]} ")
        if i < len(board) - 1:
            print("---+---+---")
    print("=" * 13 + "\n")


def demo_winning_position():
    """Démonstration : position gagnante en un coup"""
    print("=" * 60)
    print("DÉMONSTRATION PN-SEARCH : Position gagnante")
    print("=" * 60)

    board = [
        ['X', 'X', ' '],
        ['O', 'O', ' '],
        [' ', ' ', ' ']
    ]

    print("\nPosition initiale (X peut gagner) :")
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

    print("Lancement de PN-Search...")
    pn = PNSearch(game=game, max_nodes=50000, use_transposition_table=True)
    best_move = pn.choose_best_move(state)

    if best_move:
        print("\nMeilleur coup trouvé par PN-Search :")
        display_board(best_move.board)

    stats = pn.get_statistics()
    print(f"Statistiques :")
    print(f"  ✓ Nœuds explorés : {stats['nodes_explored']}")
    print(f"  ✓ Table de transposition : {stats['transposition_table_size']} entrées")
    print()


def demo_comparison():
    """Comparaison avec/sans table de transposition"""
    print("=" * 60)
    print("COMPARAISON : Impact de la table de transposition")
    print("=" * 60)

    board = [
        ['X', ' ', ' '],
        [' ', 'O', ' '],
        [' ', ' ', ' ']
    ]

    print("\nPosition de test :")
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

    # Avec table de transposition
    print("Avec table de transposition :")
    pn_with = PNSearch(game=game, max_nodes=20000, use_transposition_table=True)
    _ = pn_with.choose_best_move(state)
    stats_with = pn_with.get_statistics()
    print(f"  → Nœuds explorés : {stats_with['nodes_explored']}")
    print(f"  → Entrées TT : {stats_with['transposition_table_size']}")

    # Sans table de transposition
    print("\nSans table de transposition :")
    pn_without = PNSearch(game=game, max_nodes=20000, use_transposition_table=False)
    _ = pn_without.choose_best_move(state)
    stats_without = pn_without.get_statistics()
    print(f"  → Nœuds explorés : {stats_without['nodes_explored']}")
    print(f"  → Entrées TT : {stats_without['transposition_table_size']}")

    print("\n✓ La table de transposition réduit le travail de recherche!")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" DÉMONSTRATION DE L'ALGORITHME PN-SEARCH")
    print("=" * 60)
    print()
    print("PN-Search (Proof-Number Search) est un algorithme qui prouve")
    print("mathématiquement si une position est gagnante ou perdante.")
    print()

    demo_winning_position()
    demo_comparison()

    print("=" * 60)
    print(" FIN DE LA DÉMONSTRATION")
    print("=" * 60)
    print()
    print("Points clés :")
    print("  • Prouve mathématiquement les victoires/défaites")
    print("  • Utilise phi (preuve) et delta (réfutation)")
    print("  • Table de transposition pour optimisation")
    print("  • Détection de cycles pour éviter les boucles")
    print("  • Découplé de la logique du jeu (générique)")
    print()

