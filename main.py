from flask import Flask, render_template, request, redirect
import util

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("main.html");

@app.route("/finish")
def finish():
    try:
        x_value = int(request.args.get('x'))
        y_value = int(request.args.get('y'))
    except:
        return redirect("/")

    if not util.valid_params(x_value, y_value):
        return redirect("/")

    return render_template("result.html", x_value=x_value, y_value=y_value)


if __name__ == "__main__":
    app.run(debug=True);

