from flask import Flask, render_template, request, redirect, Blueprint

admin_controller = Blueprint('admin_controller', __name__, template_folder='templates')

@admin_controller.route("/test")
def test():
    return "hi"