# Sistema de Login e Cadastro com wxPython

Este repositório contém três atividades avaliativas focadas no desenvolvimento de interfaces gráficas utilizando a biblioteca `wxPython` em Python. O projeto evolui de um sistema de login simples com armazenamento local para uma aplicação conectada a um banco de dados relacional com funcionalidades de cadastro.

## 📂 Estrutura do Repositório

* **Atividade 1:** Sistema de login onde as credenciais (usuário e senha) são armazenadas e lidas a partir de um arquivo `usuarios.json`.
* **Atividade 2 (Desafio 2):** Evolução do sistema de login, substituindo o arquivo JSON por um banco de dados MySQL (`sistema_banco`).
* **Atividade 3 (Cadastro de PET):** Expansão do sistema. Após o login, o usuário acessa um painel para cadastrar e visualizar os seus próprios pets. Utiliza um banco de dados dedicado (`sistema_pet`).

## ⚙️ Pré-requisitos

Para rodar os códigos deste repositório, você precisará ter o Python instalado em sua máquina, além das seguintes bibliotecas:

```bash
pip install wxPython
pip install mysql-connector-python
```

Também é necessário ter um servidor MySQL rodando localmente (via XAMPP, MySQL Workbench, etc.) para testar as Atividades 2 e 3.

## 🚀 Como Executar

### Atividade 1 (Armazenamento em JSON)
1. Navegue até a pasta da atividade 1.
2. Execute o arquivo Python principal.
3. O arquivo `usuarios.json` será criado automaticamente na mesma pasta (caso não exista) com um usuário padrão (`admin` / `1234`).

### Atividade 2 (Armazenamento em MySQL)
Para testar a integração com o banco de dados:

1. Abra o seu gerenciador de banco de dados (como o MySQL Workbench).
2. Execute os comandos SQL correspondentes à Atividade 2 para criar o banco de dados `sistema_banco` e a tabela `usuarios`:

```sql
CREATE DATABASE sistema_banco;
USE sistema_banco;
CREATE TABLE usuarios (
    nome VARCHAR(50) PRIMARY KEY,
    senha VARCHAR(50) NOT NULL
);
INSERT INTO usuarios (nome, senha) VALUES ('admin', '1234');
```

3. Altere o dicionário `DB_CONFIG` no código Python com as credenciais do seu servidor local e execute o programa.

### Atividade 3 (Sistema de Cadastro de PET)
Esta atividade utiliza um banco de dados separado para não interferir na Atividade 2.

1. No MySQL Workbench, execute o seguinte script para criar o novo banco de dados `sistema_pet` e as tabelas necessárias:

```sql
CREATE DATABASE sistema_pet;
USE sistema_pt;

CREATE TABLE usuarios (
    nome VARCHAR(50) PRIMARY KEY,
    senha VARCHAR(50) NOT NULL
);

INSERT INTO usuarios (nome, senha) VALUES ('admin', '1234');

CREATE TABLE pets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dono VARCHAR(50),
    nome VARCHAR(50),
    idade VARCHAR(20),
    raca VARCHAR(50),
    peso VARCHAR(20),
    cor VARCHAR(30)
);
```

2. Abra o arquivo Python da Atividade 3.
3. Confirme que o dicionário `DB_CONFIG` tem a senha correta do seu servidor local:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'SUA_SENHA_AQUI',
    'database': 'sistema_pet'
}
```

4. Salve o arquivo e execute o código. O login poderá ser feito com `admin` e `1234`. Os pets cadastrados ficarão associados e visíveis apenas para o usuário que fez o login.