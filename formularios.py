from wtforms import Form
from wtforms import StringField, PasswordField, EmailField, FloatField,IntegerField, TextAreaField
from flask_wtf import FlaskForm
from wtforms import validators


# Criação de formularios e as suas respetivas validações

class FormularioUtilizador(Form):
    nome = StringField('Nome (Cliente ou Empresa)', [validators.InputRequired()])
    telefone = IntegerField('Telefone (opcional)')
    email = EmailField('Email', [validators.InputRequired()])
    endereço = StringField('Endereço (opcional)')
    NIF = IntegerField('NIF', [validators.InputRequired()])
    contrasenha = PasswordField('Palavra-passe', [validators.length(min=7, max=12, message="Introduça uma 'contrasenha' de 7 a 12 carateres"),
                                                  validators.InputRequired()]
                                )


class FormularioLogin(Form):
    email = StringField('Email', [validators.InputRequired()])
    contrasenha = PasswordField('Palavra-passe', [validators.length(min=7, max=12, message="Introduça uma 'contrasenha' de 7 a 12 carateres"),
                                                  validators.InputRequired()]
                                )

class OferecerProduto(Form):
    descriçao = TextAreaField('Descrição do produto', [validators.InputRequired()])
    marca = StringField('Marca', [validators.InputRequired()])
    modelo = StringField('Modelo', [validators.InputRequired()])
    preço_compra = FloatField('Preço de compra', [validators.InputRequired()])
    IVA = IntegerField('IVA%', [validators.InputRequired()])
    desconto = FloatField('Desconto%', [validators.InputRequired()])
    referencia = StringField('Referência do produto', [validators.length(min=9, max=9, message="Introduça uma referencia de 9 carateres"),
                                                       validators.InputRequired()])
    stock = IntegerField('Stock', [validators.InputRequired()])
    quantidade = IntegerField('Quantidade')

class FiltrarDadosPorData(Form):
    dia = IntegerField('Dia')
    mes = IntegerField('Mês')
    ano = IntegerField('Ano')