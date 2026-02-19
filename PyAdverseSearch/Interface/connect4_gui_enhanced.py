# FILE: connect4_gui_enhanced.py

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os
import time
import threading

# Ajouter le chemin parent pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyAdverseSearch.test.state_connect4 import generate_connect4_game
from PyAdverseSearch.classes.minimax import Minimax
from PyAdverseSearch.classes.alphabeta import AlphaBeta
from PyAdverseSearch.classes.montecarlo import MonteCarlo


class EnhancedAlgorithm:
    """Wrapper pour suivre les performances de l'algorithme"""
    def __init__(self, algorithm, callback=None):
        self.algorithm = algorithm
        self.callback = callback
        self.nodes_explored = 0
        self.start_time = None
        self.elapsed_time = 0
        
    def choose_best_move(self, state):
        self.nodes_explored = 0
        self.start_time = time.time()
        
        # Pour Monte Carlo, on peut suivre les itérations
        if isinstance(self.algorithm, MonteCarlo):
            return self._choose_best_move_mcts(state)
        else:
            return self._choose_best_move_standard(state)
    
    def _choose_best_move_mcts(self, state):
        """Version avec suivi pour Monte Carlo"""
        max_iterations = self.algorithm.max_iterations
        
        # On va modifier temporairement pour suivre la progression
        original_max = self.algorithm.max_iterations
        step = max(1, original_max // 100)  # Updates tous les 1%
        
        best_state = None
        for i in range(0, original_max, step):
            self.algorithm.max_iterations = min(step, original_max - i)
            if i == 0:
                best_state = self.algorithm.choose_best_move(state)
            else:
                # Continue les simulations
                best_state = self.algorithm.choose_best_move(state)
            
            self.nodes_explored = i + step
            progress = min(100, (self.nodes_explored / original_max) * 100)
            
            if self.callback:
                self.callback(progress, self.nodes_explored)
        
        self.algorithm.max_iterations = original_max
        self.elapsed_time = time.time() - self.start_time
        return best_state
    
    def _choose_best_move_standard(self, state):
        """Version standard pour Minimax/AlphaBeta"""
        # Pour ces algorithmes, on simule la progression
        # car ils n'ont pas de suivi natif
        best_state = None
        
        # Lancer dans un thread pour ne pas bloquer l'UI
        def compute():
            nonlocal best_state
            best_state = self.algorithm.choose_best_move(state)
        
        thread = threading.Thread(target=compute)
        thread.start()
        
        # Simuler la progression pendant le calcul
        while thread.is_alive():
            self.elapsed_time = time.time() - self.start_time
            # Progression estimée basée sur le temps
            estimated_time = 5.0  # Estimation en secondes
            progress = min(99, (self.elapsed_time / estimated_time) * 100)
            
            if self.callback:
                self.callback(progress, self.nodes_explored)
            
            time.sleep(0.1)
        
        thread.join()
        self.elapsed_time = time.time() - self.start_time
        
        if self.callback:
            self.callback(100, self.nodes_explored)
        
        return best_state


class Connect4GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Puissance 4 - Enhanced AI")
        self.root.resizable(False, False)
        
        # Configuration du jeu
        self.ROWS = 6
        self.COLS = 7
        self.CELL_SIZE = 80
        self.MARGIN = 10
        
        # Couleurs
        self.BOARD_COLOR = "#0066cc"
        self.EMPTY_COLOR = "#ffffff"
        self.PLAYER_COLOR = "#ff0000"  # Rouge pour le joueur humain
        self.AI_COLOR = "#ffff00"      # Jaune pour l'IA
        self.HIGHLIGHT_COLOR = "#00ff00"
        
        # Variables de jeu
        self.game = None
        self.state = None
        self.algorithm = None
        self.enhanced_algo = None
        self.human_is_max = None
        self.game_over = False
        
        # Stats IA
        self.ai_thinking = False
        self.ai_progress = 0
        self.ai_time = 0
        self.ai_nodes = 0
        self.move_history = []
        
        # Interface de configuration
        self.create_config_screen()
        
    def create_config_screen(self):
        """Écran de configuration initiale"""
        config_frame = tk.Frame(self.root, padx=20, pady=20)
        config_frame.pack()
        
        # Titre
        title = tk.Label(config_frame, text="Puissance 4", font=("Arial", 24, "bold"))
        title.pack(pady=10)
        
        subtitle = tk.Label(config_frame, text="Version Enhanced AI", 
                           font=("Arial", 10, "italic"), fg="gray")
        subtitle.pack()
        
        # Choix du joueur qui commence
        tk.Label(config_frame, text="Qui commence ?", font=("Arial", 14)).pack(pady=5)
        self.start_choice = tk.StringVar(value="human")
        tk.Radiobutton(config_frame, text="Vous (Rouge)", variable=self.start_choice, 
                      value="human", font=("Arial", 12)).pack()
        tk.Radiobutton(config_frame, text="IA (Jaune)", variable=self.start_choice, 
                      value="ai", font=("Arial", 12)).pack()
        
        # Choix de l'algorithme
        tk.Label(config_frame, text="Algorithme IA", font=("Arial", 14)).pack(pady=(20, 5))
        self.algo_choice = tk.StringVar(value="alphabeta")
        tk.Radiobutton(config_frame, text="Minimax (Plus lent)", variable=self.algo_choice, 
                      value="minimax", font=("Arial", 12)).pack()
        tk.Radiobutton(config_frame, text="Alpha-Beta (Recommandé)", variable=self.algo_choice, 
                      value="alphabeta", font=("Arial", 12)).pack()
        tk.Radiobutton(config_frame, text="Monte Carlo (Simulations)", variable=self.algo_choice, 
                      value="montecarlo", font=("Arial", 12)).pack()
        
        # Choix de la difficulté
        tk.Label(config_frame, text="Difficulté", font=("Arial", 14)).pack(pady=(20, 5))
        self.difficulty = tk.StringVar(value="medium")
        tk.Radiobutton(config_frame, text="Facile (profondeur 3)", variable=self.difficulty, 
                      value="easy", font=("Arial", 12)).pack()
        tk.Radiobutton(config_frame, text="Moyen (profondeur 5)", variable=self.difficulty, 
                      value="medium", font=("Arial", 12)).pack()
        tk.Radiobutton(config_frame, text="Difficile (profondeur 7)", variable=self.difficulty, 
                      value="hard", font=("Arial", 12)).pack()
        tk.Radiobutton(config_frame, text="Expert (profondeur 9)", variable=self.difficulty, 
                      value="expert", font=("Arial", 12)).pack()
        
        # Bouton de démarrage
        start_btn = tk.Button(config_frame, text="Commencer", command=self.start_game,
                             font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
                             padx=20, pady=10)
        start_btn.pack(pady=20)
        
    def start_game(self):
        """Initialise et démarre le jeu"""
        # Déterminer qui commence
        if self.start_choice.get() == "human":
            self.human_is_max = False
            max_starting = False
        else:
            self.human_is_max = True
            max_starting = True
        
        # Créer le jeu
        self.game = generate_connect4_game(max_starting)
        self.state = self.game.state
        
        # Déterminer la profondeur selon la difficulté
        depth_map = {"easy": 3, "medium": 5, "hard": 7, "expert": 9}
        depth = depth_map[self.difficulty.get()]
        
        # Créer l'algorithme
        algo_name = self.algo_choice.get()
        if algo_name == "minimax":
            self.algorithm = Minimax(game=self.game, max_depth=depth)
        elif algo_name == "alphabeta":
            self.algorithm = AlphaBeta(game=self.game, max_depth=depth)
        else:  # montecarlo
            iterations = 2000 * depth
            self.algorithm = MonteCarlo(game=self.game, max_iterations=iterations)
        
        # Wrapper pour suivre les performances
        self.enhanced_algo = EnhancedAlgorithm(
            self.algorithm, 
            callback=self.update_ai_progress
        )
        
        # Réinitialiser l'historique
        self.move_history = []
        
        # Détruire l'écran de configuration et créer le plateau
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.create_game_board()
        
        # Si l'IA commence, faire son coup
        current_is_max = (self.state.player == "MAX")
        if current_is_max != self.human_is_max:
            self.root.after(500, self.ai_move)
    
    def create_game_board(self):
        """Crée l'interface du plateau de jeu"""
        # Initialiser highlight_col avant tout
        self.highlight_col = None
        
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)
        
        # Frame supérieur pour infos
        top_frame = tk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=5)
        
        # Label d'information
        self.info_label = tk.Label(top_frame, text="", font=("Arial", 14, "bold"))
        self.info_label.pack(side=tk.LEFT, padx=10)
        
        # Label pour le temps IA
        self.time_label = tk.Label(top_frame, text="Temps IA: --", 
                                   font=("Arial", 11), fg="blue")
        self.time_label.pack(side=tk.RIGHT, padx=10)
        
        self.update_info_label()
        
        # Barre de progression IA
        progress_frame = tk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(progress_frame, text="Réflexion IA:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress_bar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.progress_label = tk.Label(progress_frame, text="0%", font=("Arial", 10))
        self.progress_label.pack(side=tk.LEFT, padx=5)
        
        # Stats IA
        stats_frame = tk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=5)
        
        self.stats_label = tk.Label(stats_frame, text="", font=("Arial", 9), fg="gray")
        self.stats_label.pack()
        
        # Canvas pour le plateau
        canvas_width = self.COLS * self.CELL_SIZE + 2 * self.MARGIN
        canvas_height = self.ROWS * self.CELL_SIZE + 2 * self.MARGIN
        
        self.canvas = tk.Canvas(main_frame, width=canvas_width, height=canvas_height,
                               bg=self.BOARD_COLOR)
        self.canvas.pack(pady=10)
        
        # Dessiner la grille
        self.draw_board()
        
        # Historique des coups
        history_frame = tk.Frame(main_frame)
        history_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(history_frame, text="Historique:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        self.history_text = tk.Text(history_frame, height=3, width=50, font=("Courier", 9))
        self.history_text.pack(fill=tk.X)
        self.history_text.config(state=tk.DISABLED)
        
        # Boutons en bas
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Nouvelle Partie", command=self.reset_game,
                 font=("Arial", 12), padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Quitter", command=self.root.quit,
                 font=("Arial", 12), padx=10).pack(side=tk.LEFT, padx=5)
        
        # Bind pour les clics de colonne
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)
    
    def draw_board(self):
        """Dessine le plateau de jeu"""
        self.canvas.delete("all")
        
        # Dessiner les cercles
        for row in range(self.ROWS):
            for col in range(self.COLS):
                x = self.MARGIN + col * self.CELL_SIZE
                y = self.MARGIN + row * self.CELL_SIZE
                
                # Déterminer la couleur
                cell_value = self.state.board[row][col]
                if cell_value == 'X':
                    color = self.PLAYER_COLOR if self.human_is_max else self.AI_COLOR
                elif cell_value == 'O':
                    color = self.AI_COLOR if self.human_is_max else self.PLAYER_COLOR
                else:
                    color = self.EMPTY_COLOR
                
                # Dessiner le cercle
                padding = 5
                self.canvas.create_oval(x + padding, y + padding,
                                       x + self.CELL_SIZE - padding,
                                       y + self.CELL_SIZE - padding,
                                       fill=color, outline="black", width=2)
        
        # Surligner la colonne si la souris est dessus
        if self.highlight_col is not None and not self.game_over and not self.ai_thinking:
            x = self.MARGIN + self.highlight_col * self.CELL_SIZE
            self.canvas.create_rectangle(x, 0, x + self.CELL_SIZE, 
                                        self.MARGIN + self.ROWS * self.CELL_SIZE,
                                        outline=self.HIGHLIGHT_COLOR, width=3, 
                                        stipple="gray50")
    
    def on_mouse_move(self, event):
        """Gère le survol de la souris"""
        if self.game_over or self.ai_thinking:
            return
        
        # Vérifier si c'est le tour du joueur humain
        current_is_max = (self.state.player == "MAX")
        if current_is_max != self.human_is_max:
            if self.highlight_col is not None:
                self.highlight_col = None
                self.draw_board()
            return
        
        col = (event.x - self.MARGIN) // self.CELL_SIZE
        if 0 <= col < self.COLS and col in self.state._possible_actions():
            if self.highlight_col != col:
                self.highlight_col = col
                self.draw_board()
        else:
            if self.highlight_col is not None:
                self.highlight_col = None
                self.draw_board()
    
    def on_canvas_click(self, event):
        """Gère les clics sur le canvas"""
        if self.game_over or self.ai_thinking:
            return
        
        # Déterminer si c'est le tour de l'humain
        current_is_max = (self.state.player == "MAX")
        if current_is_max != self.human_is_max:
            return
        
        # Déterminer la colonne cliquée
        col = (event.x - self.MARGIN) // self.CELL_SIZE
        
        if 0 <= col < self.COLS and col in self.state._possible_actions():
            self.make_move(col, is_human=True)
    
    def make_move(self, col, is_human=False):
        """Applique un coup"""
        # Ajouter à l'historique
        move_num = len(self.move_history) + 1
        player = "Vous" if is_human else "IA"
        self.move_history.append(f"{move_num}. {player}: Col {col + 1}")
        self.update_history()
        
        # Appliquer l'action
        self.state = self.state._apply_action(col)
        self.draw_board()
        self.update_info_label()
        
        # Vérifier fin de partie
        if self.check_game_over():
            return
        
        # Tour de l'IA - vérifier que c'est bien son tour maintenant
        current_is_max = (self.state.player == "MAX")
        if current_is_max != self.human_is_max:
            self.root.after(500, self.ai_move)
    
    def update_history(self):
        """Met à jour l'affichage de l'historique"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        # Afficher les 10 derniers coups
        recent_moves = self.move_history[-10:]
        self.history_text.insert(1.0, " | ".join(recent_moves))
        
        self.history_text.config(state=tk.DISABLED)
    
    def ai_move(self):
        """Fait jouer l'IA"""
        if self.game_over:
            return
        
        self.ai_thinking = True
        self.info_label.config(text="L'IA réfléchit...", fg="orange")
        self.progress_bar['value'] = 0
        self.progress_label.config(text="0%")
        self.root.update()
        
        # Lancer le calcul dans un thread
        def compute_move():
            start = time.time()
            best_state = self.enhanced_algo.choose_best_move(self.state)
            elapsed = time.time() - start
            
            # Trouver la colonne jouée
            col = None
            for c in range(self.COLS):
                test_state = self.state._apply_action(c)
                if test_state.board == best_state.board:
                    col = c
                    break
            
            # Mettre à jour l'UI dans le thread principal
            self.root.after(0, lambda: self.finish_ai_move(best_state, col, elapsed))
        
        thread = threading.Thread(target=compute_move)
        thread.daemon = True
        thread.start()
    
    def update_ai_progress(self, progress, nodes):
        """Callback pour mettre à jour la progression de l'IA"""
        self.progress_bar['value'] = progress
        self.progress_label.config(text=f"{int(progress)}%")
        
        algo_name = self.algo_choice.get()
        if algo_name == "montecarlo":
            self.stats_label.config(text=f"Simulations: {nodes}/{self.algorithm.max_iterations}")
        else:
            self.stats_label.config(text=f"Exploration en cours... ({progress:.1f}%)")
        
        self.root.update()
    
    def finish_ai_move(self, best_state, col, elapsed):
        """Termine le coup de l'IA"""
        if best_state is None:
            messagebox.showerror("Erreur", "L'IA n'a pas trouvé de coup valide")
            self.ai_thinking = False
            return
        
        # Mettre à jour les stats
        self.time_label.config(text=f"Temps IA: {elapsed:.2f}s")
        self.progress_bar['value'] = 100
        self.progress_label.config(text="100%")
        
        algo_name = self.algo_choice.get()
        if algo_name == "montecarlo":
            self.stats_label.config(
                text=f"✓ {self.algorithm.max_iterations} simulations en {elapsed:.2f}s "
                     f"({int(self.algorithm.max_iterations/elapsed)}/s)"
            )
        else:
            self.stats_label.config(
                text=f"✓ Calcul terminé en {elapsed:.2f}s (profondeur {self.algorithm.max_depth})"
            )
        
        # Appliquer le coup
        self.make_move(col, is_human=False)
        
        self.ai_thinking = False
        self.draw_board()
        self.update_info_label()
        
        # Vérifier fin de partie
        self.check_game_over()
    
    def update_info_label(self):
        """Met à jour le label d'information"""
        if self.game_over:
            return
        
        if self.ai_thinking:
            self.info_label.config(text="L'IA réfléchit...", fg="orange")
            return
        
        current_is_max = (self.state.player == "MAX")
        if current_is_max != self.human_is_max:
            self.info_label.config(text="Tour de l'IA...", fg="orange")
        else:
            self.info_label.config(text="Votre tour (cliquez sur une colonne)", fg="green")
    
    def check_game_over(self):
        """Vérifie si le jeu est terminé"""
        if self.state._is_terminal():
            self.game_over = True
            winner = self.game.winner_function(self.state)
            
            if winner is None:
                message = "Match nul !"
                self.info_label.config(text=message, fg="blue")
            elif (winner == "MAX") == self.human_is_max:
                message = "Vous avez gagné ! Félicitations !"
                self.info_label.config(text=message, fg="green")
            else:
                message = "L'IA a gagné !"
                self.info_label.config(text=message, fg="red")
            
            messagebox.showinfo("Fin de partie", message)
            return True
        
        return False
    
    def reset_game(self):
        """Réinitialise le jeu"""
        self.game_over = False
        self.ai_thinking = False
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_config_screen()


def main():
    root = tk.Tk()
    app = Connect4GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
