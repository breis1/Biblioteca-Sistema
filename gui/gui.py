import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTreeView,
                             QDialog, QDialogButtonBox, QHBoxLayout, QComboBox, QFormLayout, QHeaderView,
                             QMessageBox)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from database.database import BibliotecaDB

class BibliotecaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.db = BibliotecaDB('biblioteca', 'postgres', 'Brunovisqui1@', 'localhost')
        self.contexto_atual = 'livro'  # Começa com contexto de busca por livros

    def initUI(self):
        self.setWindowTitle('Biblioteca')
        self.setGeometry(100, 100, 1000, 700)

        layout = QVBoxLayout()

        # Layout para buscar
        searchLayout = QHBoxLayout()
        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText('Buscar')
        searchLayout.addWidget(self.searchBar)

        self.searchButton = QPushButton('Buscar', self)
        searchLayout.addWidget(self.searchButton)
        self.searchButton.clicked.connect(self.buscar_item)

        layout.addLayout(searchLayout)

        # Área para listar resultados
        self.resultList = QTreeView(self)
        self.resultModel = QStandardItemModel()
        self.resultList.setModel(self.resultModel)
        layout.addWidget(self.resultList)

        # Layout para filtrar e ordenar
        filterLayout = QHBoxLayout()
        self.orderByCombo = QComboBox(self)
        self.orderByCombo.addItems(['ID', 'Titulo', 'Autor', 'Ano', 'ISBN', 'Quantidade'])
        filterLayout.addWidget(QLabel('Ordenar por:', self))
        filterLayout.addWidget(self.orderByCombo)

        self.orderDirCombo = QComboBox(self)
        self.orderDirCombo.addItems(['ASC', 'DESC'])
        filterLayout.addWidget(QLabel('Direção:', self))
        filterLayout.addWidget(self.orderDirCombo)

        self.filterButton = QPushButton('Filtrar', self)
        filterLayout.addWidget(self.filterButton)
        self.filterButton.clicked.connect(self.atualizar_lista)

        layout.addLayout(filterLayout)

        # Layout para botões específicos
        buttonLayout = QHBoxLayout()
        self.loadAllButton = QPushButton('Listar Todos os Livros', self)
        buttonLayout.addWidget(self.loadAllButton)
        self.loadAllButton.clicked.connect(self.listar_todos_livros)

        self.loadAvailableButton = QPushButton('Listar Livros Disponíveis', self)
        buttonLayout.addWidget(self.loadAvailableButton)
        self.loadAvailableButton.clicked.connect(self.listar_livros_disponiveis)

        self.listarUsuariosButton = QPushButton('Listar Usuários', self)
        buttonLayout.addWidget(self.listarUsuariosButton)
        self.listarUsuariosButton.clicked.connect(self.listar_usuarios)

        layout.addLayout(buttonLayout)

        # Layout para empréstimos
        emprestimoLayout = QVBoxLayout()

        self.emprestarBar = QLineEdit(self)
        self.emprestarBar.setPlaceholderText('ID do Livro para Empréstimo')
        emprestimoLayout.addWidget(self.emprestarBar)

        self.usuarioBar = QLineEdit(self)
        self.usuarioBar.setPlaceholderText('ID do Usuário')
        emprestimoLayout.addWidget(self.usuarioBar)

        self.emprestarButton = QPushButton('Emprestar Livro', self)
        self.emprestarButton.clicked.connect(self.emprestar_livro)
        emprestimoLayout.addWidget(self.emprestarButton)

        self.devolverBar = QLineEdit(self)
        self.devolverBar.setPlaceholderText('ID do Empréstimo para Devolução')
        emprestimoLayout.addWidget(self.devolverBar)

        self.devolverButton = QPushButton('Devolver Livro', self)
        self.devolverButton.clicked.connect(self.devolver_livro)
        emprestimoLayout.addWidget(self.devolverButton)

        layout.addLayout(emprestimoLayout)

        # Botão para listar empréstimos
        self.listarEmprestimosButton = QPushButton('Listar Empréstimos', self)
        self.listarEmprestimosButton.clicked.connect(self.listar_emprestimos)
        layout.addWidget(self.listarEmprestimosButton)

        # Botão para criar usuário
        self.criarUsuarioButton = QPushButton('Criar Usuário', self)
        self.criarUsuarioButton.clicked.connect(self.criar_usuario)
        layout.addWidget(self.criarUsuarioButton)

        self.setLayout(layout)

    def atualizar_lista(self):
        ordem = self.orderByCombo.currentText().lower()
        direcao = self.orderDirCombo.currentText()

        if self.contexto_atual == 'livro':
            self.atualizar_lista_livros(self.db.listar_livros(ordem, direcao))
        elif self.contexto_atual == 'emprestimo':
            self.atualizar_lista_emprestimos(self.db.listar_emprestimos(ordem, direcao))

    def atualizar_lista_livros(self, resultados):
        self.resultModel.clear()
        self.resultModel.setColumnCount(6)
        self.resultModel.setHorizontalHeaderLabels(['ID', 'Titulo', 'Autor', 'Ano', 'ISBN', 'Quantidade'])

        for row in resultados:
            item = []
            for col in row:
                item.append(QStandardItem(str(col)))
            self.resultModel.appendRow(item)

        self.resultList.header().setSectionResizeMode(QHeaderView.ResizeToContents)

    def atualizar_lista_emprestimos(self, resultados):
        self.resultModel.clear()
        self.resultModel.setColumnCount(5)
        self.resultModel.setHorizontalHeaderLabels(['ID', 'Livro', 'Usuário', 'Data Empréstimo', 'Data Devolução'])

        for row in resultados:
            item = []
            for col in row:
                item.append(QStandardItem(str(col)))
            self.resultModel.appendRow(item)

        self.resultList.header().setSectionResizeMode(QHeaderView.ResizeToContents)

    def buscar_item(self):
        texto_busca = self.searchBar.text()
        if not texto_busca:
            QMessageBox.warning(self, 'Erro', 'Por favor, insira um termo de busca.')
            return

        resultados = self.db.buscar(self.contexto_atual, texto_busca)

        if self.contexto_atual == 'livro':
            self.atualizar_lista_livros(resultados)
        elif self.contexto_atual == 'emprestimo':
            self.atualizar_lista_emprestimos(resultados)
        elif self.contexto_atual == 'usuario':
            self.atualizar_lista_usuarios(resultados)

    def listar_todos_livros(self):
        self.atualizar_lista_livros(self.db.listar_livros())

    def listar_livros_disponiveis(self):
        self.atualizar_lista_livros(self.db.listar_livros_disponiveis())

    def listar_emprestimos(self):
        self.atualizar_lista_emprestimos(self.db.listar_emprestimos())

    def listar_usuarios(self):
        resultados = self.db.listar_usuarios()
        self.atualizar_lista_usuarios(resultados)

    def criar_usuario(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Criar Usuário')

        layout = QFormLayout()
        nomeLabel = QLabel('Nome:')
        nomeInput = QLineEdit()
        layout.addRow(nomeLabel, nomeInput)

        emailLabel = QLabel('Email:')
        emailInput = QLineEdit()
        layout.addRow(emailLabel, emailInput)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)

        layout.addWidget(buttonBox)
        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            nome = nomeInput.text()
            email = emailInput.text()

            if nome and email:
                novo_id = self.db.criar_usuario(nome, email)
                QMessageBox.information(self, 'Usuário Criado', f'Usuário criado com ID: {novo_id}')
                self.listar_usuarios()
            else:
                QMessageBox.warning(self, 'Erro', 'Por favor, preencha todos os campos.')

    def emprestar_livro(self):
        livro_id = self.emprestarBar.text()
        usuario_id = self.usuarioBar.text()

        if not livro_id or not usuario_id:
            QMessageBox.warning(self, 'Erro', 'Por favor, insira IDs válidos para livro e usuário.')
            return

        try:
            self.db.emprestar_livro(int(livro_id), int(usuario_id))
            QMessageBox.information(self, 'Empréstimo Realizado', 'Livro emprestado com sucesso.')
            self.emprestarBar.clear()
            self.usuarioBar.clear()
        except Exception as e:
            QMessageBox.warning(self, 'Erro', f'Erro ao realizar empréstimo: {e}')

    def devolver_livro(self):
        emprestimo_id = self.devolverBar.text()

        if not emprestimo_id:
            QMessageBox.warning(self, 'Erro', 'Por favor, insira um ID válido para o empréstimo.')
            return

        try:
            self.db.devolver_livro(int(emprestimo_id))
            QMessageBox.information(self, 'Devolução Realizada', 'Livro devolvido com sucesso.')
            self.devolverBar.clear()
        except Exception as e:
            QMessageBox.warning(self, 'Erro', f'Erro ao realizar devolução: {e}')

    def atualizar_lista_usuarios(self, resultados):
        self.resultModel.clear()
        self.resultModel.setColumnCount(3)
        self.resultModel.setHorizontalHeaderLabels(['ID', 'Nome', 'Email'])

        for row in resultados:
            item = []
            for col in row:
                item.append(QStandardItem(str(col)))
            self.resultModel.appendRow(item)

        self.resultList.header().setSectionResizeMode(QHeaderView.ResizeToContents)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    biblioteca_app = BibliotecaApp()
    biblioteca_app.show()
    sys.exit(app.exec_())
