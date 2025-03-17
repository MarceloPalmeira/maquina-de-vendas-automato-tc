import tkinter as tk
from tkinter import messagebox

# Descrições dos estados do autômato (novos estados: Q0, Q1, Q2, Q3, Q4, QF)
STATE_DESCRIPTIONS = {
    "Q0": "Estado inicial: Saldo 0. Aguardando inserção de dinheiro.",
    "Q1": "Saldo R$2. Opções: comprar (Refrigerante) ou inserir mais R$2 para ir a Q4.",
    "Q2": "Saldo R$5. Opções: comprar (Batata Frita) ou inserir mais R$5 para ir a Q3.",
    "Q3": "Saldo R$10. Pode ser atingido diretamente de Q0 ou via Q2. Compre (Doce).",
    "Q4": "Saldo R$4. Compre (Água).",
    "QF": "Estado Final: Transação Concluída."
}

# Painel do autômato com estados circulares e os 5 requisitos
class AutomataDisplay:
    def __init__(self, master):
        self.master = master
        
        # Título do diagrama de estados
        tk.Label(master, text="Transições Possíveis:", font=("Helvetica", 10, "bold")).pack(pady=(5,0))
        
        # Canvas para desenhar o diagrama
        self.diagram_canvas = tk.Canvas(master, width=500, height=300, bg="white")
        self.diagram_canvas.pack(padx=5, pady=5)
        
        # Define as posições para cada estado: (centro_x, centro_y, raio)
        self.state_positions = {
            "Q0": (60, 150, 40),
            "Q1": (160, 150, 40),  # Saldo R$2
            "Q2": (160, 50, 40),   # Saldo R$5
            "Q3": (260, 50, 40),   # Saldo R$10
            "Q4": (260, 150, 40),  # Saldo R$4
            "QF": (360, 100, 40)   # Estado Final
        }
        self.state_circles = {}
        self.draw_diagram()
        
        # Painel com detalhes dos estados
        self.details_frame = tk.Frame(master)
        self.details_frame.pack(padx=5, pady=5, fill=tk.X)
        tk.Label(self.details_frame, text="Detalhes dos Estados do Autômato:", font=("Helvetica", 10, "bold")).pack(anchor="w")
        self.details_labels = {}
        for state, description in STATE_DESCRIPTIONS.items():
            lbl = tk.Label(self.details_frame, text=f"{state}: {description}", anchor="w")
            lbl.pack(fill=tk.X)
            self.details_labels[state] = lbl

        # Painel com os 5 requisitos do autômato
        self.requirements_frame = tk.Frame(master, bg="white")
        self.requirements_frame.pack(padx=5, pady=5, fill=tk.X)
        req_text = (
            "Requisitos do Autômato:\n"
            "1. Estado Inicial: Q0 (Aceitando Dinheiro).\n"
            "2. Alfabeto: {2, 4, 5, 10, 'comprar'}.\n"
            "3. Conjunto de Estados Finais: {TRANSAÇÃO CONCLUÍDA} ou estado de conclusão da compra.\n"
            "4. Função de Transição: Definida pelas transições entre Q0, Q1, Q2, Q3 e Q4.\n"
            "5. Quinto Elemento: O conjunto de Estados Finais (F)."
        )
        tk.Label(self.requirements_frame, text=req_text, justify="left", font=("Helvetica", 10)).pack(anchor="w")

    def draw_diagram(self):
        # Desenha cada estado como um círculo com o nome
        for state, (cx, cy, r) in self.state_positions.items():
            x1, y1, x2, y2 = cx - r, cy - r, cx + r, cy + r
            oval = self.diagram_canvas.create_oval(x1, y1, x2, y2, fill="white", outline="black", width=2)
            self.state_circles[state] = oval
            self.diagram_canvas.create_text(cx, cy, text=state, font=("Helvetica", 8, "bold"), width=80)
        
        # Cálculo dos pontos de saída e chegada para cada seta:
        # Q0 -> Q1
        start = (self.state_positions["Q0"][0] + 40, self.state_positions["Q0"][1])
        end   = (self.state_positions["Q1"][0] - 40, self.state_positions["Q1"][1])
        self.diagram_canvas.create_line(start[0], start[1], end[0], end[1], arrow=tk.LAST, width=2)
        
        # Q0 -> Q2
        start = (self.state_positions["Q0"][0] + 40, self.state_positions["Q0"][1])
        end   = (self.state_positions["Q2"][0] - 40, self.state_positions["Q2"][1])
        self.diagram_canvas.create_line(start[0], start[1], end[0], end[1], arrow=tk.LAST, width=2)
        
        # Q0 -> Q3
        start = (self.state_positions["Q0"][0] + 40, self.state_positions["Q0"][1])
        end   = (self.state_positions["Q3"][0] - 40, self.state_positions["Q3"][1])
        self.diagram_canvas.create_line(start[0], start[1], end[0], end[1], arrow=tk.LAST, width=2)
        
        # Q1 -> Q4 (inserir mais R$2)
        start = (self.state_positions["Q1"][0] + 40, self.state_positions["Q1"][1])
        end   = (self.state_positions["Q4"][0] - 40, self.state_positions["Q4"][1])
        self.diagram_canvas.create_line(start[0], start[1], end[0], end[1], arrow=tk.LAST, width=2)
        
        # Q2 -> Q3 (inserir mais R$5)
        start = (self.state_positions["Q2"][0] + 40, self.state_positions["Q2"][1])
        end   = (self.state_positions["Q3"][0] - 40, self.state_positions["Q3"][1])
        self.diagram_canvas.create_line(start[0], start[1], end[0], end[1], arrow=tk.LAST, width=2)
        
        # Transição de compra (estado para QF):
        # Q1 -> QF (Comprar Refrigerante)
        start = (self.state_positions["Q1"][0] + 40, self.state_positions["Q1"][1])
        end   = (self.state_positions["QF"][0] - 40, self.state_positions["QF"][1])
        self.diagram_canvas.create_line(start[0], start[1], end[0], end[1], arrow=tk.LAST, width=3)
        
        # Q2 -> QF (Comprar Batata Frita) - NOVA seta
        start = (self.state_positions["Q2"][0] + 40, self.state_positions["Q2"][1])
        end   = (self.state_positions["QF"][0] - 40, self.state_positions["QF"][1])
        self.diagram_canvas.create_line(start[0], start[1], end[0], end[1], arrow=tk.LAST, width=3)
        
        # Q3 -> QF (Comprar Doce)
        start = (self.state_positions["Q3"][0] + 40, self.state_positions["Q3"][1])
        end   = (self.state_positions["QF"][0] - 40, self.state_positions["QF"][1])
        self.diagram_canvas.create_line(start[0], start[1], end[0], end[1], arrow=tk.LAST, width=2)
        
        # Q4 -> QF (Comprar Água)
        start = (self.state_positions["Q4"][0] + 40, self.state_positions["Q4"][1])
        end   = (self.state_positions["QF"][0] - 40, self.state_positions["QF"][1])
        self.diagram_canvas.create_line(start[0], start[1], end[0], end[1], arrow=tk.LAST, width=2)
        
        # Círculo extra ao redor de QF para destacar o estado final
        cx, cy, r = self.state_positions["QF"]
        extra_margin = 5
        self.diagram_canvas.create_oval(cx - r - extra_margin, cy - r - extra_margin,
                                          cx + r + extra_margin, cy + r + extra_margin,
                                          outline="red", width=3)

    def update_state(self, current_state):
        # Atualiza o diagrama destacando o estado atual
        for state, circle in self.state_circles.items():
            color = "lightblue" if state == current_state else "white"
            self.diagram_canvas.itemconfig(circle, fill=color)
        for state, lbl in self.details_labels.items():
            if state == current_state:
                lbl.config(bg="lightyellow")
            else:
                lbl.config(bg=self.master.cget("bg"))

# Representação gráfica da máquina de vendas
class VendingMachineGraphic:
    def __init__(self, master, products):
        self.master = master
        self.products = products
        self.canvas = tk.Canvas(master, width=300, height=400, bg="#eee")
        self.canvas.pack(padx=5, pady=5)
        self.draw_machine()

    def draw_machine(self):
        self.canvas.delete("all")
        # Desenha o corpo da máquina
        self.canvas.create_rectangle(20, 20, 280, 380, fill="#ccc", outline="black", width=2)
        # Área de exibição de produtos
        self.canvas.create_rectangle(30, 30, 270, 200, fill="#fff", outline="black")
        self.canvas.create_text(150, 40, text="Produtos", font=("Helvetica", 10, "bold"))
        # Desenha os compartimentos para os produtos
        num = len(self.products)
        slot_height = 150 // num
        y = 60
        for code, info in self.products.items():
            self.canvas.create_rectangle(40, y, 260, y+slot_height-5, fill="#ddd", outline="black")
            self.canvas.create_text(150, y + slot_height//2 - 5, 
                                    text=f"{code}: {info['name']} - R$ {info['price']:.2f}", 
                                    font=("Helvetica", 9))
            y += slot_height
        # Área para inserção de dinheiro
        self.canvas.create_rectangle(30, 220, 270, 280, fill="#fafafa", outline="black")
        self.canvas.create_text(150, 240, text="Entrada de Dinheiro", font=("Helvetica", 10, "italic"))
        # Área para entrega do produto
        self.canvas.create_rectangle(30, 300, 270, 360, fill="#fafafa", outline="black")
        self.canvas.create_text(150, 330, text="Entrega do Produto", font=("Helvetica", 10, "italic"), tag="delivery")

    def highlight_slot(self, code):
        # Redesenha a máquina para manter os preços e realça o compartimento do produto correspondente
        self.draw_machine()
        num = len(self.products)
        slot_height = 150 // num
        y = 60
        for c in self.products.keys():
            if c == code:
                outline_color = "red"
                self.canvas.create_rectangle(40, y, 260, y+slot_height-5, fill="#ddd", outline=outline_color, width=3)
            y += slot_height

    def deliver_product(self, product_name):
        # Atualiza a área de "Entrega do Produto" com o nome do produto comprado
        self.canvas.delete("delivery")
        self.canvas.create_text(150, 330, text=f"Entrega: {product_name}", font=("Helvetica", 10, "italic"), tag="delivery")

# Sistema interativo da Máquina de Vendas (em português)
class AmericanVendingMachine:
    def __init__(self, master, automata_display, vending_graphic):
        self.master = master
        self.automata_display = automata_display
        self.vending_graphic = vending_graphic
        
        self.frame = tk.Frame(master, bg="#222", padx=10, pady=10)
        self.frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        # Catálogo de produtos com preços permitidos únicos (em R$)
        self.products = {
            "R": {"name": "Refrigerante", "price": 2},
            "A": {"name": "Água", "price": 4},
            "B": {"name": "Batata Frita", "price": 5},
            "D": {"name": "Doce", "price": 10}
        }
        # Estado inicial: Q0
        self.state = "Q0"
        self.balance = 0.0
        self.matching_product = None  # Produto cujo preço corresponde exatamente ao saldo
        self.create_widgets()
        self.update_state("Q0")
        
    def create_widgets(self):
        title = tk.Label(self.frame, text="Máquina de Vendas Americana", bg="#222", fg="white",
                         font=("Helvetica", 16, "bold"))
        title.pack(pady=(0,10))
        
        # Exibição do saldo atual
        self.balance_label = tk.Label(self.frame, text=f"Saldo Atual: R$ {self.balance:.2f}", bg="#222", fg="white", font=("Helvetica", 12))
        self.balance_label.pack(pady=5)
        
        # Frame para inserção de dinheiro
        self.cash_frame = tk.Frame(self.frame, bg="#222")
        self.cash_frame.pack(pady=10)
        tk.Label(self.cash_frame, text="Inserir Dinheiro (R$):", bg="#222", fg="white", font=("Helvetica", 10)).pack(side=tk.LEFT)
        self.cash_entry = tk.Entry(self.cash_frame, width=8, font=("Helvetica", 10))
        self.cash_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(self.cash_frame, text="Inserir", font=("Helvetica", 10),
                  command=self.insert_cash, bg="#eee", fg="#222").pack(side=tk.LEFT)
        
        # Frame de escolha (oculto inicialmente)
        self.choice_frame = tk.Frame(self.frame, bg="#222")
        
        # Botão para resetar a máquina
        tk.Button(self.frame, text="Resetar Máquina", font=("Helvetica", 10, "bold"),
                  command=self.reset_machine, bg="#f00", fg="white").pack(pady=5)
    
    def update_state(self, new_state):
        self.state = new_state
        self.automata_display.update_state(self.state)
    
    def insert_cash(self):
        try:
            cash = float(self.cash_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido.")
            return
        self.balance += cash
        self.cash_entry.delete(0, tk.END)
        self.balance_label.config(text=f"Saldo Atual: R$ {self.balance:.2f}")
        
        # Verifica se o saldo corresponde a um dos preços permitidos
        self.matching_product = None
        # Se estiver em Q0, as transições diretas:
        if self.state == "Q0":
            if self.balance == 2:
                self.matching_product = ("P1", self.products["R"])
                self.update_state("Q1")
            elif self.balance == 5:
                self.matching_product = ("P3", self.products["B"])
                self.update_state("Q2")
            elif self.balance == 10:
                self.matching_product = ("P4", self.products["D"])
                self.update_state("Q3")
        # Se estiver em Q1, opção de inserir mais R$2 para ir a Q4:
        if self.state == "Q1" and self.balance == 4:
            self.matching_product = ("P2", self.products["A"])
            self.update_state("Q4")
        # Se estiver em Q2, opção de inserir mais R$5 para ir a Q3:
        if self.state == "Q2" and self.balance == 10:
            self.matching_product = ("P4", self.products["D"])
            self.update_state("Q3")
        
        if self.matching_product:
            self.enter_choice_state()
    
    def enter_choice_state(self):
        for widget in self.choice_frame.winfo_children():
            widget.destroy()
        code, info = self.matching_product
        tk.Label(self.choice_frame, text=f"Seu saldo corresponde a {info['name']} (R$ {info['price']:.2f}).",
                 bg="#222", fg="white", font=("Helvetica", 10)).pack(pady=5)
        btn_frame = tk.Frame(self.choice_frame, bg="#222")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Comprar Produto", font=("Helvetica", 10),
                  command=self.purchase_product, bg="#0a0", fg="white").pack(side=tk.LEFT, padx=5)
        # Apenas em Q1 e Q2 há a opção de inserir mais dinheiro
        if self.state in ["Q1", "Q2"]:
            tk.Button(btn_frame, text="Inserir Mais Dinheiro", font=("Helvetica", 10),
                      command=self.add_more_cash, bg="#00a", fg="white").pack(side=tk.LEFT, padx=5)
        self.choice_frame.pack(pady=10)
        self.vending_graphic.highlight_slot(code)
    
    def add_more_cash(self):
        self.choice_frame.pack_forget()
        self.update_state("Q0")
    
    def purchase_product(self):
        self.choice_frame.pack_forget()
        code, info = self.matching_product
        # Atualiza o estado para QF (estado final) antes de concluir a transação
        self.update_state("QF")
        self.vending_graphic.deliver_product(info["name"])
        messagebox.showinfo("Transação", "Transação concluída!")
        self.reset_machine()
    
    def reset_machine(self):
        self.balance = 0.0
        self.matching_product = None
        self.update_state("Q0")
        self.balance_label.config(text=f"Saldo Atual: R$ {self.balance:.2f}")
        self.cash_entry.delete(0, tk.END)
        self.choice_frame.pack_forget()
        self.vending_graphic.draw_machine()

# Função principal que organiza os painéis da interface
def main():
    root = tk.Tk()
    root.title("Máquina de Vendas Americana & Demonstração do Autômato")
    
    # Frame principal com fundo escuro
    main_frame = tk.Frame(root, bg="#222")
    main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    # Painel esquerdo: Interface interativa + representação gráfica da máquina de vendas
    left_frame = tk.Frame(main_frame, bg="#222")
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Painel interativo (parte superior do painel esquerdo)
    interactive_frame = tk.Frame(left_frame, bg="#222")
    interactive_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    # Painel gráfico da máquina de vendas (parte inferior do painel esquerdo)
    vending_graphic_frame = tk.Frame(left_frame, bg="#222")
    vending_graphic_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    
    # Painel direito: Diagrama do autômato, detalhes e requisitos
    right_frame = tk.Frame(main_frame, bg="#ddd")
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    automata_display = AutomataDisplay(right_frame)
    
    # Catálogo de produtos com preços permitidos únicos
    products = {
        "R": {"name": "Refrigerante", "price": 2},
        "A": {"name": "Água", "price": 4},
        "B": {"name": "Batata Frita", "price": 5},
        "D": {"name": "Doce", "price": 10}
    }
    
    # Cria a representação gráfica da máquina de vendas
    class VendingMachineGraphicWrapper:
        def __init__(self, master, products):
            self.master = master
            self.products = products
            self.canvas = tk.Canvas(master, width=300, height=400, bg="#eee")
            self.canvas.pack(padx=5, pady=5)
            self.draw_machine()

        def draw_machine(self):
            self.canvas.delete("all")
            self.canvas.create_rectangle(20, 20, 280, 380, fill="#ccc", outline="black", width=2)
            self.canvas.create_rectangle(30, 30, 270, 200, fill="#fff", outline="black")
            self.canvas.create_text(150, 40, text="Produtos", font=("Helvetica", 10, "bold"))
            num = len(self.products)
            slot_height = 150 // num
            y = 60
            for code, info in self.products.items():
                self.canvas.create_rectangle(40, y, 260, y+slot_height-5, fill="#ddd", outline="black")
                self.canvas.create_text(150, y + slot_height//2 - 5, 
                                        text=f"{code}: {info['name']} - R$ {info['price']:.2f}", 
                                        font=("Helvetica", 9))
                y += slot_height
            self.canvas.create_rectangle(30, 220, 270, 280, fill="#fafafa", outline="black")
            self.canvas.create_text(150, 240, text="Entrada de Dinheiro", font=("Helvetica", 10, "italic"))
            self.canvas.create_rectangle(30, 300, 270, 360, fill="#fafafa", outline="black")
            self.canvas.create_text(150, 330, text="Entrega do Produto", font=("Helvetica", 10, "italic"), tag="delivery")

        def highlight_slot(self, code):
            self.draw_machine()
            num = len(self.products)
            slot_height = 150 // num
            y = 60
            for c in self.products.keys():
                if c == code:
                    outline_color = "red"
                    self.canvas.create_rectangle(40, y, 260, y+slot_height-5, fill="#ddd", outline=outline_color, width=3)
                y += slot_height

        def deliver_product(self, product_name):
            self.canvas.delete("delivery")
            self.canvas.create_text(150, 330, text=f"Entrega: {product_name}", font=("Helvetica", 10, "italic"), tag="delivery")
    
    vending_graphic = VendingMachineGraphicWrapper(vending_graphic_frame, products)
    
    AmericanVendingMachine(interactive_frame, automata_display, vending_graphic)
    
    root.mainloop()

if __name__ == "__main__":
    main()
