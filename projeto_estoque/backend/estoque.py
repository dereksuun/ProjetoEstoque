import pymysql

# Função para conectar ao banco de dados MySQL
def conectar_banco():
    return pymysql.connect(
        host='localhost',
        user='root',  # Substitua com seu usuário
        password='@fe2809Dba',  # Substitua com sua senha
        database='controle_estoque'
    )

class Estoque:
    def __init__(self):
        self.historico_movimentacao = []

    def adicionar_item(self, nome_uniforme, tamanho, quantidade):
        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("SELECT quantidade FROM uniformes WHERE tipo_uniforme=%s AND tamanho=%s", (nome_uniforme, tamanho))
        resultado = cursor.fetchone()

        if resultado:
            nova_quantidade = resultado[0] + quantidade
            cursor.execute("UPDATE uniformes SET quantidade=%s WHERE tipo_uniforme=%s AND tamanho=%s",
                           (nova_quantidade, nome_uniforme, tamanho))
        else:
            cursor.execute("INSERT INTO uniformes (tipo_uniforme, tamanho, quantidade) VALUES (%s, %s, %s)",
                           (nome_uniforme, tamanho, quantidade))

        conexao.commit()
        cursor.close()
        conexao.close()

        self.historico_movimentacao.append(f"Entrada: {quantidade} {nome_uniforme}(s) tamanho {tamanho}")
        return f"{quantidade} {nome_uniforme}(s) tamanho {tamanho} adicionados ao estoque."

    def remover_item(self, nome_uniforme, tamanho, quantidade):
        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("SELECT quantidade FROM uniformes WHERE tipo_uniforme=%s AND tamanho=%s", (nome_uniforme, tamanho))
        resultado = cursor.fetchone()

        if resultado and resultado[0] >= quantidade:
            nova_quantidade = resultado[0] - quantidade
            cursor.execute("UPDATE uniformes SET quantidade=%s WHERE tipo_uniforme=%s AND tamanho=%s",
                           (nova_quantidade, nome_uniforme, tamanho))
            conexao.commit()

            self.historico_movimentacao.append(f"Saída: {quantidade} {nome_uniforme}(s) tamanho {tamanho}")
            return f"{quantidade} {nome_uniforme}(s) tamanho {tamanho} removidos do estoque."
        else:
            return f"Erro: Quantidade insuficiente de {nome_uniforme} tamanho {tamanho}."

    def consultar_estoque(self):
        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("SELECT tipo_uniforme, tamanho, quantidade FROM uniformes")
        resultados = cursor.fetchall()

        estoque = "\n".join([f"{item[0]} tamanho {item[1]}: {item[2]} unidades" for item in resultados])

        cursor.close()
        conexao.close()

        return estoque

    def gerar_relatorio(self):
        return "\n".join(self.historico_movimentacao)
