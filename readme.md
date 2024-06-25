# Sistema de Biblioteca

Este é um sistema de biblioteca desenvolvido em Python usando PostgreSQL como banco de dados.

## Requisitos

- Python 3.x
- PostgreSQL

## Configuração

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/breis1/Biblioteca-Sistema/
   cd SistemaBiblioteca
Instale as dependências:

Recomenda-se criar um ambiente virtual antes de instalar as dependências.

bash
Copiar código
python -m venv venv
source venv/bin/activate  # no Windows use `venv\Scripts\activate`
pip install -r requirements.txt
Configure o banco de dados:

Certifique-se de que o PostgreSQL está instalado e configurado.
Crie um banco de dados chamado biblioteca.
Execute as migrações do banco de dados:

bash
Copiar código
python manage.py migrate
Execute o servidor:

bash
Copiar código
python manage.py runserver
Acesse a aplicação:

Abra seu navegador e acesse http://localhost:8000 para visualizar a aplicação.

Funcionalidades
Listagem de livros, usuários e empréstimos.
Pesquisa dinâmica por livros, usuários e empréstimos.
Gerenciamento de empréstimos (emprestar e devolver livros).
Contribuição
Contribuições são bem-vindas! Para alterações importantes, abra um problema primeiro para discutir o que você gostaria de mudar.
requirements.txt: Lista de dependências do Python necessárias para o projeto.
Contribuições
Contribuições são bem-vindas! Para reportar bugs, sugestões ou contribuir com código, por favor abra uma issue ou envie um pull request no GitHub.

Autor
Bruno Rodrigues Reis
RA: 8222243147
