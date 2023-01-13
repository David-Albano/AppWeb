**README - Aplicação de Gestão de Produtos**

Esta aplicação é um protótipo de gestão de produtos com acesso através de três tipos de utilizadores: Administrador, Provedor e Cliente. É uma aplicação de e-commerce, com carrinho de compras (sem a opção de método de pagamento) e gráficos de comparação de vendas e compras. A aplicação foi desenvolvida em Python, utilizando as bibliotecas Flask e SQLAlchemy, e a biblioteca Matplotlib para gerar gráficos.

**Requisitos**
Para executar esta aplicação, é necessário ter os seguintes requisitos instalados:

- Python 3
- pip
- Flask
- SQLAlchemy
- Matplotlib
- Instalação

Instale as dependências:

**Instalação de Python**
- Para instalar Python en sistemas operativos Windows, descargue la última versión en el sitio web oficial de Python: https://www.python.org/downloads/
- Ejecute el archivo de instalador descargado y siga las instrucciones en pantalla. Asegúrese de seleccionar la opción de agregar Python a su PATH durante la instalación.
- Abra una terminal de comandos y verifique la versión de Python instalada ejecutando el comando: python --version

**Instalação de pip**
- pip ya debería estar instalado junto con Python. Sin embargo, si desea actualizarlo o tiene problemas para utilizarlo, puede instalarlo manualmente.
- Descargue el archivo get-pip.py desde el sitio web oficial: https://pip.pypa.io/en/stable/installing/
- Abra una terminal de comandos, navegue hasta la carpeta donde se descargó el archivo get-pip.py y ejecute el siguiente comando: python get-pip.py

**Instalando Flask, SQLAlchemy y Matplotlib**
- En una terminal de comandos, ejecute el siguiente comando para instalar Flask:
 `pip install Flask`
- Para instalar SQLAlchemy, ejecute el siguiente comando:
 `pip install SQLAlchemy`
- Para instalar Matplotlib, ejecute el siguiente comando: 
`pip install matplotlib`

Nota: Puede ser necesario agregar el comando sudo al principio de cada comando de instalación si está utilizando un sistema operativo Linux o Mac.

**Inicie o servidor de desenvolvimento:**
python app.py
Acesse a aplicação em seu navegador através da URL: http://127.0.0.1:5000/

**Utilização**
Ao acessar a aplicação, você será redirecionado para a página de login. Se você for um administrador, provedor ou cliente já cadastrado, poderá fazer login com suas credenciais. Caso contrário, será necessário se cadastrar antes de usar a aplicação

Ao fazer login, você será redirecionado para a página inicial da aplicação, onde poderá visualizar os produtos disponíveis, adicioná-los ao carrinho de compras e visualizar os gráficos de vendas e compras.

**Notas**:
- Esta app web não tem desenho 'responsive'
- Como esta é uma aplicação protótipo, não há suporte para pagamentos e os dados são armazenados em um banco de dados de desenvolvimento local.
- Certifique-se de ter o python e pip instalado antes de tentar instalar as dependências.
