import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class Estoque:
    def __init__(self):
        self.itens = {}
        self.historico_movimentacao = []

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
        return "\n".join([f"{item[0]} tamanho {item[1]}: {quantidade} unidades" for item, quantidade in self.itens.items()])

    def gerar_relatorio(self):
        return "\n".join(self.historico_movimentacao)

class App:
    def __init__(self, root):
        self.estoque = Estoque()

        root.title("Controle de Estoque de Uniformes")
        root.geometry("500x400")
        root.configure(bg='#f0f0f0')

        # Título
        self.label_title = tk.Label(root, text="Sistema de Controle de Estoque", font=("Arial", 16, "bold"), bg='#f0f0f0')
        self.label_title.pack(pady=10)

        # Seção para adicionar/remover uniformes
        self.frame_acoes = tk.Frame(root, bg='#f0f0f0')
        self.frame_acoes.pack(pady=10)

        tk.Button(self.frame_acoes, text="Adicionar Uniforme", command=self.escolher_uniforme_adicionar, width=20, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame_acoes, text="Remover Uniforme", command=self.escolher_uniforme_remover, width=20, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        # Exibir o estoque
        self.label_estoque = tk.Label(root, text="Estoque Atual:", font=("Arial", 12, "bold"), bg='#f0f0f0')
        self.label_estoque.pack(pady=10)

        self.text_estoque = tk.Text(root, height=10, width=50, state=tk.DISABLED)
        self.text_estoque.pack(pady=10)

        # Botão para atualizar estoque removido, pois agora será automático

        # Exibir histórico de movimentação
        tk.Button(root, text="Ver Relatório de Movimentação", command=self.mostrar_relatorio, font=("Arial", 10)).pack(pady=10)

        # Atualiza o estoque ao iniciar
        self.mostrar_estoque()

    # Lógica para Adicionar Uniforme
    def escolher_uniforme_adicionar(self):
        self.janela_uniforme = tk.Toplevel()
        self.janela_uniforme.title("Escolher Uniforme")

        tk.Label(self.janela_uniforme, text="Selecione o Uniforme:", font=("Arial", 12)).pack(pady=10)

        tk.Button(self.janela_uniforme, text="Camisa", width=20, command=lambda: self.escolher_tamanho_adicionar("Camisa")).pack(pady=5)
        tk.Button(self.janela_uniforme, text="Calça", width=20, command=lambda: self.escolher_tamanho_adicionar("Calça")).pack(pady=5)
        tk.Button(self.janela_uniforme, text="Calçado", width=20, command=lambda: self.escolher_numero_adicionar("Calçado")).pack(pady=5)
        tk.Button(self.janela_uniforme, text="Paletó", width=20, command=lambda: self.escolher_tamanho_adicionar("Paletó")).pack(pady=5)

    def escolher_tamanho_adicionar(self, tipo_uniforme):
        self.janela_uniforme.destroy()  # Fechar a janela anterior
        self.janela_tamanho = tk.Toplevel()
        self.janela_tamanho.title("Escolher Tamanho")

        tk.Label(self.janela_tamanho, text=f"Selecione o Tamanho para {tipo_uniforme}:", font=("Arial", 12)).pack(pady=10)

        tamanhos = ["P", "M", "G", "GG"]
        for tamanho in tamanhos:
            tk.Button(self.janela_tamanho, text=tamanho, width=20, command=lambda t=tamanho: self.digitar_quantidade_adicionar(tipo_uniforme, t)).pack(pady=5)

    def escolher_numero_adicionar(self, tipo_uniforme):
        self.janela_uniforme.destroy()  # Fechar a janela anterior
        self.janela_numero = tk.Toplevel()
        self.janela_numero.title("Escolher Número de Calçado")

        tk.Label(self.janela_numero, text=f"Selecione o Número para {tipo_uniforme}:", font=("Arial", 12)).pack(pady=10)

        numeros = list(range(35, 43))  # Números de 35 a 42
        for numero in numeros:
            tk.Button(self.janela_numero, text=str(numero), width=20, command=lambda n=numero: self.digitar_quantidade_adicionar(tipo_uniforme, n)).pack(pady=5)

    def digitar_quantidade_adicionar(self, tipo_uniforme, tamanho_ou_numero):
        if hasattr(self, 'janela_tamanho'):
            self.janela_tamanho.destroy()  # Fechar a janela de tamanho, se estiver aberta
        if hasattr(self, 'janela_numero'):
            self.janela_numero.destroy()  # Fechar a janela de número, se estiver aberta

        quantidade = simpledialog.askinteger("Quantidade", f"Digite a quantidade para {tipo_uniforme} tamanho {tamanho_ou_numero}:")
        if quantidade is not None:
            self.estoque.adicionar_item(tipo_uniforme, tamanho_ou_numero, quantidade)
            self.mostrar_estoque()  # Atualiza o estoque após adicionar

    # Lógica para Remover Uniforme
    def escolher_uniforme_remover(self):
        self.janela_uniforme = tk.Toplevel()
        self.janela_uniforme.title("Escolher Uniforme")

        tk.Label(self.janela_uniforme, text="Selecione o Uniforme:", font=("Arial", 12)).pack(pady=10)

        tk.Button(self.janela_uniforme, text="Camisa", width=20, command=lambda: self.escolher_tamanho_remover("Camisa")).pack(pady=5)
        tk.Button(self.janela_uniforme, text="Calça", width=20, command=lambda: self.escolher_tamanho_remover("Calça")).pack(pady=5)
        tk.Button(self.janela_uniforme, text="Calçado", width=20, command=lambda: self.escolher_numero_remover("Calçado")).pack(pady=5)
        tk.Button(self.janela_uniforme, text="Paletó", width=20, command=lambda: self.escolher_tamanho_remover("Paletó")).pack(pady=5)

    def escolher_tamanho_remover(self, tipo_uniforme):
        self.janela_uniforme.destroy()  # Fechar a janela anterior
        self.janela_tamanho = tk.Toplevel()
        self.janela_tamanho.title("Escolher Tamanho")

        tk.Label(self.janela_tamanho, text=f"Selecione o Tamanho para {tipo_uniforme}:", font=("Arial", 12)).pack(pady=10)

        tamanhos = ["P", "M", "G", "GG"]
        for tamanho in tamanhos:
            tk.Button(self.janela_tamanho, text=tamanho, width=20, command=lambda t=tamanho: self.digitar_quantidade_remover(tipo_uniforme, t)).pack(pady=5)

    def escolher_numero_remover(self, tipo_uniforme):
        self.janela_uniforme.destroy()  # Fechar a janela anterior
        self.janela_numero = tk.Toplevel()
        self.janela_numero.title("Escolher Número de Calçado")

        tk.Label(self.janela_numero, text=f"Selecione o Número para {tipo_uniforme}:", font=("Arial", 12)).pack(pady=10)

        numeros = list(range(35, 43))  # Números de 35 a 42
        for numero in numeros:
            tk.Button(self.janela_numero, text=str(numero), width=20, command=lambda n=numero: self.digitar_quantidade_remover(tipo_uniforme, n)).pack(pady=5)

    def digitar_quantidade_remover(self, tipo_uniforme, tamanho_ou_numero):
        if hasattr(self, 'janela_tamanho'):
            self.janela_tamanho.destroy()  # Fechar a janela de tamanho, se estiver aberta
        if hasattr(self, 'janela_numero'):
            self.janela_numero.destroy()  # Fechar a janela de número, se estiver aberta

        quantidade = simpledialog.askinteger("Quantidade", f"Digite a quantidade para remover de {tipo_uniforme} tamanho {tamanho_ou_numero}:")
        if quantidade is not None:
            self.estoque.remover_item(tipo_uniforme, tamanho_ou_numero, quantidade)
            self.mostrar_estoque()  # Atualiza o estoque após remover

    def mostrar_estoque(self):
        estoque_str = self.estoque.consultar_estoque()
        self.text_estoque.config(state=tk.NORMAL)
        self.text_estoque.delete(1.0, tk.END)  # Limpa o campo de texto
        self.text_estoque.insert(tk.END, estoque_str)
        self.text_estoque.config(state=tk.DISABLED)  # Desabilita edição no campo de texto

    def mostrar_relatorio(self):
        relatorio_str = self.estoque.gerar_relatorio()
        if relatorio_str:
            messagebox.showinfo("Relatório de Movimentação", relatorio_str)
        else:
            messagebox.showinfo("Relatório de Movimentação", "Nenhuma movimentação registrada.")

# Executar o programa com GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
