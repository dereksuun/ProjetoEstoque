import tkinter as tk
from tkinter import messagebox, simpledialog
import pymongo
from pymongo import MongoClient

class Estoque:
    def __init__(self):
        self.itens = {}
        self.historico_movimentacao = []
        self.cliente_mongo = None
        self.db = None

    def conectar_mongodb(self, url="mongodb://localhost:27017/", db_name="estoque_uniformes"):
        """Conecta ao MongoDB"""
        try:
            self.cliente_mongo = MongoClient(url)
            self.db = self.cliente_mongo[db_name]
            messagebox.showinfo("Sucesso", f"Conectado ao MongoDB: {db_name}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao conectar no MongoDB: {e}")
    
    def adicionar_item(self, nome_uniforme, tamanho, quantidade):
        chave = (nome_uniforme, tamanho)
        if chave in self.itens:
            self.itens[chave] += quantidade
        else:
            self.itens[chave] = quantidade
        self.historico_movimentacao.append(f"Entrada: {quantidade} {nome_uniforme}(s) tamanho {tamanho}")
        messagebox.showinfo("Sucesso", f"{quantidade} {nome_uniforme}(s) tamanho {tamanho} adicionados ao estoque.")

    def remover_item(self, nome_uniforme, tamanho, quantidade):
        chave = (nome_uniforme, tamanho)
        if chave in self.itens and self.itens[chave] >= quantidade:
            self.itens[chave] -= quantidade
            self.historico_movimentacao.append(f"Saída: {quantidade} {nome_uniforme}(s) tamanho {tamanho}")
            messagebox.showinfo("Sucesso", f"{quantidade} {nome_uniforme}(s) tamanho {tamanho} removidos do estoque.")
        else:
            messagebox.showerror("Erro", f"Quantidade insuficiente de {nome_uniforme} tamanho {tamanho} no estoque ou item não existe.")

    def consultar_estoque(self):
        estoque_str = "\n".join([f"{item[0]} tamanho {item[1]}: {quantidade} unidades" for item, quantidade in self.itens.items()])
        if estoque_str:
            messagebox.showinfo("Estoque Atual", estoque_str)
        else:
            messagebox.showinfo("Estoque Atual", "O estoque está vazio.")

    def gerar_relatorio(self):
        relatorio_str = "\n".join(self.historico_movimentacao)
        if relatorio_str:
            messagebox.showinfo("Relatório de Movimentação", relatorio_str)
        else:
            messagebox.showinfo("Relatório de Movimentação", "Nenhuma movimentação registrada.")

    def exportar_para_mongodb(self):
        if self.db is None:
            messagebox.showerror("Erro", "Não conectado ao MongoDB.")
            return

        try:
            # Exportar o estoque atual
            colecao_estoque = self.db['estoque']
            colecao_estoque.delete_many({})  # Limpar coleção antes de atualizar
            for item, quantidade in self.itens.items():
                documento = {"nome_uniforme": item[0], "tamanho": item[1], "quantidade": quantidade}
                colecao_estoque.insert_one(documento)

            # Exportar o histórico de movimentação
            colecao_movimentacao = self.db['movimentacoes']
            colecao_movimentacao.delete_many({})  # Limpar coleção antes de atualizar
            for movimentacao in self.historico_movimentacao:
                colecao_movimentacao.insert_one({"movimentacao": movimentacao})

            messagebox.showinfo("Sucesso", "Dados exportados para o MongoDB.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar dados para o MongoDB: {e}")

class App:
    def __init__(self, root):
        self.estoque = Estoque()

        root.title("Controle de Estoque de Uniformes")
        root.geometry("400x300")

        # Botões principais
        btn_adicionar = tk.Button(root, text="Adicionar Uniforme", command=self.adicionar_item)
        btn_adicionar.pack(pady=10)

        btn_remover = tk.Button(root, text="Remover Uniforme", command=self.remover_item)
        btn_remover.pack(pady=10)

        btn_consultar = tk.Button(root, text="Consultar Estoque", command=self.estoque.consultar_estoque)
        btn_consultar.pack(pady=10)

        btn_relatorio = tk.Button(root, text="Gerar Relatório", command=self.estoque.gerar_relatorio)
        btn_relatorio.pack(pady=10)

        btn_conectar = tk.Button(root, text="Conectar MongoDB", command=self.conectar_mongo)
        btn_conectar.pack(pady=10)

        btn_exportar = tk.Button(root, text="Exportar para MongoDB", command=self.estoque.exportar_para_mongodb)
        btn_exportar.pack(pady=10)

    def adicionar_item(self):
        nome = simpledialog.askstring("Adicionar Item", "Nome do Uniforme:")
        if nome:
            tipo_item = simpledialog.askstring("Adicionar Item", "É um uniforme ou calçado? (Digite 'uniforme' ou 'calçado')")
            if tipo_item == "uniforme":
                tamanho = simpledialog.askstring("Adicionar Item", "Tamanho (P, M, G):")
            elif tipo_item == "calçado":
                tamanho = simpledialog.askinteger("Adicionar Item", "Número do Calçado:")
            else:
                messagebox.showerror("Erro", "Tipo de item inválido.")
                return

            quantidade = simpledialog.askinteger("Adicionar Item", "Quantidade:")
            if quantidade is not None:
                self.estoque.adicionar_item(nome, tamanho, quantidade)

    def remover_item(self):
        nome = simpledialog.askstring("Remover Item", "Nome do Uniforme:")
        if nome:
            tipo_item = simpledialog.askstring("Remover Item", "É um uniforme ou calçado? (Digite 'uniforme' ou 'calçado')")
            if tipo_item == "uniforme":
                tamanho = simpledialog.askstring("Remover Item", "Tamanho (P, M, G):")
            elif tipo_item == "calçado":
                tamanho = simpledialog.askinteger("Remover Item", "Número do Calçado:")
            else:
                messagebox.showerror("Erro", "Tipo de item inválido.")
                return

            quantidade = simpledialog.askinteger("Remover Item", "Quantidade:")
            if quantidade is not None:
                self.estoque.remover_item(nome, tamanho, quantidade)

    def conectar_mongo(self):
        url = simpledialog.askstring("Conectar MongoDB", "URL do MongoDB:", initialvalue="mongodb://localhost:27017/")
        db_name = simpledialog.askstring("Conectar MongoDB", "Nome do banco de dados:", initialvalue="estoque_uniformes")
        self.estoque.conectar_mongodb(url, db_name)


# Executar o programa com GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
