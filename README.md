# Sistema de Login com wxPython

Este repositório contém duas atividades avaliativas focadas no desenvolvimento de uma interface gráfica de login utilizando a biblioteca `wxPython` em Python. A primeira versão utiliza armazenamento local em arquivo, enquanto a segunda versão (Desafio 2) evolui para uma arquitetura com banco de dados.

## 📂 Estrutura do Repositório

* **Atividade 1:** Sistema de login onde as credenciais (usuário e senha) são armazenadas e lidas a partir de um arquivo `usuarios.json`.
* **Atividade 2 (Desafio 2):** Evolução do sistema de login, substituindo o arquivo JSON por um banco de dados relacional MySQL.
* **`script.sql`:** Arquivo contendo os comandos SQL necessários para criar a estrutura do banco de dados exigida na Atividade 2.

## ⚙️ Pré-requisitos

Para rodar os códigos deste repositório, você precisará ter o Python instalado em sua máquina, além das seguintes bibliotecas:

```bash
pip install wxPython
pip install mysql-connector-python
```

Também é necessário ter um servidor MySQL rodando localmente (via XAMPP, MySQL Workbench, etc.) para testar a Atividade 2.

## 🚀 Como Executar

### Atividade 1 (Armazenamento em JSON)
1. Navegue até a pasta da atividade 1.
2. Execute o arquivo Python principal.
3. O arquivo `usuarios.json` será criado automaticamente na mesma pasta (caso não exista) com um usuário padrão (`admin` / `1234`).

### Atividade 2 (Armazenamento em MySQL)
Para testar a integração com o banco de dados, é necessário configurar o ambiente local antes de rodar o código:

1. Abra o seu gerenciador de banco de dados (como o MySQL Workbench).
2. Copie e execute os comandos do arquivo `script.sql` para criar o banco de dados e a tabela de usuários:

```sql
CREATE DATABASE sistema_banco;
USE sistema_banco;
CREATE TABLE usuarios (
    nome VARCHAR(50) PRIMARY KEY,
    senha VARCHAR(50) NOT NULL
);
INSERT INTO usuarios (nome, senha) VALUES ('admin', '1234');
```

3. Abra o arquivo Python da Atividade 2 no seu editor de código.
4. Localize o dicionário `DB_CONFIG` e altere os campos `'user'` e `'password'` para as credenciais do seu servidor MySQL local:

```python
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'SUA_SENHA_AQUI',
    'database': 'sistema_banco'
}
```

5. Salve o arquivo e execute o código Python. O login poderá ser feito com as credenciais padrão inseridas pelo script SQL (`admin` / `1234`).
