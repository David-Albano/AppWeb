from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import make_response
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from matplotlib import pyplot as plt
from datetime import datetime

# Importamos funções
from funçoes import *

# Importamos formularios.py
import formularios

app = Flask(__name__)
# RuntimeError: A secret key is required to use CSRF.
app.secret_key = "minha_chave_secreta_"
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/app_web_database.db'
db = SQLAlchemy(app)


# Definição de tabelas na base de dados
class Cliente(db.Model):
    __tablename = "Cliente"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.Integer)
    email = db.Column(db.String(100), unique=True)
    endereço = db.Column(db.String)
    NIF = db.Column(db.Integer, unique=True)
    contrasenha = db.Column(db.String(10))
    compras = db.Column(db.Integer)
    total_compras = db.Column(db.Float)


class Compras_Cliente(db.Model):
    __tablename__ = "Compras Clientes"
    id = db.Column(db.Integer, primary_key=True)
    email_comprador = db.Column(db.String(200))
    dia = db.Column(db.String(200))
    mes = db.Column(db.String(200))
    ano = db.Column(db.String(200))
    hora = db.Column(db.String(200))
    referencia_produto = db.Column(db.String(9))
    preço = db.Column(db.Float)
    quantidade = db.Column(db.Integer)
    valor_total = db.Column(db.Float)

class Carrinho_de_Compras(db.Model):
    __tablename__ = "Carrinho"
    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.String)
    email_comprador = db.Column(db.String(200))
    marca = db.Column(db.String(200))
    modelo = db.Column(db.String(200))
    referencia_produto = db.Column(db.String(9))
    preço = db.Column(db.Float)
    quantidade = db.Column(db.Integer)
    valor_total = db.Column(db.Float)

class Fornecedor(db.Model):
    __tablename__ = "Fornecedores"
    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.String)
    NIF = db.Column(db.Integer, unique=True)
    contrasenha = db.Column(db.String(10))
    telefone = db.Column(db.Integer)
    email = db.Column(db.String(100), unique=True)
    endereço = db.Column(db.String)


class Produtos_Fornecedor(db.Model):
    __tablename__ = "Produtos Fornecedor"
    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.String)
    email_empresa = db.Column(db.String(100))
    descriçao = db.Column(db.String)
    tipo = db.Column(db.String(100))
    marca = db.Column(db.String(200))
    modelo = db.Column(db.String(200))
    referencia = db.Column(db.String(9), unique=True)
    preço_compra = db.Column(db.Float)
    IVA = db.Column(db.Integer)
    desconto = db.Column(db.Float)
    stock = db.Column(db.Integer)

class Vendas_Fornecedores(db.Model):
    __tablename__ = "Vendas Fornecedores"
    id = db.Column(db.Integer, primary_key=True)
    email_fornecedor = db.Column(db.String(200))
    dia = db.Column(db.String(200))
    mes = db.Column(db.String(200))
    ano = db.Column(db.String(200))
    hora = db.Column(db.String(200))
    referencia_produto = db.Column(db.String(9))
    preço = db.Column(db.Float)
    quantidade = db.Column(db.Integer)
    valor_total = db.Column(db.Float)

class Dados_Empresa(db.Model):
    __tablename__ = "Dados da Empresa"
    id = db.Column(db.Integer, primary_key=True)
    nome_da_empresa = db.Column(db.String)
    NIF = db.Column(db.Integer, unique=True)
    contrasenha = db.Column(db.String(10))
    telefone = db.Column(db.Integer)
    email = db.Column(db.String(100))
    endereço = db.Column(db.String)
    codigo_postal = db.Column(db.Integer)
    numero_compras = db.Column(db.Integer)
    numero_vendas = db.Column(db.Integer)
    valor_total_compras = db.Column(db.Float)
    valor_total_vendas = db.Column(db.Float)


class Produtos_Empresa(db.Model):
    __tablename__ = "Produtos da Empresa"
    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.String)
    tipo = db.Column(db.String(100))
    descriçao = db.Column(db.String)
    marca = db.Column(db.String(200))
    modelo = db.Column(db.String(200))
    preço_de_compra = db.Column(db.Float)
    preço_de_venda = db.Column(db.Float)
    stock = db.Column(db.Integer)
    limite_em_stock = db.Column(db.Integer)
    referencia = db.Column(db.String(12), unique=True)
    armazem = db.Column(db.String)

class Utilizadores(db.Model):
    __tablename__ = "Utilizadores"
    id = db.Column(db.Integer, primary_key=True)
    utilizador = db.Column(db.String(100))

cliente = Utilizadores(utilizador="Cliente")
fornecedor = Utilizadores(utilizador="Fornecedor")
admin = Utilizadores(utilizador="Admin")

# Criação dos principais dados da empresa, para acesso à plataforma, informação e contacto
empresa = Dados_Empresa(nome_da_empresa="SuperEquipments",
                        NIF=505123456,
                        contrasenha="12345678",
                        telefone="202123456",
                        email="geral@superequip.com",
                        endereço="Rua do norte 285, Portugal",
                        codigo_postal="3800-123",
                        numero_compras=0,
                        numero_vendas=0,
                        valor_total_compras=0,
                        valor_total_vendas=0)

# Criação de tabelas
with app.app_context():
    db.create_all()
    # db.session.add(cliente) # Comentar depois da primera execução
    # db.session.add(fornecedor) # Comentar depois da primera execução
    # db.session.add(admin) # Comentar depois da primera execução
    # db.session.add(empresa) # Comentar depois da primera execução

    db.session.commit()

# Criação de rutas e métodos

# ! Verificamos se existe uma sessão para poder acceder às interfaces que correspondam ao utilizador.. con:
# if 'email' in session:
# return redirect(url_for('ir_a_login'))

# - Rutas Login/Logout/Criação de conta
@app.route('/', methods=["GET", "POST"])
def ir_a_login():
    form_utilizadores = Utilizadores.query.all()
    form_login = formularios.FormularioLogin()
    value_utilizador = request.form.get('user-type')
    return render_template('login.html',
                           form_login=form_login,
                           form_utilizadores=form_utilizadores,
                           value_utilizador=value_utilizador)

@app.route('/terminar-sessao', methods=["GET", "POST"])
def terminar_sessao():
    if 'email' in session:
        ler_cookie()
        session.pop('email', None)
        mensagem = "A sessão foi terminada com sucesso"
    return redirect(url_for('ir_a_login'))


@app.route('/fazer-login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        value_utilizador = request.form.get('user-type')
        form_utilizadores = Utilizadores.query.all()
        form_login = formularios.FormularioLogin(request.form)
        email= form_login.email.data
        contrasenha= form_login.contrasenha.data
        produtos = Produtos_Empresa().query.all()

        # Fazer o inicio de sessão e reencaminhamos para a interface correspondente ao tipo utilizador
        if value_utilizador == "Cliente":
            usuario_cliente = Cliente().query.filter_by(email=email).first()
            return iniciar_sessao(usuario_cliente, 'categorias/pagina_inicial.html', contrasenha, value_utilizador, form_login, form_utilizadores, produtos)

        elif value_utilizador == "Fornecedor":
            usuario_fornecedor = Fornecedor().query.filter_by(email=email).first()
            return iniciar_sessao(usuario_fornecedor, 'categorias/pagina_inicial.html', contrasenha, value_utilizador, form_login, form_utilizadores, produtos)

        elif value_utilizador == "Admin":
            usuario_admin = Dados_Empresa().query.filter_by(email=email).first()
            return iniciar_sessao(usuario_admin, 'categorias/pagina_inicial.html', contrasenha, value_utilizador, form_login, form_utilizadores, produtos)

@app.route('/criar-utilizador', methods=["GET", "POST"])
def criar_utilizador():
    form_utilizadores = Utilizadores.query.all()
    form_utilizador = formularios.FormularioUtilizador(request.form)
    # Obtemos a informação dos formulários
    tipo_utilizador = request.form.get('user-type')
    email = form_utilizador.email.data
    nif = form_utilizador.NIF.data
    mensagem=""

    # Validamos a informação inserida dos formulários
    if form_utilizador.validate():
        if tipo_utilizador == 'Cliente':
            email_usuario = Cliente().query.filter_by(email=email).first()
            nif_usuario = Cliente().query.filter_by(NIF=nif).first()

            # Comprovar se o email ou o NIF já existem
            if email_usuario:
                mensagem = "Este email já se encontra em uso. Introduça outro email"
            elif nif_usuario:
                mensagem = "Este NIF já se encontra em uso. Introduça outro NIF"
            else:
                # Criação do usuário cliente
                utilizador = Cliente(nome=form_utilizador.nome.data,
                                    telefone=form_utilizador.telefone.data,
                                    email=form_utilizador.email.data,
                                    endereço=form_utilizador.endereço.data,
                                    NIF=form_utilizador.NIF.data,
                                    contrasenha=form_utilizador.contrasenha.data,
                                    compras=0,
                                    total_compras=0)

                db.session.add(utilizador)
                db.session.commit()

                mensagem = "Parabéns! A sua conta foi criada com sucesso! Faça login para ingressa a nossa plataforma"

        elif tipo_utilizador == 'Fornecedor':
            email_usuario = Fornecedor().query.filter_by(email=email).first()
            nif_usuario = Fornecedor().query.filter_by(NIF=nif).first()

            # Comprovar se o email ou o NIF já existem
            if email_usuario:
                mensagem = "Este email já se encontra em uso.Introduça outro email"
            elif nif_usuario:
                mensagem = "Este NIF já se encontra em uso. Introduça outro NIF"
            else:
                # Criação do usuário fornecedor
                utilizador = Fornecedor(empresa=form_utilizador.nome.data,
                                        telefone=form_utilizador.telefone.data,
                                        email=form_utilizador.email.data,
                                        endereço=form_utilizador.endereço.data,
                                        NIF=form_utilizador.NIF.data,
                                        contrasenha=form_utilizador.contrasenha.data)

                db.session.add(utilizador)
                db.session.commit()

                mensagem = "Parabéns! A sua conta foi criada com sucesso! Faça login para ingressa a nossa plataforma"

    return render_template('criar_utilizador.html',
                           form_utilizadores=form_utilizadores,
                           form_utilizador=form_utilizador,
                           mensagem=mensagem)


# - Rutas interfaces gerais(Para todos os utilizadores)

@app.route('/pagina_inicial', methods=["GET", "POST"])
def ir_a_pagina_inicial():
    if 'email' in session:
        cookies = ler_cookie()
        value_utilizador = cookies['value_utilizador']
        produtos = Produtos_Empresa().query.all()

        return render_template("categorias/pagina_inicial.html",
                               value_utilizador=value_utilizador,
                               categorias=categorias,
                               produtos=produtos)
    return ir_fazer_login()

@app.route('/categorias/<tipo>', methods=["GET", "POST"])
def ir_a_categoria(tipo):
    if 'email' in session:
        cookies = ler_cookie()
        value_utilizador = cookies['value_utilizador']
        produtos = Produtos_Empresa().query.filter_by(tipo=tipo)

        return render_template("categorias/categorias.html",
                               value_utilizador=value_utilizador,
                               tipo=tipo,
                               categorias=categorias,
                               produtos=produtos)
    return ir_fazer_login()

@app.route('/produto/<referencia>', methods=["GET", "POST"])
def ir_a_produto(referencia):
    if 'email' in session:
        cookies = ler_cookie()
        value_utilizador = cookies['value_utilizador']
        email = cookies['email']
        input_quantidade = formularios.OferecerProduto()
        form_quantidade = formularios.OferecerProduto(request.form)
        quantidade_compra = form_quantidade.quantidade.data
        mensagem=""

        produto_carrinho = Carrinho_de_Compras().query.filter_by(email_comprador=email,
                                                                 referencia_produto=referencia).first()
        produto = Produtos_Empresa().query.filter_by(referencia=referencia).first()

        # Adicionar produto ao carrinho de compras
        if quantidade_compra != None:
            if produto:
                if quantidade_compra <= 0:
                    mensagem = 'A quantidade deve ser maior que 0'
                elif quantidade_compra > produto.stock:
                    mensagem=f'A quantidade deve menor a {produto.stock}'
                else:
                    if produto_carrinho:
                        produto_carrinho.quantidade += quantidade_compra
                        produto_carrinho.valor_total = produto.preço_de_venda * produto_carrinho.quantidade
                        mensagem="Produto adicionado satisfatoriamente ao teu carrinho de compras"
                    else:
                        valor_total = produto.preço_de_venda * quantidade_compra
                        produto_carrinho = Carrinho_de_Compras(empresa=produto.empresa,
                                                               email_comprador=email,
                                                               marca=produto.marca,
                                                               modelo=produto.modelo,
                                                               referencia_produto=referencia,
                                                               preço=produto.preço_de_venda,
                                                               quantidade=quantidade_compra,
                                                               valor_total=valor_total)
                        mensagem="Produto adicionado satisfatoriamente ao teu carrinho de compras"

                    db.session.add(produto_carrinho)
                    db.session.commit()


        return render_template('categorias/produto.html',
                               value_utilizador=value_utilizador,
                               categorias=categorias,
                               produto=produto,
                               input_quantidade=input_quantidade,
                               mensagem=mensagem)
    return ir_fazer_login()

# - Rutas Interfaces Cliente

@app.route('/carrinho', methods=["GET", "POST"])
def ir_a_carrinho():
    if 'email' in session:
        if session['value_utilizador'] != 'Fornecedor':
            cookies = ler_cookie()
            value_utilizador = cookies['value_utilizador']
            email = cookies['email']

            # Mostrar conteudo do carrinho de compras do usuario
            produtos_carrinho = Carrinho_de_Compras().query.filter_by(email_comprador=email)

            total_carrinho = 0
            for produto in produtos_carrinho:
                total_carrinho += produto.valor_total

            return render_template('cliente/carrinho.html',
                                   value_utilizador=value_utilizador,
                                   categorias=categorias,
                                   produtos_carrinho=produtos_carrinho,
                                   total_carrinho=round(total_carrinho, 2))
        else:
            return mensagem_interdito()
    return ir_fazer_login()

@app.route('/eliminar-produto-carrinho/<referencia>', methods=["GET", "POST"])
def eliminar_produto_carrinho(referencia):
    if 'email' in session:
        cookies = ler_cookie()
        email = cookies['email']

        produto_carrinho = Carrinho_de_Compras().query.filter_by(referencia_produto=referencia, email_comprador=email).delete()
        db.session.commit()
        return redirect(url_for('ir_a_carrinho'))
    return ir_fazer_login()


@app.route('/diminuir-carrinho/<referencia>', methods=["GET", "POST"])
def diminuir_carrinho(referencia):
    if 'email' in session:
        cookies = ler_cookie()
        email = cookies['email']

        produto_carrinho = Carrinho_de_Compras().query.filter_by(referencia_produto=referencia, email_comprador=email).first()

        produto_carrinho.quantidade -= 1
        valor_total_carrinho = produto_carrinho.valor_total - produto_carrinho.preço
        produto_carrinho.valor_total = round(valor_total_carrinho, 2)
        db.session.commit()

        if produto_carrinho.quantidade > 0:
            return redirect(url_for('ir_a_carrinho'))
        else:
            return redirect(url_for('eliminar_produto_carrinho', referencia=referencia))
    return ir_fazer_login()

@app.route('/aumentar-carrinho/<referencia>', methods=["GET", "POST"])
def aumentar_carrinho(referencia):
    if 'email' in session:
        cookies = ler_cookie()
        email = cookies['email']

        produto_carrinho = Carrinho_de_Compras().query.filter_by(referencia_produto=referencia, email_comprador=email).first()

        produto_carrinho.quantidade += 1
        valor_total_carrinho = produto_carrinho.valor_total + produto_carrinho.preço
        produto_carrinho.valor_total = round(valor_total_carrinho, 2)
        db.session.commit()

        return redirect(url_for('ir_a_carrinho'))
    return ir_fazer_login()

@app.route('/comprar-carrinho', methods=["GET", "POST"])
def comprar_carrinho():
    if 'email' in session:
        if session['value_utilizador'] != 'Fornecedor':
            cookies = ler_cookie()
            email = cookies['email']
            value_utilizador = cookies['value_utilizador']

            mensagem=""

            # Obtemos a data da venda
            dt = datetime.now()
            dia = dt.day
            mes = dt.month
            ano = dt.year
            hora = "{}:{}".format(dt.hour, dt.minute)

            produto_carrinho = Carrinho_de_Compras().query.filter_by(email_comprador=email).all()
            compras_cliente = Cliente().query.filter_by(email=email).first()

            # Aramzenamos os dados da venda
            for produto in produto_carrinho:
                produto_comprado=Compras_Cliente(email_comprador=email,
                                                 dia=dia,
                                                 mes=mes,
                                                 ano=ano,
                                                 hora=hora,
                                                 referencia_produto=produto.referencia_produto,
                                                 preço=produto.preço,
                                                 quantidade=produto.quantidade,
                                                 valor_total=produto.valor_total)

                # Restar quantiade em stock
                produto_empresa = Produtos_Empresa.query.filter_by(referencia=produto.referencia_produto).first()
                produto_empresa.stock -= produto.quantidade

                # Guardamos nos dados da empresa as quantidades e os valores da compra realizada
                venda_empresa = Dados_Empresa().query.filter_by(id=1).first()
                venda_empresa.valor_total_vendas += produto.valor_total
                venda_empresa.numero_vendas += produto.quantidade

                produto_carrinho = Carrinho_de_Compras().query.filter_by(referencia_produto=produto.referencia_produto, email_comprador=email).delete()
                compras_cliente.compras += 1  # Uma unidade por cada categoria de artigo
                compras_cliente.total_compras += produto.valor_total

                mensagem = "Compra efetuada com sucesso! Obrigado pela vossa confiança"

                db.session.add(produto_comprado)
                db.session.commit()
            return render_template('cliente/carrinho.html',
                                   value_utilizador=value_utilizador,
                                   categorias=categorias,
                                   total_carrinho=0,
                                   mensagem=mensagem)
        else:
            return mensagem_interdito()
    return ir_fazer_login()

# - Rutas interfaces do Administrador
@app.route('/stock', methods=["GET", "POST"])
def stock():
        if 'email' in session:
            if session['value_utilizador'] == 'Admin':
                cookies = ler_cookie()
                value_utilizador = cookies['value_utilizador']
                return render_template("admin/stock.html",
                                       value_utilizador=value_utilizador,
                                       categorias=categorias)
            else:
                return mensagem_interdito()
        return ir_fazer_login()


@app.route('/stock/mostrar_stock', methods=["GET", "POST"])
def mostrar_stock():
    if 'email' in session:
            if session['value_utilizador'] == 'Admin':
                cookies = ler_cookie()
                value_utilizador = cookies['value_utilizador']
                stock = Produtos_Empresa.query.all()
                return render_template("admin/mostrar_stock.html",
                                       value_utilizador=value_utilizador,
                                       stock=stock,
                                       categorias=categorias)
            else:
                return mensagem_interdito()
    return ir_fazer_login()

@app.route('/stock/filtrar_stock', methods=["GET", "POST"])
def filtrar_stock():
    if 'email' in session:
        if session['value_utilizador'] == 'Admin':
            cookies = ler_cookie()
            value_utilizador = cookies['value_utilizador']
            tipo = request.form.get("filtro-tipo")
            stock = Produtos_Empresa().query.filter_by(tipo=tipo)
            return render_template("admin/filtrar_stock.html",
                                   # stock=stock,
                                   stock=stock,
                                   categorias=categorias,
                                   value_utilizador=value_utilizador)
        else:
            return mensagem_interdito()
    return ir_fazer_login()

# Rutas interfaces do Administrador

# Interface Admin/Fornecedores
@app.route('/fornecedores', methods=["GET", "POST"])
def fornecedores():
    if 'email' in session:
        if session['value_utilizador'] == 'Admin':
            cookies = ler_cookie()
            value_utilizador = cookies['value_utilizador']
            return render_template("admin/fornecedores.html",
                                   value_utilizador=value_utilizador,
                                   categorias=categorias)
        else:
            return mensagem_interdito()
    return ir_fazer_login()

@app.route('/fornecedores/mostrar_fornecedores', methods=["GET", "POST"])
def mostrar_fornecedores():
    if 'email' in session:
        if session['value_utilizador'] == 'Admin':
            cookies = ler_cookie()
            value_utilizador = cookies['value_utilizador']

            # Mostramos uma tabela com os fornecedores e os seus dados
            fornecedores = Fornecedor.query.all()
            return render_template("admin/mostrar_fornecedores.html",
                                   fornecedores=fornecedores,
                                   categorias=categorias,
                                   value_utilizador=value_utilizador)
        else:
            return mensagem_interdito()
    return ir_fazer_login()

@app.route('/fornecedor/comprar_produto', methods=["GET", "POST"])
def comprar_produto():
    if 'email' in session:
        if session['value_utilizador'] == 'Admin':
            cookies = ler_cookie()
            value_utilizador = cookies['value_utilizador']

            # Filtrar produtos dos fornecedores
            tipo = request.form.get("filtro-tipo")
            if tipo == None:
                produtos_fornecedores = Produtos_Fornecedor.query.all()
            else:
                produtos_fornecedores = Produtos_Fornecedor.query.filter_by(tipo=tipo)
            form_adicionar = formularios.OferecerProduto()
            form_quantidade = formularios.OferecerProduto(request.form)
            quantidade_compra = form_quantidade.quantidade.data
            limite_em_stock = 100
            dados_compras = Dados_Empresa().query.filter_by(id=1).first()

            mensagem=""

            referencia = request.form.get('referencia')
            produto_selecionado = Produtos_Fornecedor().query.filter_by(referencia=referencia).first()
            # Produto já existente no stock da Empresa
            produto_comprado = Produtos_Empresa().query.filter_by(referencia=referencia).first()

            # Obtemos a data da compra
            dt = datetime.now()
            dia = dt.day
            mes = dt.month
            ano = dt.year
            hora = "{}:{}".format(dt.hour, dt.minute)

            if quantidade_compra != None:
                # Se o produto selecionado existe nos produtos dos fornecdores efetuar o seguinte:
                if produto_selecionado:
                    numero_armazem = str(produto_selecionado.id)

                    if quantidade_compra > produto_selecionado.stock:
                        mensagem = "Por favor introduça uma quantidade menor ou igual ao stock do produto"
                    elif quantidade_compra <= 0:
                        mensagem = "A quantidade a comprar não pode ser zero"
                    elif quantidade_compra > limite_em_stock:
                        mensagem = f"A quantidade a comprar debe ser igual ou menor que {limite_em_stock}"
                    else:
                        # Calculamos os preços de compra e venda
                        produto_selecionado.stock -= quantidade_compra
                        preço_iva = produto_selecionado.preço_compra + (produto_selecionado.preço_compra * (produto_selecionado.IVA / 100))
                        preço_compra = preço_iva - (preço_iva * (produto_selecionado.desconto / 100))
                        preço_compra = round(preço_compra, 2)
                        preço_venda = preço_compra * 1.50  # Para granhar o 50% por produto
                        preço_venda = round(preço_venda, 2)

                        # Armazenamos valores nos dados da empresa
                        dados_compras.valor_total_compras += (preço_compra * quantidade_compra)
                        dados_compras.numero_compras += quantidade_compra

                        # Verificamos se o produto já existe em stock e acrescentamos só a quantidade de produtos
                        if produto_comprado:
                            # Verificamos que a quantidade a comprar não ultrapasse o limite do stock
                            if quantidade_compra + produto_comprado.stock > produto_comprado.limite_em_stock:
                                espaço_disponivel_em_stock = produto_comprado.limite_em_stock - produto_comprado.stock
                                mensagem = f"Só podes comprar {espaço_disponivel_em_stock} unidades deste produto"

                            elif produto_comprado.limite_em_stock == produto_comprado.stock:
                                mensagem = f"Não tens espaço suficiente no stock para este produto"

                            else:
                                produto_comprado.stock += quantidade_compra
                                mensagem="Compra realizada com sucesso"

                                # Aramzenamos os dados nas vendas do fornecedor
                                produto_vendido = Vendas_Fornecedores(email_fornecedor=produto_selecionado.email_empresa,
                                                                      dia=dia,
                                                                      mes=mes,
                                                                      ano=ano,
                                                                      hora=hora,
                                                                      referencia_produto=referencia,
                                                                      preço=preço_compra,
                                                                      quantidade=quantidade_compra,
                                                                      valor_total=round(preço_compra * quantidade_compra, 2))
                                db.session.add(produto_vendido)

                        # Definimos a localização no armazém
                        else:
                            if produto_selecionado.tipo == "TV,V,S":
                                armazem = "A-" + numero_armazem
                            elif produto_selecionado.tipo == "FOTO":
                                armazem = "B-" + numero_armazem
                            elif produto_selecionado.tipo == "SP":
                                armazem = "C-" + numero_armazem
                            elif produto_selecionado.tipo == "DESK":
                                armazem = "D-" + numero_armazem
                            elif produto_selecionado.tipo == "G":
                                armazem = "E-" + numero_armazem
                            elif produto_selecionado.tipo == "I&A":
                                armazem = "F-" + numero_armazem

                            # Guardamos o produto comprado na tabela Produtos da Empresa
                            produto_comprado=Produtos_Empresa(empresa=produto_selecionado.empresa,
                                                              tipo=produto_selecionado.tipo,
                                                              descriçao=produto_selecionado.descriçao,
                                                              marca=produto_selecionado.marca,
                                                              modelo=produto_selecionado.modelo,
                                                              preço_de_compra=preço_compra,
                                                              preço_de_venda=preço_venda,
                                                              stock=quantidade_compra,
                                                              limite_em_stock=limite_em_stock,
                                                              referencia=referencia,
                                                              armazem=armazem)

                            # Aramazenamos os dados nas vendas do fornecedor
                            produto_vendido=Vendas_Fornecedores(email_fornecedor=produto_selecionado.email_empresa,
                                                                dia=dia,
                                                                mes=mes,
                                                                ano=ano,
                                                                hora=hora,
                                                                referencia_produto=referencia,
                                                                preço=preço_compra,
                                                                quantidade=quantidade_compra,
                                                                valor_total=round(preço_compra*quantidade_compra, 2))
                            db.session.add(produto_vendido)

                            mensagem="Compra realizada com sucesso"

                        db.session.add(produto_comprado)
                        db.session.add(produto_selecionado)
                        db.session.add(dados_compras)
                        db.session.commit()

            return render_template("admin/ofertas.html",
                                   form_adicionar=form_adicionar,
                                   produtos_fornecedores=produtos_fornecedores,
                                   categorias=categorias,
                                   value_utilizador=value_utilizador,
                                   mensagem=mensagem)
        else:
            return mensagem_interdito()
    return ir_fazer_login()

# Interface Admin/Clientes
@app.route('/clientes', methods=["GET", "POST"])
def mostrar_clientes():
    if 'email' in session:
        if session['value_utilizador'] == 'Admin':
            cookies = ler_cookie()
            value_utilizador = cookies['value_utilizador']

            # Mostramos uma tabela com os clientes e os seus dados
            clientes = Cliente.query.all()
            return render_template("admin/clientes.html",
                                   clientes=clientes,
                                   value_utilizador=value_utilizador,
                                   categorias=categorias)
        else:
            return mensagem_interdito()
    return ir_fazer_login()

# Interface Admin/Dados compra e venda
@app.route('/dados_compra_venda', methods=["GET", "POST"])
def mostrar_dados_compra_venda():
    if 'email' in session:
        cookies = ler_cookie()
        value_utilizador = cookies['value_utilizador']
        utilizadores = Utilizadores().query.all()
        return render_template("admin/dados_compra_e_venda.html",
                               utilizadores=utilizadores,
                               value_utilizador=value_utilizador,
                               categorias=categorias)
    return ir_fazer_login()

@app.route('/mostrar_graficos', methods=["GET", "POST"])
def mostrar_graficos():
    if 'email' in session:
        if session['value_utilizador'] == 'Cliente':
            cookies = ler_cookie()
            value_utilizador = cookies['value_utilizador']
            email = cookies['email']
            query = Compras_Cliente().query.filter_by(email_comprador=email)

            mostrar_dados_de_compra_e_venda(query, 'Compras')
            plt.show()

            return render_template("admin/dados_compra_e_venda.html",
                                   value_utilizador=value_utilizador,
                                   categorias=categorias,
                                   query=query)

        elif session['value_utilizador'] == 'Fornecedor':
            cookies = ler_cookie()
            value_utilizador = cookies['value_utilizador']
            email = cookies['email']
            query = Vendas_Fornecedores().query.filter_by(email_fornecedor=email)

            mostrar_dados_de_compra_e_venda(query, 'Vendas')
            plt.show()

            return render_template("admin/dados_compra_e_venda.html",
                                   value_utilizador=value_utilizador,
                                   categorias=categorias,
                                   query=query)

        elif session['value_utilizador'] == 'Admin':
            cookies = ler_cookie()
            value_utilizador = cookies['value_utilizador']
            email = cookies['email']

            utilizadores = Utilizadores().query.all()
            utilizador = request.form.get('utilizador')

            if utilizador == "Cliente":
                query = Compras_Cliente().query.all()
                mostrar_dados_de_compra_e_venda(query, 'Compras Clientes')
                plt.show()

                return render_template("admin/dados_compra_e_venda.html",
                                       query=query,
                                       utilizadores=utilizadores,
                                       utilizador=utilizador,
                                       value_utilizador=value_utilizador,
                                       categorias=categorias)

            elif utilizador == "Fornecedor":
                query = Vendas_Fornecedores().query.all()
                mostrar_dados_de_compra_e_venda(query, 'Compras a Fornecedores')
                plt.show()

                return render_template("admin/dados_compra_e_venda.html",
                                       query=query,
                                       utilizadores=utilizadores,
                                       utilizador=utilizador,
                                       value_utilizador=value_utilizador,
                                       categorias=categorias)

            elif utilizador == "Admin":
                return render_template('admin/dados_comparativos.html',
                                       utilizadores=utilizadores,
                                       utilizador=utilizador,
                                       value_utilizador=value_utilizador,
                                       categorias=categorias)
        else:
            return mensagem_interdito()
    return ir_fazer_login()

@app.route('/mostrar_graficos_empresa', methods=["GET", "POST"])
def mostrar_graficos_empresa():
    if 'email' in session:
        if session['value_utilizador'] == 'Admin':
            cookies = ler_cookie()
            value_utilizador = cookies['value_utilizador']
            mensagem=""

            utilizadores = Utilizadores().query.all()
            utilizador = request.form.get('utilizador')

            # ---- Para dados totais ----

            # Definimos os valores totais de compras e vendas

            # Filtramos comparativas por data
            form_filtrar_dados = formularios.FiltrarDadosPorData()
            data = formularios.FiltrarDadosPorData(request.form)

            # Definimos os dados para os gráficos atraves da função

            grafico_compras = mostrar_dados_de_compra_e_venda(Vendas_Fornecedores().query.all(), 'Compras')
            grafico_vendas = mostrar_dados_de_compra_e_venda(Compras_Cliente().query.all(), 'Vendas')

            # Personalizamos os gráficos
            plt.subplot(2, 1, 1)
            plt.plot(grafico_compras['x'], grafico_compras['y'], 'r--o', c='red')
            plt.title('Compras')
            plt.suptitle('Gráfica comparativa')
            plt.legend(["€ vs Data/Hora"])
            plt.xticks(rotation=30)
            plt.ylabel('Valor de transação', c='green')
            plt.grid(b=True)

            plt.subplot(2, 1, 2)
            plt.plot(grafico_vendas['x'], grafico_vendas['y'], 'r--o', c='green')
            plt.title('Vendas')

            plt.xlabel('Data da transação', c='blue')
            plt.xticks(rotation=30)
            plt.grid(b=True)
            plt.tight_layout()
            plt.show()

            # Mostramos comparativa de compras e vendas totais
            dados_empresa = Dados_Empresa().query.filter_by(id=1).first()

            total_vendas = dados_empresa.valor_total_vendas
            total_compras = dados_empresa.valor_total_compras
            lucro = total_vendas - total_compras

            dados = {
                'numero_compras': dados_empresa.numero_compras,
                'numero_vendas': dados_empresa.numero_vendas,
                'total_vendas': total_vendas,
                'total_compras': total_compras,
                'lucro': round(lucro, 2)
            }

            return render_template('admin/comparativa_geral.html',
                                               dados=dados,
                                               form_filtrar_dados=form_filtrar_dados,
                                               utilizadores=utilizadores,
                                               utilizador=utilizador,
                                               mensagem=mensagem,
                                               value_utilizador=value_utilizador,
                                               categorias=categorias)
    else:
        return mensagem_interdito()
    return ir_fazer_login()

@app.route('/filtrar_dados_por_data', methods=["GET", "POST"])
def filtrar_dados_por_data():
    if 'email' in session:
        if session['value_utilizador'] == 'Admin':
            cookies = ler_cookie()
            value_utilizador = cookies['value_utilizador']
            mensagem=""

            utilizadores = Utilizadores().query.all()
            utilizador = request.form.get('utilizador')

            # Definimos os valores totais de compras e vendas

            # Filtramos comparativas por data
            form_filtrar_dados = formularios.FiltrarDadosPorData()
            data = formularios.FiltrarDadosPorData(request.form)

            # ---- Para dados filtrados por data ----

            # Covertemos os dados da data a str para manipular de melhor maneira
            dia = data.dia.data
            mes = data.mes.data
            ano = data.ano.data

            # Definir as seguintes variaveis como None para evitar o erro UnboundLocalError: local variable 'dados' referenced before assignment
            # no caso em que dia, mes e ano sejam None
            query_vendas = None
            query_compras = None
            dados = None

            # Validamos os valores inseridos
            if dia == None and mes == None and ano == None:
                mensagem = "Introduça un valor válido"
            else:
                if dia == None and mes and ano:
                    if len(str(mes)) > 2 or mes <= 0 or mes > 12 or ano <= 0 or len(str(ano)) != 4:
                        mensagem = "Introduça uma data válida"
                    else:
                        query_vendas = Compras_Cliente.query.filter_by(mes=str(mes), ano=str(ano))
                        query_compras = Vendas_Fornecedores.query.filter_by(mes=str(mes), ano=str(ano))

                elif dia == None and mes == None:
                    if ano <= 0 or len(str(ano)) != 4:
                        mensagem = "Introduça uma data válida: ano (xxxx)"
                    else:
                        query_vendas = Compras_Cliente.query.filter_by(ano=str(ano))
                        query_compras = Vendas_Fornecedores.query.filter_by(ano=str(ano))

                elif dia == None and ano == None:
                    mensagem = "Não pode inserir só o mês"

                elif mes == None and ano == None:
                    mensagem = "Não pode inserir só o dia"

                elif ano == None:
                    mensagem = "Tem de inserir o ano"

                elif dia != None and mes != None and ano != None:
                    if dia <= 0 or dia > 31 or len(str(dia)) > 2 or len(str(mes)) > 2 or mes <= 0 or mes > 12 or ano <= 0 or len(str(ano)) != 4:
                        mensagem = "Introduça uma data válida"
                    else:
                        query_vendas = Compras_Cliente.query.filter_by(dia=str(dia), mes=str(mes), ano=str(ano))
                        query_compras = Vendas_Fornecedores.query.filter_by(dia=str(dia), mes=str(mes), ano=str(ano))

                if query_vendas and query_compras:
                    # Definimos os dados para os gráficos atraves da função
                    grafico_compras = mostrar_dados_de_compra_e_venda(query_compras, 'Compras')
                    grafico_vendas = mostrar_dados_de_compra_e_venda(query_vendas, 'Vendas')

                    # Personalizamos os gráficos
                    plt.subplot(2, 1, 1)
                    plt.plot(grafico_compras['x'], grafico_compras['y'], 'r--o', c='red')
                    plt.title('Compras')
                    plt.suptitle('Gráfica comparativa')
                    plt.legend(["€ vs Data/Hora"])
                    plt.xticks(rotation=30)
                    plt.ylabel('Valor de transação', c='green')
                    plt.grid(b=True)

                    plt.subplot(2, 1, 2)
                    plt.plot(grafico_vendas['x'], grafico_vendas['y'], 'r--o', c='green')
                    plt.title('Vendas')

                    plt.xlabel('Data da transação', c='blue')
                    plt.xticks(rotation=30)
                    plt.grid(b=True)
                    plt.tight_layout()
                    plt.show()

                    # Definimos os valores totais de compras e vendas filtradas por data

                    dados_compras = query_compras
                    total_compras = 0
                    numero_compras = 0
                    for compras in dados_compras:
                        total_compras += compras.valor_total
                        numero_compras += compras.quantidade

                    dados_vendas = query_vendas
                    total_vendas = 0
                    numero_vendas = 0
                    for vendas in dados_vendas:
                        total_vendas += vendas.valor_total
                        numero_vendas += vendas.quantidade

                    lucro = total_vendas - total_compras

                    dados = {
                        'numero_compras': numero_compras,
                        'numero_vendas': numero_vendas,
                        'total_vendas': total_vendas,
                        'total_compras': total_compras,
                        'lucro': round(lucro, 2)
                    }

            return render_template('admin/comparativa_geral.html',
                                   dados=dados,
                                   form_filtrar_dados=form_filtrar_dados,
                                   utilizadores=utilizadores,
                                   utilizador=utilizador,
                                   mensagem=mensagem,
                                   value_utilizador=value_utilizador,
                                   categorias=categorias)
    else:
        return mensagem_interdito()
    return ir_fazer_login()

# Rutas interfaces do Fornecedor

# Interface Fornecedor/Empresa
@app.route('/empresa', methods=["GET", "POST"])
def empresa():
    if 'email' in session:
        if session['value_utilizador'] != 'Cliente':
           cookies = ler_cookie()
           value_utilizador = cookies['value_utilizador']

           # Mostramos informação e dados de contacto da empresa
           dados_empresa = Dados_Empresa.query.filter_by(id=1).first()
           return render_template("fornecedor/empresa.html",
                                  dados_empresa=dados_empresa,
                                  categorias=categorias,
                                  value_utilizador=value_utilizador)
        else:
            return mensagem_interdito()
    return ir_fazer_login()

@app.route('/oferecer_produto', methods=["GET", "POST"])
def oferecer_produto():
    if 'email' in session:
        if session['value_utilizador'] != 'Cliente':
            cookies = ler_cookie()
            value_utilizador = cookies['value_utilizador']
            email = cookies['email']

            # Produtos oferecidos pelo fornecedor
            produtos_fornecedor = Produtos_Fornecedor.query.filter_by(email_empresa=email)

            # Os fornecedores poderam oferecer todos os os produtos que tiverm disponíveis
            empresa = Fornecedor().query.filter_by(email=email).first()

            mensagem=""

            dados_empresa = Dados_Empresa.query.filter_by(id=1).first()
            form_oferecer = formularios.OferecerProduto()
            # Obtemos e verificamos os dados inseridos no formulário
            tipo=request.form.get('filtros')
            dados_formulario=formularios.OferecerProduto(request.form)
            referencia_existente = Produtos_Fornecedor.query.filter_by(referencia=dados_formulario.referencia.data).first()


            if dados_formulario.validate():

                # Verificamos se a referência do produto já existe
                if referencia_existente:
                    mensagem = "A referência do produto já existe, por favor insira outra referência"

                else:
                    # Guardamos os dados do produto oferecido pela empresa
                    produto_fornecedor= Produtos_Fornecedor(descriçao=dados_formulario.descriçao.data,
                                                        tipo=tipo,
                                                        empresa=empresa.empresa,
                                                        email_empresa=email,
                                                        marca=dados_formulario.marca.data,
                                                        modelo=dados_formulario.modelo.data,
                                                        preço_compra=dados_formulario.preço_compra.data,
                                                        IVA=dados_formulario.IVA.data,
                                                        desconto=dados_formulario.desconto.data,
                                                        referencia=dados_formulario.referencia.data,
                                                        stock=dados_formulario.stock.data)

                    db.session.add(produto_fornecedor)
                    db.session.commit()

                    mensagem = "Produto oferecido satisfatoriamente. A empresa poderá ver o teu produto e comprá-lo"



            return render_template("fornecedor/oferecer_produto.html",
                                   produtos_fornecedor=produtos_fornecedor,
                                   form_oferecer=form_oferecer,
                                   categorias=categorias,
                                   dados_empresa=dados_empresa,
                                   value_utilizador=value_utilizador,
                                   mensagem=mensagem)
        else:
            return mensagem_interdito()
    return ir_fazer_login()


if __name__ == "__main__":
    app.run(debug=True)
