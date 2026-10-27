CREATE DATABASE sistema_banco;
USE sistema_banco;
CREATE TABLE usuarios (
    nome VARCHAR(50) PRIMARY KEY,
    senha VARCHAR(50) NOT NULL
);
INSERT INTO usuarios (nome, senha) VALUES ('admin', '1234');