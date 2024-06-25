# database/database.py

import psycopg2

class BibliotecaDB:
    def __init__(self, dbname, user, password, host):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        self.create_tables()

    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS livros (
                    id SERIAL PRIMARY KEY,
                    titulo VARCHAR(255) NOT NULL,
                    autor VARCHAR(255) NOT NULL,
                    ano INT NOT NULL,
                    isbn VARCHAR(255) NOT NULL,
                    quantidade INT NOT NULL
                );
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL
                );
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS emprestimos (
                    id SERIAL PRIMARY KEY,
                    livro_id INT NOT NULL,
                    usuario_id INT NOT NULL,
                    data_emprestimo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_devolucao TIMESTAMP,
                    FOREIGN KEY (livro_id) REFERENCES livros(id),
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                );
            ''')
            self.conn.commit()

    def criar_usuario(self, nome, email):
        with self.conn.cursor() as cur:
            cur.execute('INSERT INTO usuarios (nome, email) VALUES (%s, %s) RETURNING id;', (nome, email))
            self.conn.commit()
            return cur.fetchone()[0]

    def listar_livros(self, ordem='id', direcao='ASC'):
        with self.conn.cursor() as cur:
            try:
                cur.execute(f'SELECT id, titulo, autor, ano, isbn, quantidade FROM livros ORDER BY livros.{ordem} {direcao};')
                return cur.fetchall()
            except psycopg2.Error as e:
                print(f"Erro ao listar livros: {e}")
                return []

    def listar_livros_disponiveis(self):
        with self.conn.cursor() as cur:
            cur.execute('SELECT id, titulo, autor, ano, isbn, quantidade FROM livros WHERE quantidade > 0;')
            return cur.fetchall()

    def emprestar_livro(self, livro_id, usuario_id):
        cur = self.conn.cursor()

        try:
            # Verificar se há livros disponíveis antes de emprestar
            cur.execute('SELECT quantidade FROM livros WHERE id = %s;', (livro_id,))
            quantidade_atual = cur.fetchone()[0]

            if quantidade_atual > 0:
                # Inserir o empréstimo na tabela de empréstimos
                cur.execute('INSERT INTO emprestimos (livro_id, usuario_id) VALUES (%s, %s);', (livro_id, usuario_id))

                # Atualizar a quantidade disponível de livros
                cur.execute('UPDATE livros SET quantidade = quantidade - 1 WHERE id = %s;', (livro_id,))

                self.conn.commit()
            else:
                print("Não há livros disponíveis para empréstimo.")

        except Exception as e:
            print(f"Erro ao emprestar livro: {e}")

        finally:
            cur.close()

    def devolver_livro(self, emprestimo_id):
        with self.conn.cursor() as cur:
            cur.execute('UPDATE emprestimos SET data_devolucao = CURRENT_TIMESTAMP WHERE id = %s AND data_devolucao IS NULL;', (emprestimo_id,))
            cur.execute('UPDATE livros SET quantidade = quantidade + 1 WHERE id = (SELECT livro_id FROM emprestimos WHERE id = %s);', (emprestimo_id,))
            self.conn.commit()

    def listar_emprestimos(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    e.id,
                    l.titulo AS livro,
                    u.nome AS usuario,
                    TO_CHAR(e.data_emprestimo, 'DD/MM/YYYY HH24:MI:SS') AS data_emprestimo,
                    TO_CHAR(e.data_devolucao, 'DD/MM/YYYY HH24:MI:SS') AS data_devolucao
                FROM 
                    emprestimos e
                    JOIN livros l ON e.livro_id = l.id
                    JOIN usuarios u ON e.usuario_id = u.id
                ORDER BY e.id DESC;
            """)
            return cur.fetchall()

    def listar_usuarios(self):
        with self.conn.cursor() as cur:
            cur.execute('SELECT id, nome, email FROM usuarios;')
            return cur.fetchall()

    def buscar(self, contexto, termo):
        with self.conn.cursor() as cur:
            if contexto == 'livro':
                cur.execute('SELECT id, titulo, autor, ano, isbn, quantidade FROM livros WHERE LOWER(titulo) LIKE LOWER(%s) OR LOWER(autor) LIKE LOWER(%s) OR isbn LIKE %s;', (f'%{termo}%', f'%{termo}%', f'%{termo}%'))
                return cur.fetchall()
            elif contexto == 'emprestimo':
                cur.execute("""
                    SELECT 
                        e.id,
                        l.titulo AS livro,
                        u.nome AS usuario,
                        TO_CHAR(e.data_emprestimo, 'DD/MM/YYYY HH24:MI:SS') AS data_emprestimo,
                        TO_CHAR(e.data_devolucao, 'DD/MM/YYYY HH24:MI:SS') AS data_devolucao
                    FROM 
                        emprestimos e
                        JOIN livros l ON e.livro_id = l.id
                        JOIN usuarios u ON e.usuario_id = u.id
                    WHERE 
                        LOWER(l.titulo) LIKE LOWER(%s)
                        OR LOWER(l.autor) LIKE LOWER(%s)
                        OR LOWER(u.nome) LIKE LOWER(%s);
                """, (f'%{termo}%', f'%{termo}%', f'%{termo}%'))
                return cur.fetchall()
            elif contexto == 'usuario':
                cur.execute('SELECT id, nome, email FROM usuarios WHERE LOWER(nome) LIKE LOWER(%s) OR LOWER(email) LIKE LOWER(%s);', (f'%{termo}%', f'%{termo}%'))
                return cur.fetchall()
            else:
                raise ValueError(f'Contexto desconhecido: {contexto}')
