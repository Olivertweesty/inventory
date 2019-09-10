from flask import render_template
from . import routes

@routes.route('/pointofsale')
def pointofsale():
    return render_template("pos_main.html")