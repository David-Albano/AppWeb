**README - Product Management Application**

This application is a product management prototype with access through three types of users: Administrator, Provider and Customer. It is an e-commerce application, with a shopping cart (without the payment method option) and sales and purchase comparison charts. The application was developed in Python, using the Flask and SQLAlchemy libraries, and the Matplotlib library to generate graphs.

Have a look to the previews: [Previews](https://github.com/David-Albano/AppWeb/blob/main/Template%20App%20Manager.pdf)

** Requirements **
To run this application, you must have the following requirements installed:

- Python 3
- pip
- Flask
- SQLAlchemy
- Matplotlib
- Installation

Install the dependencies:

**Python Installation**
- To install Python on Windows operating systems, download the latest version from the official Python website: https://www.python.org/downloads/
- Run the downloaded installer file and follow the instructions on the screen. Be sure to select the option to add Python to your PATH during installation.
- Open a command terminal and check the installed Python version by running the command: python --version

**Pip Installation**
- pip ya should be installed along with Python. However, if you want to update it or have problems using it, you can install it manually.
- Download the get-pip.py file from the official website: https://pip.pypa.io/en/stable/installing/
- Open a command terminal, navigate to the carpet where the get-pip.py file was downloaded and execute the following command: python get-pip.py

**Installing Flask, SQLAlchemy and Matplotlib**
- In a command terminal, run the following command to install Flask:
  `pip install Flask`
- To install SQLAlchemy, run the following command:
  `pip install SQLAlchemy`
- To install Matplotlib, run the following command:
`pip install matplotlib`

Note: It may be necessary to add the sudo command at the beginning of each installation command if you are using a Linux or Mac operating system.

Run the application with the following command: `python app.py`
Access the application in your browser via the URL: http://127.0.0.1:5000/

**Use**
Upon accessing the application, you will be redirected to the login page. If you are an administrator, provider or customer already registered, you can login with your credentials. Otherwise, you will need to register before using the application.

When logging in, you will be redirected to the application's home page, where you can view the available products, add them to the shopping cart and view the sales and purchases graphs.

**Grades**:
- This web app does not have a 'responsive' design
- As this is a prototype application, payments are not supported and data is stored in a local development database.
- Make sure you have python and pip installed before trying to install dependencies.
