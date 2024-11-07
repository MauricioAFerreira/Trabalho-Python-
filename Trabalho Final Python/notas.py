import sqlite3
from datetime import datetime

# Função para conectar ao banco de dados e criar a tabela se não existir
def inicializar_bd():
    conexao = sqlite3.connect('alunos.db')
    cursor = conexao.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS alunos ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome TEXT NOT NULL, 
            cpf INTEGER NOT NULL, 
            data_nascimento TEXT NOT NULL 
        ) 
    ''') 
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS notas ( 
            aluno_id INTEGER, 
            nota1 REAL NOT NULL, 
            nota2 REAL NOT NULL, 
            nota3 REAL NOT NULL, 
            FOREIGN KEY(aluno_id) REFERENCES alunos(id) 
        ) 
    ''') 
    conexao.commit() 
    conexao.close()

# Função para adicionar um aluno ao banco de dados
def adicionar_aluno(nome, cpf, data_nascimento):
    conexao = sqlite3.connect('alunos.db')
    cursor = conexao.cursor()
    cursor.execute(''' 
        INSERT INTO alunos (nome, cpf, data_nascimento) 
        VALUES (?, ?, ?) 
    ''', (nome, cpf, data_nascimento)) 
    conexao.commit() 
    aluno_id = cursor.lastrowid 
    conexao.close() 
    return aluno_id

# Função para adicionar notas de um aluno
def adicionar_notas(aluno_id, nota1, nota2, nota3):
    conexao = sqlite3.connect('alunos.db')
    cursor = conexao.cursor()
    cursor.execute(''' 
        INSERT INTO notas (aluno_id, nota1, nota2, nota3) 
        VALUES (?, ?, ?, ?) 
    ''', (aluno_id, nota1, nota2, nota3)) 
    conexao.commit() 
    conexao.close()

# Função para editar notas de um aluno
def editar_notas(aluno_id, nota1, nota2, nota3):
    conexao = sqlite3.connect('alunos.db')
    cursor = conexao.cursor()
    cursor.execute(''' 
        UPDATE notas SET nota1 = ?, nota2 = ?, nota3 = ? WHERE aluno_id = ? 
    ''', (nota1, nota2, nota3, aluno_id)) 
    conexao.commit() 
    conexao.close()

# Função para calcular nota máxima, mínima, média e verificar se está na média
def calcular_notas(aluno_id):
    conexao = sqlite3.connect('alunos.db')
    cursor = conexao.cursor()
    cursor.execute(''' 
        SELECT nota1, nota2, nota3 FROM notas WHERE aluno_id = ? 
    ''', (aluno_id,)) 
    notas = cursor.fetchone() 
    conexao.close()

    if notas:
        nota_maxima = max(notas)
        nota_minima = min(notas)
        media = sum(notas) / len(notas)
        situacao = "Aprovado" if media >= 6 else "Reprovado"
        return notas, nota_maxima, nota_minima, media, situacao
    else:
        return None, None, None, None, None

# Função para pesquisar alunos por CPF ou ID
def pesquisar_alunos():
    conexao = sqlite3.connect('alunos.db')
    cursor = conexao.cursor()
    print("1. Pesquisar por CPF")
    print("2. Pesquisar por ID")
    print("3. Listar Todos os Alunos")
    escolha = input("Escolha uma opção: ")

    if escolha == '1':
        cpf = input("Digite o CPF do aluno (somente números): ")
        cursor.execute(''' 
            SELECT id, nome, cpf FROM alunos WHERE cpf = ? 
        ''', (cpf,))
    elif escolha == '2':
        aluno_id = input("Digite o ID do aluno: ")
        cursor.execute(''' 
            SELECT id, nome, cpf FROM alunos WHERE id = ? 
        ''', (aluno_id,))
    elif escolha == '3':
        cursor.execute(''' 
            SELECT id, nome, cpf FROM alunos
        ''')
    else:
        print("Opção inválida.")
        conexao.close()
        return None
    
    alunos = cursor.fetchall()
    conexao.close()
    return alunos

# Função principal para interagir com o usuário
def main():
    inicializar_bd()
    while True:
        print("\nSistema de Notas - Menu")
        print("1. Adicionar Aluno")
        print("2. Adicionar Notas")
        print("3. Calcular Notas")
        print("4. Editar Notas")
        print("5. Pesquisar Alunos")
        print("6. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome = input("Nome do aluno: ")
            cpf = input("CPF do aluno (somente números): ")
            data_nascimento = input("Data de nascimento (dd/mm/yyyy): ")

            # Validando a data de nascimento
            try:
                datetime.strptime(data_nascimento, '%d/%m/%Y')
                aluno_id = adicionar_aluno(nome, cpf, data_nascimento)
                print(f"Aluno adicionado com sucesso! ID do aluno: {aluno_id}")
            except ValueError:
                print("Data de nascimento inválida. Por favor, use o formato dd/mm/yyyy.")
        elif escolha == '2':
            aluno_id = input("ID do aluno: ")
            nota1 = float(input("Nota 1: "))
            nota2 = float(input("Nota 2: "))
            nota3 = float(input("Nota 3: "))
            adicionar_notas(aluno_id, nota1, nota2, nota3)
            print("Notas adicionadas com sucesso!")
        elif escolha == '3':
            aluno_id = input("ID do aluno: ")
            notas, nota_maxima, nota_minima, media, situacao = calcular_notas(aluno_id)
            if notas is not None:
                print(f"Notas: {notas}")
                print(f"Nota máxima: {nota_maxima}")
                print(f"Nota mínima: {nota_minima}")
                print(f"Média: {media:.2f}")
                print(f"Situação: {situacao}")
            else:
                print("Notas não encontradas para o aluno.")
        elif escolha == '4':
            aluno_id = input("ID do aluno: ")
            nota1 = float(input("Nova Nota 1: "))
            nota2 = float(input("Nova Nota 2: "))
            nota3 = float(input("Nova Nota 3: "))
            editar_notas(aluno_id, nota1, nota2, nota3)
            print("Notas editadas com sucesso!")
        elif escolha == '5':
            alunos = pesquisar_alunos()
            if alunos:
                print("\nLista de Alunos encontrados:")
                for aluno in alunos:
                    print(f"ID: {aluno[0]}, Nome: {aluno[1]}, CPF: {aluno[2]}")
            else:
                print("Nenhum aluno encontrado.")
        elif escolha == '6':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
