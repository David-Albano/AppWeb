from app import *

categorias = [
                ["TV,V,S", "TV, Vídeo e Som"],
                ["FOTO", "Fotografia"],
                ["SP", "Smartphones"],
                ["DESK", "Desktop"],
                ["G", "Gaming"],
                ["I&A", "Informática e Acessórios"]
            ]


def ir_fazer_login():
    return render_template('mensagem_login.html')

def mensagem_interdito():
    return render_template('interdito.html')


def ler_cookie():
    # Obtemos e devolvemos os valores das cookies
    email = request.cookies.get('email', 'Undefined')
    value_utilizador = request.cookies.get('tipo_de_utilizador', 'Undefined')
    cookies = {
        'email': email,
        'value_utilizador': value_utilizador
    }
    return cookies

def iniciar_sessao(usuario, template, contrasenha, value_utilizador, form_login, form_utilizadores, produtos):
    if usuario:
        # Conferimos dados de login
        if usuario.contrasenha == contrasenha:
            mensagem_login="O inicio de sessão foi efetuado com sucesso"
            resposta = make_response(render_template(template,
                                                 value_utilizador=value_utilizador,
                                                 form_login=form_login,
                                                 produtos=produtos,
                                                 categorias=categorias,
                                                 mensagem_login=mensagem_login))

            # Criação de cookies com os dados do login
            resposta.set_cookie('email', usuario.email)
            resposta.set_cookie('tipo_de_utilizador', value_utilizador)
            # Definimos uma sessão para o utilizador
            session['email'] = usuario.email
            session['value_utilizador'] = value_utilizador
            # Obtemos cookies
            ler_cookie()
            return resposta
        else:
            mensagem="Palavra-passe incorreta"
            return render_template('login.html',
                                   form_login=form_login,
                                   form_utilizadores=form_utilizadores,
                                   value_utilizador=value_utilizador,
                                   mensagem=mensagem)
    else:
        mensagem = "Email incorreto ou inexistente. Tente novamente"
        return render_template('login.html',
                               form_login=form_login,
                               form_utilizadores=form_utilizadores,
                               value_utilizador=value_utilizador,
                               mensagem=mensagem)

def mostrar_dados_de_compra_e_venda(query, titulo):
    registos = query
    datas = []
    valor = []

    # Definimos os dados para os gráficos
    for registo in registos:
        data = "{}/{}/{}".format(registo.dia, registo.mes, registo.ano)
        datas.append(data + "-" + registo.hora)
        valor.append(registo.valor_total)

    grafico = {
        'x': datas,
        'y': valor
    }

    # Personalizamos os gráficos
    plt.plot(datas, valor, 'r--o', c='green')
    plt.legend(["€ Euros vs Data/Hora"])
    plt.xlabel('Data da transação', c='blue')
    plt.xticks(rotation=30)
    plt.ylabel('Valor de transação', c='green')
    plt.grid(b=True)
    plt.title(titulo)
    plt.tight_layout()

    return grafico