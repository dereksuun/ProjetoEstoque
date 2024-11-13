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
    def __init__(self, host='localhost', user='root', password='@fe2809Dba', database='controle_estoque'):
        self.historico_movimentacao = []
        self.db_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.conexao = None
        self.cursor = None
        self._conectar()
        self._setup_database()

    def _conectar(self):
        self.conexao = pymysql.connect(**self.db_config)
        self.cursor = self.conexao.cursor()

    def _setup_database(self):
        # Criação das tabelas se não existirem
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS uniformes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                tipo_uniforme VARCHAR(50),
                tamanho VARCHAR(10),
                quantidade INT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS historico_movimentacao (
                id INT AUTO_INCREMENT PRIMARY KEY,
                movimentacao TEXT
            )
        """)
        self.conexao.commit()

    def _salvar_historico(self, movimentacao):
        self.cursor.execute("INSERT INTO historico_movimentacao (movimentacao) VALUES (%s)", (movimentacao,))
        self.conexao.commit()

    def adicionar_item(self, nome_uniforme, tamanho, quantidade):
        self.cursor.execute(
            "SELECT quantidade FROM uniformes WHERE tipo_uniforme=%s AND tamanho=%s",
            (nome_uniforme, tamanho)
        )
        resultado = self.cursor.fetchone()

        if resultado:
            nova_quantidade = resultado[0] + quantidade
            self.cursor.execute(
                "UPDATE uniformes SET quantidade=%s WHERE tipo_uniforme=%s AND tamanho=%s",
                (nova_quantidade, nome_uniforme, tamanho)
            )
        else:
            self.cursor.execute(
                "INSERT INTO uniformes (tipo_uniforme, tamanho, quantidade) VALUES (%s, %s, %s)",
                (nome_uniforme, tamanho, quantidade)
            )

        movimentacao = f"Entrada: {quantidade} {nome_uniforme}(s) tamanho {tamanho}"
        self.historico_movimentacao.append(movimentacao)
        self._salvar_historico(movimentacao)
        self.conexao.commit()
        return f"{quantidade} {nome_uniforme}(s) tamanho {tamanho} adicionados ao estoque."

    def remover_item(self, nome_uniforme, tamanho, quantidade):
        self.cursor.execute(
            "SELECT quantidade FROM uniformes WHERE tipo_uniforme=%s AND tamanho=%s",
            (nome_uniforme, tamanho)
        )
        resultado = self.cursor.fetchone()

        if resultado and resultado[0] >= quantidade:
            nova_quantidade = resultado[0] - quantidade
            self.cursor.execute(
                "UPDATE uniformes SET quantidade=%s WHERE tipo_uniforme=%s AND tamanho=%s",
                (nova_quantidade, nome_uniforme, tamanho)
            )

            movimentacao = f"Saída: {quantidade} {nome_uniforme}(s) tamanho {tamanho}"
            self.historico_movimentacao.append(movimentacao)
            self._salvar_historico(movimentacao)
            self.conexao.commit()
            return f"{quantidade} {nome_uniforme}(s) tamanho {tamanho} removidos do estoque."
        else:
            return f"Erro: Quantidade insuficiente de {nome_uniforme} tamanho {tamanho}."

    def consultar_estoque(self):
        self.cursor.execute("SELECT tipo_uniforme, tamanho, quantidade FROM uniformes")
        resultados = self.cursor.fetchall()
        estoque = "\n".join([f"{item[0]} tamanho {item[1]}: {item[2]} unidades" for item in resultados])
        return estoque

    def gerar_relatorio(self):
        self.cursor.execute("SELECT movimentacao FROM historico_movimentacao")
        resultados = self.cursor.fetchall()
        return "\n".join([row[0] for row in resultados])

    def fechar_conexao(self):
        self.cursor.close()
        self.conexao.close()
