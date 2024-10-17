import tkinter as tk
from tkinter import simpledialog, messagebox
from backend.estoque import Estoque

class App:
    def __init__(self, root):
        self.estoque = Estoque()

        root.title("Controle de Estoque de Uniformes")
        root.geometry("500x400")
        root.configure(bg='#f0f0f0')

        self.label_title = tk.Label(root, text="Sistema de Controle de Estoque", font=("Arial", 16, "bold"), bg='#f0f0f0')
        self.label_title.pack(pady=10)

        self.frame_acoes = tk.Frame(root, bg='#f0f0f0')
        self.frame_acoes.pack(pady=10)

        tk.Button(self.frame_acoes, text="Adicionar Uniforme", command=self.escolher_uniforme_adicionar, width=20, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame_acoes, text="Remover Uniforme", command=self.escolher_uniforme_remover, width=20, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        self.label_estoque = tk.Label(root, text="Estoque Atual:", font=("Arial", 12, "bold"), bg='#f0f0f0')
        self.label_estoque.pack(pady=10)

        self.text_estoque = tk.Text(root, height=10, width=50, state=tk.DISABLED)
        self.text_estoque.pack(pady=10)

        tk.Button(root, text="Ver Relatório de Movimentação", command=self.mostrar_relatorio, font=("Arial", 10)).pack(pady=10)

        self.mostrar_estoque()

    def escolher_uniforme_adicionar(self):
        # Aqui vai a lógica de adicionar uniforme
        pass

    def escolher_uniforme_remover(self):
        # Aqui vai a lógica de remover uniforme
        pass

    def mostrar_estoque(self):
        estoque_str = self.estoque.consultar_estoque()
        self.text_estoque.config(state=tk.NORMAL)
        self.text_estoque.delete(1.0, tk.END)
        self.text_estoque.insert(tk.END, estoque_str)
        self.text_estoque.config(state=tk.DISABLED)

    def mostrar_relatorio(self):
        relatorio_str = self.estoque.gerar_relatorio()
        if relatorio_str:
            messagebox.showinfo("Relatório de Movimentação", relatorio_str)
        else:
            messagebox.showinfo("Relatório de Movimentação", "Nenhuma movimentação registrada.")
