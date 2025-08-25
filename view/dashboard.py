from .window import Window
from controller import PlayerDataController
from controller import GameDataController

import  matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as tb
from tkinter.filedialog import askopenfile
import json

class Dashboard:
    def __init__(self, config = None):
       self.window = Window(config)
       self.style = tb.Style("darkly")
       self.clr = self.style.colors
       self.player_data = PlayerDataController()
       self.game_data = GameDataController()
       self.graphs = {}
       self.cards = {}
       self._build_gui()
    
    ## Construction functions
    def _build_gui(self):
        self.nb = tb.Notebook(self.window.window)
        self.nb.pack(fill="both", expand=True)
        self._make_menu()
        self._make_game_data_tab()
        self._make_player_data_tab()


    def _make_menu(self):
        menubar = tb.Menu(self.window.window)
        filemenu = tb.Menu(menubar, tearoff=False)
        filemenu.add_command(label="Load Game Data", command=self.on_load_game_data)
        filemenu.add_command(label="Load Play Data", command=self.on_load_player_data)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.window.window.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.window.window.config(menu=menubar)

    def _make_game_data_tab(self):
        tab = tb.Frame(self.nb)
        self.nb.add(tab, text="Game Data")
        self._make_cards(tab, self.game_data)
        self._make_figure(tab, self.game_data)
        self._draw_game_analysis()
    
    def _make_player_data_tab(self):
        tab = tb.Frame(self.nb)
        self.nb.add(tab, text="Play Data")
        self._make_cards(tab, self.player_data)
        self._make_figure(tab, self.player_data)
    
    def _make_figure(self, tab, controller):
        fr = tb.Frame(tab)
        fr.pack(fill="both", expand=True, padx=8, pady=6)
        figure = plt.Figure(figsize=(15,8), facecolor="#1e1e1e", constrained_layout=True)
        canvas = FigureCanvasTkAgg(figure, master=fr)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self.graphs[controller.get_controller_identifier()] = {
            "figure":figure,
            "canvas":canvas
        }
        
    def _make_cards(self, parent, controller_object):
        wrap = tb.Frame(parent)
        wrap.pack(fill="x", padx=8)
        for lbl in controller_object.get_model_aggregate_labels():
            card = tb.Frame(wrap, padding=6, relief="ridge", bootstyle="dark")
            card.pack(side="left", fill="x", expand=True, padx=4, pady=4)
            val = tb.Label(card, text="-", font=("Arial", 16, "bold"), foreground=self.clr.info)
            val.pack()
            tb.Label(card, text=lbl, foreground="white").pack()
            self.cards[lbl] = val

    def _update_cards(self, controller_object):
        for lbl in controller_object.get_model_aggregate_labels():
            self.cards[lbl].configure(text=controller_object.get_aggregate_data(lbl))

    ## Internal Functions
    def _load_data(self, content, dataRef):
        dataRef.load_data(json.loads(content))
        self._update_cards(dataRef)
        self._refresh_graphs()
    
    def _refresh_graphs(self):
        self._draw_game_analysis()
        self._draw_player_analysis()

    ## Graph population
    def _draw_game_analysis(self):
        if len(self.game_data.records) == 0:
            # print("Empty game data")
            return
        duration_data = self.game_data.get_column_data("duration")
        value_counts_game_modes = self.game_data.get_value_counts("game_mode")
        player_counts = self.game_data.get_value_counts("player_count")
        fig = self.graphs[self.game_data.get_controller_identifier()]['figure']
        bats_shot = self.game_data.get_bats_shot()

        graphs = fig.add_gridspec(2,2)
        ax_hist = fig.add_subplot(graphs[0,0])
        ax_bar = fig.add_subplot(graphs[0,1])
        ax_shot = fig.add_subplot(graphs[1,0])
        ax_pie = fig.add_subplot(graphs[1,1])

        # Game Duration Distribution
        ax_hist.hist(duration_data, bins=30, color=self.clr.info)
        ax_hist.set_title("Game Duration Distribution", color="w")
        ax_hist.set_xlabel("Duration (seconds)", color="w")
        ax_hist.set_ylabel("Games", color="w")
        ax_hist.tick_params(colors="w")

        # Game Mode Distribution
        ax_bar.bar(value_counts_game_modes.index, value_counts_game_modes.array, color=self.clr.info)
        ax_bar.set_title("Count of Games by Mode", color="w")
        ax_bar.set_ylabel("Games", color="w")
        ax_bar.tick_params(colors="w")

        # Distribution of bats shot
        ax_shot.bar(bats_shot.index, bats_shot.array, color=self.clr.info)
        ax_shot.set_title("Count of Bats Shot By Type", color="w")
        ax_shot.set_ylabel("Bats", color="w")
        ax_shot.tick_params(colors="w")
        
        # Player counts
        ax_pie.pie(player_counts.array, wedgeprops={"edgecolor":"w"}, labels=player_counts.index,
                   textprops={"color":"w"},autopct='%1.1f%%',
                   colors=[self.clr.primary, self.clr.secondary, self.clr.info, self.clr.dark])
        ax_pie.set_title("Distribution of players per game", color="w")

        self.graphs[self.game_data.get_controller_identifier()]['canvas'].draw()


    def _draw_player_analysis(self):
        if len(self.player_data.records) == 0:
            # print("Empty player data")
            return
        device_breakdown = self.player_data.get_column_value_count("device")
        accuracy_data = self.player_data.get_column("accuracy")
        score = self.player_data.get_column("score")
        sensitivity = self.player_data.get_sensitivity()

        fig = self.graphs[self.player_data.get_controller_identifier()]['figure']
        graphs = fig.add_gridspec(2,2)
        ax_hist = fig.add_subplot(graphs[0,0])
        ax_devices = fig.add_subplot(graphs[0,1])
        ax_accuracy = fig.add_subplot(graphs[1,0])
        ax_sensitivity = fig.add_subplot(graphs[1,1])

        ax_hist.hist(score / 1000, bins=30, color=self.clr.info)
        ax_hist.set_title("Distribution of Score", color="w")
        ax_hist.set_ylabel("Games", color="w")
        ax_hist.set_xlabel("Score (1000s)", color="w")
        ax_hist.tick_params(colors="w")

        ax_devices.pie(device_breakdown.array, labels=device_breakdown.index, autopct='%1.1f%%',
                       wedgeprops={"edgecolor":"w"}, textprops={"color":"w"},
                       colors=[self.clr.primary, self.clr.secondary, self.clr.info, self.clr.dark])
        ax_devices.set_title("Device Use Breakdown", color="w")

        ax_accuracy.scatter(accuracy_data, score / 1000, color=self.clr.info)
        ax_accuracy.set_title("Correlation between score and accuracy", color="w")
        ax_accuracy.set_xlabel("Accuracy", color="w")
        ax_accuracy.set_ylabel("Score (1000s)", color="w")
        ax_accuracy.tick_params(colors="w")
        
        ax_sensitivity.scatter(sensitivity["x"], sensitivity["y"], color=self.clr.info)
        ax_sensitivity.set_title("Sensitivity distribution by axis", color="w")
        ax_sensitivity.set_xlabel("X-Sensitivity", color="w")
        ax_sensitivity.set_ylabel("Y-Sensitivity", color="w")
        ax_sensitivity.tick_params(colors="w")

        self.graphs[self.player_data.get_controller_identifier()]['canvas'].draw()

    ## Button Load Functions
    def on_load_player_data(self):
        fl = askopenfile(filetypes=[("JSON files","*.json")])
        content = None
        if fl is not None:
            content = fl.read()
        if content is not None:
            self._load_data(content, self.player_data)
    
    def on_load_game_data(self):
        fl = askopenfile(filetypes=[("JSON files", "*.json")])
        content = None
        if fl is not None:
            content = fl.read()
        if content is not None:
            self._load_data(content, self.game_data)

    def run(self):
        self.window.window.mainloop()