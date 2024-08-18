# Para usar: 
<p> para acessar o executável do windows vá para dist/firstwindow.py e clique em "view raw" para instalção. </p>

## Banco de dados:

### Crie a database:

<p>
CREATE DATABASE meusql;  
</p>

### Crie a tabela:

<p>
  CREATE TABLE `acervo` (
  `i_id_acervo` int NOT NULL AUTO_INCREMENT,
  `s_titulo_acervo` varchar(200) NOT NULL,
  `s_autor_acervo` varchar(100) NOT NULL,
  `s_genero_acervo` varchar(50) NOT NULL,
  `i_quantidade_acervo` int NOT NULL,
  PRIMARY KEY (`i_id_acervo`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
</p>

# Sobre o projeto

## Descrição:

<p> Um executável que possui uma interface gráfica capaz de cadastrar, alterar, consultar e excluir livros no banco de dados.</p>

Tecnologias: ![Python](https://img.shields.io/badge/-Python-yellow) ![Tkinter](https://img.shields.io/badge/-Tkinter-darkred) ![MySQL](https://img.shields.io/badge/-MySQL-blue) 

## Interface:

![executavel_tkinter](https://github.com/user-attachments/assets/66b298f3-7c70-4d7e-b438-ac9523c281e0)

