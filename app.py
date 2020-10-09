# _*_ coding: utf-8 _*_

from flask import Flask, redirect, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.util.langhelpers import bool_or_str

from admin.Admin import start_views
from config import app_active, app_config
from controller.Product import ProductController
from controller.User import UserController

config = app_config[app_active]


def create_app(config_name):
    app = Flask(__name__, template_folder="templates")
    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["FLASK_ADMIN_SWATCH"] = "paper"

    Bootstrap(app)

    db = SQLAlchemy(config.APP)
    start_views(app, db)

    db.init_app(app)

    @app.route("/")
    def index():
        return "Hello world!"

    # Login
    @app.route("/login")
    def login():
        return render_template('login.html',
                               message="Essa é uma mensagem que veio da rota")

    @app.route("/login", methods=["POST"])
    def login_post():
        user = UserController()
        email = request.form["email"]
        password = request.form["password"]
        result = user.login(email, password)

        if result:
            return redirect("/admin")
        else:
            return render_template(
                "login.html",
                data={"status": 401, "msg": "Dados incorretos", "type": None},
            )

    # Produtos
    @app.route("/product", methods=["POST"])
    def save_products():
        product = ProductController()
        result = product.save_product(request.form)
        message = "Inserido" if result else "Não inserido"

        return message

    @app.route('/product', methods=['PUT'])
    def update_products():
        product = ProductController()
        result = product.update_product(request.form)
        message = "Editado" if result else "Não editado"

        return message

    # Recuperação de senha
    @app.route("/recovery-password/")
    def recovery_password():
        return "Aqui entrará a tela de recuperar senha"

    @app.route("/recovery-password/", methods=["POST"])
    def send_recovery_password():
        user = UserController()
        result = user.recovery(request.form["email"])

        if result:
            return render_template(
                "recovery.html",
                data={
                    "status": 200,
                    "msg": "E-mail de recuperação enviado com sucesso",
                },
            )

        else:
            return render_template(
                "recovery.html",
                data={"status": 401, "msg": "Erro ao enviar o e-mail de recuperação"},
            )

    return app
