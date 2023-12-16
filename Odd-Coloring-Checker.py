from cProfile import label
import tkinter as tk
from tkinter import ttk

class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.label = 0  # 初期値を0に設定

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        if edge not in self.edges:
            self.edges.append(edge)

class Edge:
    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node

class App:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1200x800")
        self.graph = Graph()
        self.downbox = tk.Listbox(master, width=600)
        self.downbox.pack(side=tk.BOTTOM)
        self.scrollbar = tk.Scrollbar(master, orient=tk.VERTICAL)
        self.canvas = tk.Canvas(master, width=1000, height=600, bg='white', yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.bind('<Button-1>', self.add_node)
        self.canvas.bind('<Button-3>', self.add_edge)
        self.canvas.bind('<Button-2>', self.color_mode)
        self.last_node = None
        self.clear_button = tk.Button(master, text='Clear All', command=self.clear_all, width=20, height=2)
        self.clear_button.pack()
        #self.matrix_button = tk.Button(master, text='Adjacent matrix', command=self.Adjacent_matrix, width=20, height=2)
        #self.matrix_button.pack()
        self.odd_button = tk.Button(master, text='Odd Coloring', command=self.odd_check, width=20, height=2)
        self.odd_button.pack()
        #self.proper_button = tk.Button(master, text='Proper Coloring', command=self.proper_check, width=20, height=2)
        #self.proper_button.pack()
        self.zero_button = tk.Button(master, text='Coloring', command=self.coloring, width=20, height=2)
        self.zero_button.pack()
        self.selected_number = tk.StringVar()
        available_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        self.number_menu = ttk.Combobox(self.canvas, textvariable=self.selected_number, values=available_numbers)
        self.rightbox = tk.Listbox(master, width=25)
        self.rightbox.pack(side=tk.BOTTOM)
        self.number_menu.place(x=885,y=615)
        self.history = []
        self.color_mode = False
        self.same_color = []
        
    def add_node(self, event):
        x, y = event.x, event.y
        if self.color_mode == False:
            node_name = f"Node{len(self.graph.nodes) + 1}"
            node = Node(node_name, x, y)
            self.graph.add_node(node)
            self.canvas.create_oval(x - 12, y - 12, x + 12, y + 12, fill='white')
            self.history.append(('node', node))
        else:
            node = self.get_closest_node(x, y)
            self.canvas.create_oval(node.x-5, node.y-5, node.x+5, node.y+5, fill='red', tags='highlight_start')
            self.same_color.append(node)

    def add_edge(self, event):
        x, y = event.x, event.y
        node = self.get_node_at_position(x, y)
        if node is not None:
            if self.last_node is None:
                self.last_node = node
                self.canvas.create_oval(node.x-5, node.y-5, node.x+5, node.y+5, fill='red', tags='highlight_start')
            else:
                closest_node = self.get_closest_node(x, y)
                if closest_node is not None and self.last_node != closest_node and not self.has_edge(self.last_node, closest_node):
                    self.graph.add_edge(Edge(self.last_node, closest_node))
                    self.history.append(('add_edge', self.last_node, closest_node))
                    self.canvas.create_line(self.last_node.x, self.last_node.y, closest_node.x, closest_node.y)
                    self.last_node = None
                    self.canvas.delete('highlight_start')
                else:
                    self.canvas.create_oval(node.x-5, node.y-5, node.x+5, node.y+5, fill='red', tags='highlight_start')
                    self.last_node = node
        else:
            self.last_node = None

    def color_mode(self, event):
        if  self.color_mode == True:
            self.color_mode = False
        else:
            self.color_mode = True

    def get_node_at_position(self, x, y):
        for node in self.graph.nodes:
            if node.x - 10 <= x <= node.x + 10 and node.y - 10 <= y <= node.y + 10:
                return node
        return None

    def get_closest_node(self, x, y):
        closest_node = None
        min_distance = float('inf')
        for node in self.graph.nodes:
            distance = ((x - node.x) ** 2 + (y - node.y) ** 2) ** 0.5
            if distance < min_distance:
                closest_node = node
                min_distance = distance
        return closest_node

    def has_edge(self, start_node, end_node):
        for edge in self.graph.edges:
            if (edge.start_node == start_node and edge.end_node == end_node) or \
               (edge.start_node == end_node and edge.end_node == start_node):
                return True
        return False

    def clear_all(self):
        self.canvas.delete('all')
        self.graph = Graph()
        self.history = []
        self.last_node = None

    def Adjacent_matrix(self):
        num_nodes = len(self.graph.nodes)
        matrix = [[0] * num_nodes for _ in range(num_nodes)]

        for edge in self.graph.edges:
            start_index = self.graph.nodes.index(edge.start_node)
            end_index = self.graph.nodes.index(edge.end_node)
            matrix[start_index][end_index] = 1
            matrix[end_index][start_index] = 1

        print("Original Adjacent Matrix:")
        for row in matrix:
            print(row)
        matrix = self.remove_zero_columns(matrix)
        return matrix

    def remove_zero_columns(self, matrix):
        zero_columns = [col_index for col_index, col in enumerate(zip(*matrix)) if not any(val != 0 for val in col)]
        adjusted_matrix = [[matrix[row_index][col_index] for col_index in range(len(matrix[0])) if col_index not in zero_columns] for row_index in range(len(matrix))]

        return adjusted_matrix

    def odd_check(self):
        pro_col = self.proper_check()
        if pro_col == True:
            max_label = max(node.label for node in self.graph.nodes)
            num_row= max_label + 1
            matrix = []

            for node in self.graph.nodes:
                row_vector = [0] * num_row
                index = node.label
                row_vector[index] = 1
                matrix.append(row_vector)

            odd_matrix = [list(row) for row in zip(*matrix)]

            print("Odd Coloring Matrix:")
            for row in odd_matrix:
                print(row)
            
            adj_matrix = self.Adjacent_matrix()
            product_matrix = [[sum(x * y for x, y in zip(row, col)) for col in zip(*adj_matrix)] for row in odd_matrix]

            print("Product Matrix:")
            for row in product_matrix:
                print(row)

            if any(all(element % 2 == 0 for element in col) for col in zip(*product_matrix)):
                print("Odd Coloring: False")
                self.rightbox.insert(tk.END, "Odd Coloring: False\n")
            else:
                print("Odd Coloring: True")
                self.rightbox.insert(tk.END, "Odd Coloring: True\n")
        else:
            print("Proper Coloring: False")
            self.rightbox.insert(tk.END, "Proper Coloring: False\n")

    def proper_check(self):
        for edge in self.graph.edges:
            start_label = edge.start_node.label
            end_label = edge.end_node.label

            if start_label == end_label:
                return False
        return True

    def coloring(self):
        selected_label = int(self.selected_number.get())
        color_mapping = {
            0: 'red',
            1: 'blue',
            2: 'green',
            3: 'yellow',
            4: 'orange',
            5: 'purple',
            6: 'cyan',
            7: 'pink',
            8: 'brown',
            9: 'gray',
            10: 'lightblue',
            11: 'darkgreen',
            12: 'violet',
            13: 'gold',
            14: 'magenta',
            15: 'olive',
            16: 'salmon',
            17: 'teal',
            18: 'indigo',
            19: 'tan',
            20: 'lightgray',
        }

        selected_color = color_mapping.get(selected_label, 'black')

        for node in self.same_color:
            node.label = selected_label
            self.canvas.create_text(node.x, node.y, text=str(selected_label))
            self.canvas.create_oval(node.x - 12, node.y - 12, node.x + 12, node.y + 12, fill=selected_color)

        self.canvas.delete('highlight_start')
        self.same_color = []


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()