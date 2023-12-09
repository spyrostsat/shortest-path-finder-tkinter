from tkinter import messagebox
from tkinter import ttk
from tkinter import colorchooser
from copy import deepcopy
import tkinter as tk
import networkx as nx
import random


class ShortestPathFinder(object):
    
    '''
    @Author: Spyros Tsattalios
    
    This class will create a game that will allow the user to find the shortest path between two points on a map.
    The user will be able to choose the size of the map, the cost of each area and the color of each area.
    He will also be able to add obstacles to the map and choose if he wants to include areas of attraction and repulsion.
    The user chooses the start / end points and then sees the shortest path between the two points.
    
    The game will be created using the tkinter library.
    The graph will be created using the networkx library.
    The shortest path will be found using the Dijkstra and the A* algorithm.
    '''
    
    def initial_configurations(self):
        
        # All colors that we will use in the game
        self.start_point_color = "#FFFFFF"
        self.end_point_color = "#FFFFFF"
        self.path_color = "#FFFF00"
        self.obstacle_color = "#000000"
        self.road_color = "#808080"
        self.meadow_color = "#90EE90"
        self.forest_color = "#006400"
        self.hill_color = "#8B4513"
        self.mountain_color = "#FFC0CB"
        self.lake_color = "#0000FF"

        self.min_obstacles = 5  # the minimum number of obstacles that the user has to add to the map
        
        self.font = "Comic Sans MS"
        self.font_size = 20
        
        self.box_width = 1
        self.box_height = 1
        
        self.base_padding = 10
        self.base_entry_width = 10
        
        self.bg = "black"
        self.fg = "white"
        self.button_bg = "#FAD5A5"
        self.button_fg = "#006994"
        
        # Let's create the root window
        self.root = tk.Tk()
        self.root.title("Shortest Path Finder - By: @spyrostsat")
        self.root.resizable(False, False)
        
        # Let's find the width and height of the screen
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        screen_multiplier = 0.92  # we will use this variable to adjust the size of the root window
        
        # Let's adjust the size of the root window
        self.width = int(screen_multiplier * self.screen_width)  # this will be the width of the root window 
        self.height = int(screen_multiplier * self.screen_height)  # this will be the height of the root window
        width_offset = int((self.screen_width - screen_multiplier * self.screen_width) / 2)  # this will be the offset of the root window in the x axis
        height_offset = int((self.screen_height - screen_multiplier * self.screen_height) / 2)  # this will be the offset of the root window in the y axis
        
        self.root.geometry(f"{self.width}x{self.height}+{width_offset}+{height_offset}")
        
        self.root.configure(bg=self.bg)
        self.root.iconphoto(True, tk.PhotoImage(file="icon.png"))

    
    def __init__(self) -> None:
        
        self.initial_configurations()
        
        # create a label to welcome the user
        self.welcome_label = tk.Label(self.root, text="Welcome to the Shortest Path Finder!", font=(self.font, 2 * self.font_size, "bold"), bg=self.bg, fg=self.fg)
        self.welcome_label.pack(pady=40)
        
        # Let's create a frame to hold the input fields that the user will enter
        self.input_frame = tk.Frame(self.root, bg=self.bg)
        self.input_frame.pack(pady=self.base_padding)
        
        # Labels section
        
        # Let's create a label to tell the user to enter the number of rows
        self.rows_label = tk.Label(self.input_frame, text="Number of rows in the map:", font=(self.font, self.font_size), bg=self.bg, fg=self.fg)
        self.rows_label.grid(row=0, column=0, padx=self.base_padding, pady=self.base_padding)
        
        # Let's create a label to tell the user to enter the number of columns
        self.columns_label = tk.Label(self.input_frame, text="Number of columns in the map:", font=(self.font, self.font_size), bg=self.bg, fg=self.fg)
        self.columns_label.grid(row=1, column=0, padx=self.base_padding, pady=self.base_padding)
        
        # Let's create a label to tell the user to enter the road cost
        self.road_cost_label = tk.Label(self.input_frame, text="Moving cost via road:", font=(self.font, self.font_size), bg=self.bg, fg=self.fg)
        self.road_cost_label.grid(row=2, column=0, padx=self.base_padding, pady=self.base_padding)
        
        # Let's create a label to tell the user to enter the meadow cost
        self.meadow_cost_label = tk.Label(self.input_frame, text="Moving cost via meadow:", font=(self.font, self.font_size), bg=self.bg, fg=self.fg)
        self.meadow_cost_label.grid(row=3, column=0, padx=self.base_padding, pady=self.base_padding)
        
        # Let's create a label to tell the user to enter the forest cost
        self.forest_cost_label = tk.Label(self.input_frame, text="Moving cost via forest:", font=(self.font, self.font_size), bg=self.bg, fg=self.fg)
        self.forest_cost_label.grid(row=4, column=0, padx=self.base_padding, pady=self.base_padding)
        
        # Let's create a label to tell the user to enter the hill cost
        self.hill_cost_label = tk.Label(self.input_frame, text="Moving cost via hill:", font=(self.font, self.font_size), bg=self.bg, fg=self.fg)
        self.hill_cost_label.grid(row=5, column=0, padx=self.base_padding, pady=self.base_padding)
        
        # Let's create a label to tell the user to enter the mountain cost
        self.mountain_cost_label = tk.Label(self.input_frame, text="Moving cost via mountain:", font=(self.font, self.font_size), bg=self.bg, fg=self.fg)
        self.mountain_cost_label.grid(row=6, column=0, padx=self.base_padding, pady=self.base_padding)
        
        # Let's create a label to tell the user to enter the lake cost
        self.lake_cost_label = tk.Label(self.input_frame, text="Moving cost via lake:", font=(self.font, self.font_size), bg=self.bg, fg=self.fg)
        self.lake_cost_label.grid(row=7, column=0, padx=self.base_padding, pady=self.base_padding)
        
        # Let's create a label to ask the user if he wants to include areas of attraction and repulsion
        self.attraction_repulsion_label = tk.Label(self.input_frame, text="Include attraction/repulsion areas:", font=(self.font, self.font_size), bg=self.bg, fg=self.fg)
        self.attraction_repulsion_label.grid(row=8, column=0, padx=self.base_padding, pady=self.base_padding)
        
        # Entries section
        
        # Let's add an entry box to get the number of rows
        self.rows_entry = tk.Entry(self.input_frame, font=(self.font, self.font_size), width=self.base_entry_width)
        self.rows_entry.grid(row=0, column=1, padx=self.base_padding, pady=self.base_padding)
        self.rows_entry.insert(0, "15")

        # Let's add an entry box to get the number of columns
        self.columns_entry = tk.Entry(self.input_frame, font=(self.font, self.font_size), width=self.base_entry_width)
        self.columns_entry.grid(row=1, column=1, padx=self.base_padding, pady=self.base_padding)
        self.columns_entry.insert(0, "15")
        
        # Let's add an entry box to get the road cost
        self.road_cost_entry = tk.Entry(self.input_frame, font=(self.font, self.font_size), width=self.base_entry_width)
        self.road_cost_entry.grid(row=2, column=1, padx=self.base_padding, pady=self.base_padding)
        self.road_cost_entry.insert(0, "1")
        
        # Let's add an entry box to get the meadow cost
        self.meadow_cost_entry = tk.Entry(self.input_frame, font=(self.font, self.font_size), width=self.base_entry_width)
        self.meadow_cost_entry.grid(row=3, column=1, padx=self.base_padding, pady=self.base_padding)
        self.meadow_cost_entry.insert(0, "2")
        
        # Let's add an entry box to get the forest cost
        self.forest_cost_entry = tk.Entry(self.input_frame, font=(self.font, self.font_size), width=self.base_entry_width)
        self.forest_cost_entry.grid(row=4, column=1, padx=self.base_padding, pady=self.base_padding)
        self.forest_cost_entry.insert(0, "3")
        
        # Let's add an entry box to get the hill cost
        self.hill_cost_entry = tk.Entry(self.input_frame, font=(self.font, self.font_size), width=self.base_entry_width)
        self.hill_cost_entry.grid(row=5, column=1, padx=self.base_padding, pady=self.base_padding)
        self.hill_cost_entry.insert(0, "4")
        
        # Let's add an entry box to get the mountain cost
        self.mountain_cost_entry = tk.Entry(self.input_frame, font=(self.font, self.font_size), width=self.base_entry_width)
        self.mountain_cost_entry.grid(row=6, column=1, padx=self.base_padding, pady=self.base_padding)
        self.mountain_cost_entry.insert(0, "8")
        
        # Let's add an entry box to get the lake cost
        self.lake_cost_entry = tk.Entry(self.input_frame, font=(self.font, self.font_size), width=self.base_entry_width)
        self.lake_cost_entry.grid(row=7, column=1, padx=self.base_padding, pady=self.base_padding)
        self.lake_cost_entry.insert(0, "5")
        
        # Let's add a combobox to ask the user if he wants to include areas of attraction and repulsion
        self.attraction_repulsion_combobox = ttk.Combobox(self.input_frame, font=(self.font, self.font_size), width=self.base_entry_width -1)
        self.attraction_repulsion_combobox.grid(row=8, column=1, padx=self.base_padding, pady=self.base_padding)
        self.attraction_repulsion_combobox["values"] = ["Yes", "No"]
        self.attraction_repulsion_combobox.current(0)
        
        # Let's add colorchooser buttons for each area
        
        self.road_color_button = tk.Button(self.input_frame, text="Choose the road color", font=(self.font, self.font_size), bg=self.road_color, fg=self.fg, activebackground=self.road_color, activeforeground=self.fg, padx=2 * self.base_padding, command=lambda: self.choose_color("road"))
        self.road_color_button.grid(row=2, column=2, padx=4 * self.base_padding, pady=self.base_padding, sticky="we")
        
        self.meadow_color_button = tk.Button(self.input_frame, text="Choose the meadow color", font=(self.font, self.font_size), bg=self.meadow_color, fg=self.fg, activebackground=self.meadow_color, activeforeground=self.fg, padx=2 * self.base_padding, command=lambda: self.choose_color("meadow"))
        self.meadow_color_button.grid(row=3, column=2, padx=4 * self.base_padding, pady=self.base_padding, sticky="we")
        
        self.forest_color_button = tk.Button(self.input_frame, text="Choose the forest color", font=(self.font, self.font_size), bg=self.forest_color, fg=self.fg, activebackground=self.forest_color, activeforeground=self.fg, padx=2 * self.base_padding, command=lambda: self.choose_color("forest"))
        self.forest_color_button.grid(row=4, column=2, padx=4 * self.base_padding, pady=self.base_padding, sticky="we")
        
        self.hill_color_button = tk.Button(self.input_frame, text="Choose the hill color", font=(self.font, self.font_size), bg=self.hill_color, fg=self.fg, activebackground=self.hill_color, activeforeground=self.fg, padx=2 * self.base_padding, command=lambda: self.choose_color("hill"))
        self.hill_color_button.grid(row=5, column=2, padx=4 * self.base_padding, pady=self.base_padding, sticky="we")
        
        self.mountain_color_button = tk.Button(self.input_frame, text="Choose the mountain color", font=(self.font, self.font_size), bg=self.mountain_color, activebackground=self.mountain_color, activeforeground=self.fg, fg=self.fg, padx=2 * self.base_padding, command=lambda: self.choose_color("mountain"))
        self.mountain_color_button.grid(row=6, column=2, padx=4 * self.base_padding, pady=self.base_padding, sticky="we")
        
        self.lake_color_button = tk.Button(self.input_frame, text="Choose the lake color", font=(self.font, self.font_size), bg=self.lake_color, fg=self.fg, activebackground=self.lake_color, activeforeground=self.fg, padx=2 * self.base_padding, command=lambda: self.choose_color("lake"))
        self.lake_color_button.grid(row=7, column=2, padx=4 * self.base_padding, pady=self.base_padding, sticky="we")
        
        # Finally, let's create a frame to hold the buttons
        self.buttons_frame = tk.Frame(self.root, bg=self.bg)
        self.buttons_frame.pack(pady=3 * self.base_padding)
        
        # Let's create a fun looking button to start the game
        self.start_button = tk.Button(self.buttons_frame, text="Start Game", font=(self.font, self.font_size, "bold"), bg=self.button_bg, fg=self.button_fg, bd=5, relief="sunken", activebackground=self.button_bg, activeforeground=self.button_fg, command=self.submit_form)
        self.start_button.grid(row=0, column=0, padx=self.base_padding, pady=self.base_padding)
        
        # Let's create a button to exit the game
        self.exit_button = tk.Button(self.buttons_frame, text="Exit Game", font=(self.font, self.font_size, "bold"), bg=self.button_bg, fg=self.button_fg, bd=5, relief="sunken", activebackground=self.button_bg, activeforeground=self.button_fg, command=self.root.destroy)
        self.exit_button.grid(row=0, column=1, padx=self.base_padding, pady=self.base_padding)
        
        self.root.mainloop()
        
        
    def choose_color(self, area):
        # Let's open a colorchooser window
        color = colorchooser.askcolor(title=f"Choose the color that will represent the {area} areas")
        
        # Let's change the color of the button that corresponds to the area that the user chose
        if area == "road":
            self.road_color = color[1]
            self.road_color_button.configure(bg=self.road_color)
        elif area == "meadow":
            self.meadow_color = color[1]
            self.meadow_color_button.configure(bg=self.meadow_color)
        elif area == "forest":
            self.forest_color = color[1]
            self.forest_color_button.configure(bg=self.forest_color)
        elif area == "hill":
            self.hill_color = color[1]
            self.hill_color_button.configure(bg=self.hill_color)
        elif area == "mountain":
            self.mountain_color = color[1]
            self.mountain_color_button.configure(bg=self.mountain_color)
        elif area == "lake":
            self.lake_color = color[1]
            self.lake_color_button.configure(bg=self.lake_color)
        
    
    def submit_form(self):
        # Let's get the values that the user entered and store them in variables
        # We will also check if the user entered a valid value via try-except
        try:
            self.rows = int(self.rows_entry.get())
            self.columns = int(self.columns_entry.get())
            self.road_cost = int(self.road_cost_entry.get())
            self.meadow_cost = int(self.meadow_cost_entry.get())
            self.forest_cost = int(self.forest_cost_entry.get())
            self.hill_cost = int(self.hill_cost_entry.get())
            self.mountain_cost = int(self.mountain_cost_entry.get())
            self.lake_cost = int(self.lake_cost_entry.get())
            self.attraction_repulsion = self.attraction_repulsion_combobox.get()
            
            if self.rows < 1 or self.columns < 1 or self.road_cost < 1 or self.meadow_cost < 1 or self.forest_cost < 1 or self.hill_cost < 1 or self.mountain_cost < 1 or self.lake_cost < 1:
                messagebox.showerror("Error", "Please enter positive integer values!")
                return
            
            if self.attraction_repulsion == "Yes":
                self.attraction_repulsion = True
            else:
                self.attraction_repulsion = False
            
            # Let's create a list of dictionaries that will hold the cost of each area, the type of the area and the color that represents the area
            # We will use this list to choose a random area for each square on the map
            self.areas = [
                {"weight": self.road_cost, "type": "road", "color": self.road_color},
                {"weight": self.meadow_cost, "type": "meadow", "color": self.meadow_color},
                {"weight": self.forest_cost, "type": "forest", "color": self.forest_color},
                {"weight": self.hill_cost, "type": "hill", "color": self.hill_color},
                {"weight": self.mountain_cost, "type": "mountain", "color": self.mountain_color},
                {"weight": self.lake_cost, "type": "lake", "color": self.lake_color}
            ]
            
            self.start_game()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter positive integer values!")
            return

    
    def start_game(self):
        # Let's first of all destroy everything that is in the root window
        self.welcome_label.destroy()
        self.input_frame.destroy()
        self.buttons_frame.destroy()
        
        # Let's create buttons that will represent the map of the game. We will use a list of lists to store the buttons of the map
        self.map = []
        
        # Let's create a graph that will represent the map. Each node will correspond to a button on the map
        # we will use a directed graph because all edges are bidirectional BUT the cost of each edge between the same two nodes
        # is not the same e.g. (1, 2) -> (2, 2) and (2, 2) -> (1, 2) have different costs
        
        self.graph = nx.DiGraph()  
        self.old_graph = None  # we will use this variable to keep a copy of the graph before the user adds areas of attraction or repulsion
        
        # Initializations
        
        # keep track of the number of buttons clicked to check if the user has clicked on the start and end points and if he has added some obstacles
        self.clicked_buttons_count = 0
        
        self.start_point = None  # a tuple that will hold the coordinates of the start point
        self.end_point = None
        self.obstacles = []  # a list that will hold the coordinates of the obstacles
        
        if self.attraction_repulsion:
            self.obstacles_bind_still = True  # Initialization, this variable will turn to False when the user clicks to add the first area of attraction or repulsion
            self.attraction_areas = []
            self.repulsion_areas = []
            self.max_attraction_areas = 5
            self.max_repulsion_areas = 5
            self.attraction_fg_color = "cyan"
            self.repulsion_fg_color = "red"
            self.attraction_cost_mult = 0.5
            self.attraction_cost_mult_adj = 0.75
            self.repulsion_cost_mult = 2
            self.repulsion_cost_mult_adj = 1.5
            
        # Let's create a frame to hold the buttons
        self.buttons_frame = tk.Frame(self.root, bg=self.bg)
        self.buttons_frame.pack(pady=self.base_padding)
        
        for i in range(self.rows):
            
            self.map.append([])
            
            for j in range(self.columns):
            
                # Each button will have a text that will represent the cost of the specific area
                # The background color of the button will correspond to the type of the area
                
                # each button in the map will correspond to a specific area (road, meadow, forest, hill, mountain, lake) based on chance
                
                choice = random.choices(self.areas)[0]  # we will use random.choices() to choose a random area from the list of areas
                new_button = tk.Button(self.buttons_frame, text=choice["weight"], font=(self.font, self.font_size), bg=choice["color"], fg=self.fg, activebackground=choice['color'], activeforeground="white", width=self.box_width, height=self.box_height)
                
                # let's add additional attributes to each button to keep track of the row and column that the button is in
                new_button.row = i
                new_button.column = j
                
                # Let's add the the corresponding node to the graph. The node will be represented via the coordinates of the corresponding button in the map
                # We will use the coordinates of the button as the name of the node. We will also add the weight of the respective area as an extra
                # attribute to the node to know the cost of each node. Each node will be represented as a tuple (row, column)
                
                self.graph.add_node((i, j), weight=choice["weight"])
                
                # let's add the button to the map list and place it in the buttons_frame
                self.map[i].append(new_button)
                self.map[i][j].grid(row=i, column=j, padx=0.2 * self.base_padding, pady=0.2 * self.base_padding)
                self.map[i][j].bind("<Button-1>", self.change_area)  # we will bind the left mouse button to each button so that the user can set the start and end points and add obstacles

                # Let's also bind the right and middle mouse buttons to each button if the user wants to include areas of attraction and repulsion
                if self.attraction_repulsion:
                    self.map[i][j].bind("<Button-3>", self.attraction)  # we will bind the right mouse button to each button so that the user can add areas of attraction
                    self.map[i][j].bind("<Button-2>", self.repulsion)  # we will bind the middle mouse button to each button so that the user can add areas of repulsion
                
        # Let's create a frame to hold the buttons
        self.bottom_frame = tk.Frame(self.root, bg=self.bg)
        self.bottom_frame.pack(pady=self.base_padding)
        
        # Let's add a label to the right of the map to tell the user to click on the areas that he wants to change
        self.instructions_label = tk.Label(self.bottom_frame, text="Left click to set the source", font=(self.font, self.font_size), bg=self.bg, fg=self.fg)
        self.instructions_label.grid(row=0, column=0, padx=self.base_padding, pady=self.base_padding)
        
    
    def change_area(self, event):
        # Let's get the button that the user clicked
        button = event.widget
        button_row = button.row
        button_column = button.column
        
        button_coordinates = (button_row, button_column)
        
        # Let's check if the user clicked on a button that he has already clicked
        if (button_coordinates == self.start_point) or (button_coordinates == self.end_point) or (button_coordinates in self.obstacles):
            return
        
        # Let's increment the clicked_buttons_count variable
        self.clicked_buttons_count += 1
        
        if self.clicked_buttons_count == 1:  # the first button that the user clicks will be the start point
            
            # Let's change the color of the button to represent the start point
            button.configure(bg=self.start_point_color, text="S", fg="black")
            self.start_point = (button_row, button_column)
            self.instructions_label.configure(text="Left click to set the destination")
        
        elif self.clicked_buttons_count == 2:  # the second button that the user clicks will be the end point
            
            # Let's change the color of the button to represent the end point
            button.configure(bg=self.end_point_color, text="F", fg="black")
            self.end_point = (button_row, button_column)
            self.instructions_label.configure(text=f"Left click to to add some obstacles. Add at least {self.min_obstacles} obstacles.")
        
        else:  # the rest of the buttons that the user clicks will be obstacles
            button.configure(bg=self.obstacle_color, text="X")  # change the bg color of the button to represent an obstacle
            self.obstacles.append((button_row, button_column))  # add the coordinates of the obstacle to the obstacles list
            self.graph.remove_node((button_row, button_column))  # remove the respective node from the graph
            
        # After the user has added some obstacles we will allow him to start the game by clicking a button
        if len(self.obstacles) >= self.min_obstacles:
            self.instructions_label.configure(text=f"Right click to add areas of attraction or middle click to add areas of repulsion.")
            self.start_button = tk.Button(self.bottom_frame, text="Find shortest path", font=(self.font, self.font_size, "bold"), bg=self.button_bg, fg=self.button_fg, bd=5, relief="sunken", activebackground=self.button_bg, activeforeground=self.button_fg, command=self.find_shortest_path)
            self.start_button.grid(row=1, column=0, padx=self.base_padding, pady=self.base_padding)
    
    
    def update_adjacent_node(self, button_row, button_column, multiplier):
        
        if multiplier > 1:  # the user wants to add an area of repulsion
            fg_color = self.repulsion_fg_color
            letter = "R"  # R for repulsion
        else:  # the user wants to add an area of attraction
            fg_color = self.attraction_fg_color
            letter = "A"  # A for attraction
        
        if (button_row, button_column) not in self.obstacles:
            
            node = self.graph.nodes[(button_row, button_column)]
            current_weight = node['weight']
            
            new_weight = max(int(current_weight * multiplier), 1)
            
            self.graph.nodes[(button_row, button_column)]['weight'] = new_weight
            
            self.map[button_row][button_column].configure(text=f"{letter}.{new_weight}", fg=fg_color)
    
    
    def attraction(self, event):
        # Let's get the button that the user clicked
        button = event.widget
        button_row = button.row
        button_column = button.column
        button_coordinates = (button_row, button_column)
        
        # if the user hasn't added the minimum required obstacles yet, we will not allow him to add areas of attraction
        if len(self.obstacles) < self.min_obstacles:
            return

        # Let's check if the user clicked on a button that he has already clicked
        if (button_coordinates == self.start_point) or (button_coordinates == self.end_point) or (button_coordinates in self.obstacles) or (button_coordinates in self.attraction_areas) or (button_coordinates in self.repulsion_areas):
            return
        
        # Let's check if the user has already added the maximum number of attraction areas
        if len(self.attraction_areas) == self.max_attraction_areas:
            return

        # if the above conditions are passed, we will allow the user to add an area of attraction
        
        # the moment the user starts adding areas of attraction or repulsion, we will make the buttons left-unclickable to prevent the user from adding more obstacles
        if self.obstacles_bind_still:
            self.obstacles_bind_still = False
            # keep a copy the graph before the user starts adding areas of attraction or repulsion to compare the two later
            self.old_graph = deepcopy(self.graph)
            
            for row in self.map:
                for button in row:
                    button.unbind("<Button-1>")  # unbind the left mouse button from each button so that the user cannot add more obstacles
        
        # Let's add the coordinates of the area of attraction to the attraction_areas list
        self.attraction_areas.append(button_coordinates)
        
        # the button that the user clicked will be an area of attraction
        # the button itself will have a reduction of 50% in its cost and the buttons around it will have a reduction of 25% in their cost
                    
        self.update_adjacent_node(button_row, button_column, self.attraction_cost_mult)
        
        # Update the adjacent nodes of the button that the user clicked
        
        # Let's check if the node is not in the first row
        if button_row != 0:
            self.update_adjacent_node(button_row - 1, button_column, self.attraction_cost_mult_adj)
            
        # Let's check if the node is not in the last row
        if button_row != self.rows - 1:            
            self.update_adjacent_node(button_row + 1, button_column, self.attraction_cost_mult_adj)

        # Let's check if the node is not in the first column
        if button_column != 0:
            self.update_adjacent_node(button_row, button_column - 1, self.attraction_cost_mult_adj)
            
        # Let's check if the node is not in the last column
        if button_column != self.columns - 1:
            self.update_adjacent_node(button_row, button_column + 1, self.attraction_cost_mult_adj)
            
    
    def repulsion(self, event):
        # Let's get the button that the user clicked
        button = event.widget
        button_row = button.row
        button_column = button.column
        button_coordinates = (button_row, button_column)
        
        # if the user hasn't added the minimum required obstacles yet, we will not allow him to add areas of repulsion
        if len(self.obstacles) < self.min_obstacles:
            return

        # Let's check if the user clicked on a button that he has already clicked
        if (button_coordinates == self.start_point) or (button_coordinates == self.end_point) or (button_coordinates in self.obstacles) or (button_coordinates in self.attraction_areas) or (button_coordinates in self.repulsion_areas):
            return
        
        # Let's check if the user has already added the maximum number of repulsion areas
        if len(self.repulsion_areas) == self.max_repulsion_areas:
            return

        # if the above conditions are passed, we will allow the user to add an area of repulsion
        
        # the moment the user starts adding areas of attraction or repulsion, we will make the buttons left-unclickable to prevent the user from adding more obstacles
        if self.obstacles_bind_still:
            self.obstacles_bind_still = False
            # keep a copy the graph before the user starts adding areas of attraction or repulsion to compare the two later
            self.old_graph = deepcopy(self.graph)
            
            for row in self.map:
                for button in row:
                    button.unbind("<Button-1>")  # unbind the left mouse button from each button so that the user cannot add more obstacles
        
        # Let's add the coordinates of the area of repulsion to the repulsion_areas list
        self.repulsion_areas.append(button_coordinates)
        
        # the button that the user clicked will be an area of repulsion
        # the button itself will have an increase of 100% in its cost and the buttons around it will have an increase of 50% in their cost
                    
        self.update_adjacent_node(button_row, button_column, self.repulsion_cost_mult)
        
        # Update the adjacent nodes of the button that the user clicked
        
        # Let's check if the node is not in the first row
        if button_row != 0:
            self.update_adjacent_node(button_row - 1, button_column, self.repulsion_cost_mult_adj)
            
        # Let's check if the node is not in the last row
        if button_row != self.rows - 1:            
            self.update_adjacent_node(button_row + 1, button_column, self.repulsion_cost_mult_adj)

        # Let's check if the node is not in the first column
        if button_column != 0:
            self.update_adjacent_node(button_row, button_column - 1, self.repulsion_cost_mult_adj)
            
        # Let's check if the node is not in the last column
        if button_column != self.columns - 1:
            self.update_adjacent_node(button_row, button_column + 1, self.repulsion_cost_mult_adj)
            
    
    def find_shortest_path(self):
        
        # if the user hasn't added areas of attraction or repulsion and the old_graph variable is still None, we will make now a deepcopy of the graph to avoid bugs
        if self.old_graph is None:
            self.old_graph = deepcopy(self.graph)  # in this case both graphs will be the same
        
        # Let's destroy the bottom part of the root window
        self.bottom_frame.destroy()
        
        # Let's also make the buttons unclickable and remove the bindings
        for row in self.map:
            for button in row:
                button.configure(state="disabled")
                button.unbind("<Button-1>")
                button.unbind("<Button-2>")
                button.unbind("<Button-3>")
        
        # Add all edges to the graph
        # We will add an edge between two nodes if they are not obstacles and they are adjacent to each other (up, down, left, right)
        # each node will have 2, 3 or 4 edges depending on its position on the map
        
        for i in range(self.rows):
            for j in range(self.columns):
                
                if (i, j) not in self.obstacles:  # check if the node is not an obstacle
                    
                    if i != 0:  # check if the node is not in the first row
                        if (i - 1, j) not in self.obstacles:  # check if the node above it is not an obstacle
                            self.graph.add_edge((i, j), (i - 1, j), weight=self.graph.nodes[(i - 1, j)]['weight'])
                            self.graph.add_edge((i - 1, j), (i, j), weight=self.graph.nodes[(i, j)]['weight'])
                            
                            # add the edges to the old graph as well to compare the results of the A* algorithm when the user adds areas of attraction/repulsion
                            self.old_graph.add_edge((i, j), (i - 1, j), weight=self.old_graph.nodes[(i - 1, j)]['weight'])
                            self.old_graph.add_edge((i - 1, j), (i, j), weight=self.old_graph.nodes[(i, j)]['weight'])

                    if i != self.rows - 1:  # check if the node is not in the last row
                        if (i + 1, j) not in self.obstacles:  # check if the node below it is not an obstacle
                            self.graph.add_edge((i, j), (i + 1, j), weight=self.graph.nodes[(i + 1, j)]['weight'])
                            self.graph.add_edge((i + 1, j), (i, j), weight=self.graph.nodes[(i, j)]['weight'])
                            
                            self.old_graph.add_edge((i, j), (i + 1, j), weight=self.old_graph.nodes[(i + 1, j)]['weight'])
                            self.old_graph.add_edge((i + 1, j), (i, j), weight=self.old_graph.nodes[(i, j)]['weight'])  
                    
                    if j != 0:  # check if the node is not in the first column
                        if (i, j - 1) not in self.obstacles:  # check if the node on the left is not an obstacle
                            self.graph.add_edge((i, j), (i, j - 1), weight=self.graph.nodes[(i, j - 1)]['weight'])
                            self.graph.add_edge((i, j - 1), (i, j), weight=self.graph.nodes[(i, j)]['weight'])
                            
                            self.old_graph.add_edge((i, j), (i, j - 1), weight=self.old_graph.nodes[(i, j - 1)]['weight'])
                            self.old_graph.add_edge((i, j - 1), (i, j), weight=self.old_graph.nodes[(i, j)]['weight'])
                    
                    if j != self.columns - 1:  # check if the node is not in the last column
                        if (i, j + 1) not in self.obstacles:  # check if the node on the right is not an obstacle
                            self.graph.add_edge((i, j), (i, j + 1), weight=self.graph.nodes[(i, j + 1)]['weight'])
                            self.graph.add_edge((i, j + 1), (i, j), weight=self.graph.nodes[(i, j)]['weight'])
                            
                            self.old_graph.add_edge((i, j), (i, j + 1), weight=self.old_graph.nodes[(i, j + 1)]['weight'])
                            self.old_graph.add_edge((i, j + 1), (i, j), weight=self.old_graph.nodes[(i, j)]['weight'])
        
        # Let's print the graph
        print(f"Nodes of the graph: {self.graph.nodes}\n")
        
        # Let's print the edges and the cost of each node
        for node in self.graph.nodes:
            print(f"Edges of node {node}: {self.graph.edges(node)}")
            print(f"Cost of node {node}: {self.graph.nodes[node]['weight']}")
            print("=" * 150)
        
        # print the cost of each edge
        for edge in self.graph.edges:
            print(f"Cost of edge {edge}: {self.graph.edges[edge]['weight']}")
            print("=" * 150)

        # ================================================================================================================
        # Let's find the shortest path using the Dijkstra algorithm
        try:
            self.shortest_path_dijkstra = nx.shortest_path(G=self.graph, source=self.start_point, target=self.end_point, method='dijkstra', weight="weight")
            self.shortest_path_dijkstra_old = nx.shortest_path(G=self.old_graph, source=self.start_point, target=self.end_point, method='dijkstra', weight="weight")
        except nx.exception.NetworkXNoPath:
            if messagebox.askyesno("Warning", "There is no valid path between the start point and the end point!\nPlay again?"):
                self.play_again()
            else:
                self.root.destroy()
        
        shortest_path_dijkstra_string = "Validation - Shortest path (Dijkstra): "
        
        for node in self.shortest_path_dijkstra:
            shortest_path_dijkstra_string += f"{node} -> "
        # remove the last arrow
        shortest_path_dijkstra_string = shortest_path_dijkstra_string[:-3]
        
        # let's add some lines changes to the string to make it look better if the string is too long
        limit = 200
        if len(shortest_path_dijkstra_string) > limit:
            shortest_path_dijkstra_string = shortest_path_dijkstra_string[:limit] + "\n" + shortest_path_dijkstra_string[limit:]
        
        # calculate the cost of the path
        cost_dijkstra = 0
        for i in range(1, len(self.shortest_path_dijkstra) - 1):
            cost_dijkstra += self.graph.nodes[self.shortest_path_dijkstra[i]]['weight']
        
        # ================================================================================================================
        # Let's find the shortest path using the A* algorithm
        # no need to check if there is a path between the start and end points because we already checked it with the Dijkstra algorithm
        
        # A* algorithm with areas of attraction or repulsion

        self.shortest_path_a_star = nx.astar_path(G=self.graph, source=self.start_point, target=self.end_point, heuristic=self.heuristic, weight="weight")        
        
        shortest_path_a_star_string = "Shortest path (A*): "
        
        for node in self.shortest_path_a_star:
            shortest_path_a_star_string += f"{node} -> "
        # remove the last arrow
        shortest_path_a_star_string = shortest_path_a_star_string[:-3]
        
        # let's add some lines changes to the string to make it look better if the string is too long
        if len(shortest_path_a_star_string) > limit:
            shortest_path_a_star_string = shortest_path_a_star_string[:limit] + "\n" + shortest_path_a_star_string[limit:]
        
        # calculate the cost of the path
        cost_a_star = 0
        for i in range(1, len(self.shortest_path_a_star) - 1):
            cost_a_star += self.graph.nodes[self.shortest_path_a_star[i]]['weight']
        
        # ================================================================================================================
        # A* algorithm without areas of attraction or repulsion
        
        self.shortest_path_a_star_old = nx.astar_path(G=self.old_graph, source=self.start_point, target=self.end_point, heuristic=self.heuristic, weight="weight")

        old_shortest_path_a_star_string = "Shortest path (A*) without areas of attraction/repulsion: "
        
        for node in self.shortest_path_a_star_old:
            old_shortest_path_a_star_string += f"{node} -> "
        # remove the last arrow
        old_shortest_path_a_star_string = old_shortest_path_a_star_string[:-3]
        
        # let's add some lines changes to the string to make it look better if the string is too long
        if len(old_shortest_path_a_star_string) > limit:
            old_shortest_path_a_star_string = old_shortest_path_a_star_string[:limit] + "\n" + old_shortest_path_a_star_string[limit:]
        
        # calculate the cost of the path
        old_cost_a_star = 0
        for i in range(1, len(self.shortest_path_a_star_old) - 1):
            old_cost_a_star += self.old_graph.nodes[self.shortest_path_a_star_old[i]]['weight']
                
        # ================================================================================================================        
        
        # Let's color the path
        for i in range(len(self.shortest_path_a_star)):
            row_astar = self.shortest_path_a_star[i][0]
            column_astar = self.shortest_path_a_star[i][1]
            self.map[row_astar][column_astar].configure(bg=self.path_color)
        
        # Let's make sure that the start and end points have the correct text
        self.map[self.start_point[0]][self.start_point[1]].configure(text="S", fg="black")
        self.map[self.end_point[0]][self.end_point[1]].configure(text="F", fg="black")
        
        
        # Let's create a frame to hold the buttons
        self.bottom_frame = tk.Frame(self.root, bg=self.bg)
        self.bottom_frame.pack(pady=self.base_padding)
        
        # Let's create a label to tell the user the cost of the Dijkstra algorithm
        self.cost_label_dijkstra = tk.Label(self.bottom_frame, text=f"{shortest_path_dijkstra_string}. Cost: {cost_dijkstra}", font=(self.font, int(0.8 * self.font_size)), bg=self.bg, fg=self.fg)
        self.cost_label_dijkstra.grid(row=0, column=0, padx=self.base_padding, pady=self.base_padding)
        
        # Let's create a label to tell the user the cost of the A* algorithm
        self.cost_label_a_star = tk.Label(self.bottom_frame, text=f"{shortest_path_a_star_string}. Cost: {cost_a_star}", font=(self.font, int(0.8 * self.font_size)), bg=self.bg, fg=self.fg)
        self.cost_label_a_star.grid(row=1, column=0, padx=self.base_padding, pady=self.base_padding)
        
        # Let's create a label to tell the user the cost of the A* algorithm without areas of attraction or repulsion
        self.cost_label_a_star_old = tk.Label(self.bottom_frame, text=f"{old_shortest_path_a_star_string}. Cost: {old_cost_a_star}", font=(self.font, int(0.8 * self.font_size)), bg=self.bg, fg=self.fg)
        self.cost_label_a_star_old.grid(row=2, column=0, padx=self.base_padding, pady=self.base_padding)
        
        # Let's create a button to play again
        self.play_again_button = tk.Button(self.bottom_frame, text="Play Again", font=(self.font, self.font_size, "bold"), bg=self.button_bg, fg=self.button_fg, bd=5, relief="sunken", activebackground=self.button_bg, activeforeground=self.button_fg, command=self.play_again)
        self.play_again_button.grid(row=3, column=0, padx=self.base_padding, pady=self.base_padding)
        
        # Let's create a button to exit the game
        self.exit_button = tk.Button(self.bottom_frame, text="Exit Game", font=(self.font, self.font_size, "bold"), bg=self.button_bg, fg=self.button_fg, bd=5, relief="sunken", activebackground=self.button_bg, activeforeground=self.button_fg, command=self.root.destroy)
        self.exit_button.grid(row=3, column=1, padx=self.base_padding, pady=self.base_padding)


    def heuristic(self, src, target):
        '''
        This function will calculate the heuristic of the A* algorithm.
        The heuristic will be the Manhattan distance between the two nodes.
        
        @param src: the first node (the argument passes automatically by the A* algorithm)
        @param target: the second node  (the argument passes automatically by the A* algorithm)
        @return: the heuristic of the A* algorithm
        '''
        
        # The heuristic will be the Manhattan distance between the two nodes
        heuristic = abs(src[0] - target[0]) + abs(src[1] - target[1])
        
         #wrong_heuristic = abs(src[0] - target[0]) + abs(src[1] - target[1]) + random.randint(1, 20)  # just for demonstration purposes
        
        return heuristic


    def play_again(self):
        self.root.destroy()  # destroy the root window
        ShortestPathFinder()  # create a new game


if __name__ == "__main__":
    ShortestPathFinder()
