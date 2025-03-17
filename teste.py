import tkinter as tk
from tkinter import messagebox

# Classe para a demonstração gráfica do autômato
class AutomatoGrafico:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=500, height=250, bg="white")
        self.canvas.pack(padx=10, pady=10)
        # Coordenadas dos estados
        self.coords = {
            "ESPERANDO SELEÇÃO": (70, 100, 170, 200),
            "ACEITANDO DINHEIRO": (190, 40, 290, 140),
            "ENTREGANDO PRODUTO": (310, 100, 410, 200)
        }
        self.draw_diagram()
        
    def draw_diagram(self):
        # Desenha os estados
        self.circles = {}
        for estado, coord in self.coords.items():
            x1, y1, x2, y2 = coord
            oval = self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="black", width=2)
            self.circles[estado] = oval
            # Texto centralizado
            self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=estado, font=("Arial", 8), width=80)
        
        # Desenha as setas entre os estados
        # De ESPERANDO SELEÇÃO para ACEITANDO DINHEIRO
        self.canvas.create_line(170, 150, 190, 90, arrow=tk.LAST, width=2)
        # De ACEITANDO DINHEIRO para ENTREGANDO PRODUTO
        self.canvas.create_line(290, 90, 310, 150, arrow=tk.LAST, width=2)
        # De ENTREGANDO PRODUTO para ESPERANDO SELEÇÃO (loop de retorno)
        self.canvas.create_line(360, 200, 360, 230, 110, 230, 110, 200, arrow=tk.LAST, width=2)
    
    def update_state(self, estado_atual):
        # Atualiza o diagrama, destacando o estado atual com cor
        for estado, oval in self.circles.items():
            if estado == estado_atual:
                self.canvas.itemconfig(oval, fill="lightblue")
            else:
                self.canvas.itemconfig(oval, fill="white")


# Classe para a máquina de vendas que interage com o autômato gráfico
class MaquinaVendas:
    def __init__(self, master, automato):
        # Note que master aqui é um Frame, portanto não usamos title()
        self.master = master
        self.automato = automato
        self.frame = tk.Frame(master)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        # Catálogo de produtos: código, nome e preço
        self.produtos = {
            "A1": {"nome": "Refrigerante", "preco": 5.0},
            "A2": {"nome": "Água", "preco": 3.0},
            "B1": {"nome": "Suco", "preco": 4.5},
            "B2": {"nome": "Chá", "preco": 4.0}
        }
        self.estado = "ESPERANDO SELEÇÃO"
        self.saldo = 0.0
        self.produto_selecionado = None
        self.create_widgets()
        self.atualizar_estado(self.estado)

    def create_widgets(self):
        # Frame para exibir os produtos
        self.frame_produtos = tk.LabelFrame(self.frame, text="Produtos Disponíveis")
        self.frame_produtos.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

        for codigo, info in self.produtos.items():
            texto = f"{codigo}: {info['nome']} - R$ {info['preco']:.2f}"
            btn = tk.Button(self.frame_produtos, text=texto,
                            command=lambda c=codigo: self.selecionar_produto(c))
            btn.pack(fill=tk.X, pady=2)

        # Label que exibe o estado atual do autômato
        self.label_estado = tk.Label(self.frame, text=f"Estado: {self.estado}", font=("Arial", 12, "bold"))
        self.label_estado.pack(pady=5)

        # Frame para inserção de dinheiro
        self.frame_dinheiro = tk.Frame(self.frame)
        self.frame_dinheiro.pack(pady=10)
        tk.Label(self.frame_dinheiro, text="Insira o valor (R$):").pack(side=tk.LEFT)
        self.entry_dinheiro = tk.Entry(self.frame_dinheiro, width=10)
        self.entry_dinheiro.pack(side=tk.LEFT, padx=5)
        self.btn_inserir = tk.Button(self.frame_dinheiro, text="Inserir", command=self.inserir_dinheiro)
        self.btn_inserir.pack(side=tk.LEFT)

        # Botão para resetar a máquina
        self.btn_reset = tk.Button(self.frame, text="Resetar Máquina", command=self.reset)
        self.btn_reset.pack(pady=5)

    def atualizar_estado(self, novo_estado):
        self.estado = novo_estado
        self.label_estado.config(text=f"Estado: {self.estado}")
        # Atualiza também o diagrama do autômato gráfico
        self.automato.update_state(self.estado)

    def selecionar_produto(self, codigo):
        if self.estado != "ESPERANDO SELEÇÃO":
            messagebox.showwarning("Aviso", "A máquina já está processando um pedido!")
            return
        if codigo in self.produtos:
            self.produto_selecionado = self.produtos[codigo]
            self.atualizar_estado("ACEITANDO DINHEIRO")
            messagebox.showinfo("Produto Selecionado", 
                                f"Você selecionou {self.produto_selecionado['nome']} por R$ {self.produto_selecionado['preco']:.2f}")
        else:
            messagebox.showerror("Erro", "Código inválido.")

    def inserir_dinheiro(self):
        if self.estado != "ACEITANDO DINHEIRO":
            messagebox.showwarning("Aviso", "Selecione um produto primeiro!")
            return
        try:
            valor = float(self.entry_dinheiro.get())
        except ValueError:
            messagebox.showerror("Erro", "Insira um valor numérico válido.")
            return

        self.saldo += valor
        messagebox.showinfo("Saldo Atual", f"Saldo atual: R$ {self.saldo:.2f}")
        self.entry_dinheiro.delete(0, tk.END)

        if self.saldo >= self.produto_selecionado['preco']:
            self.atualizar_estado("ENTREGANDO PRODUTO")
            self.dispense()

    def dispense(self):
        troco = self.saldo - self.produto_selecionado['preco']
        mensagem = f"Produto {self.produto_selecionado['nome']} entregue com sucesso!"
        if troco > 0:
            mensagem += f"\nTroco: R$ {troco:.2f}"
        messagebox.showinfo("Entrega", mensagem)
        self.reset()

    def reset(self):
        # Reinicia a máquina para uma nova operação
        self.saldo = 0.0
        self.produto_selecionado = None
        self.atualizar_estado("ESPERANDO SELEÇÃO")
        self.entry_dinheiro.delete(0, tk.END)


# Função principal que cria as janelas e inicia a aplicação
def main():
    root = tk.Tk()
    root.title("Simulação: Máquina de Vendas e Autômato")
    
    # Cria um frame principal para separar as interfaces
    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    # Frame para a máquina de vendas (lado esquerdo)
    frame_vendas = tk.Frame(main_frame)
    frame_vendas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Frame para o automato gráfico (lado direito)
    frame_automato = tk.Frame(main_frame)
    frame_automato.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # Inicializa o autômato gráfico
    automato = AutomatoGrafico(frame_automato)
    # Inicializa a máquina de vendas, passando a referência do automato gráfico
    maquina = MaquinaVendas(frame_vendas, automato)
    
    root.mainloop()


if __name__ == "__main__":
    main()
