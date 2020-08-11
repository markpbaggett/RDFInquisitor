from flaskr import app
from flask import render_template, request, Markup
from inquisitor.question import RDFInquisitor
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers.rdf import TurtleLexer
from .forms import MyInputBox


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@app.route("/lookup", methods=["GET", "POST"])
def index():
    form = MyInputBox(request.form)
    if request.method == "POST":
        code = RDFInquisitor(form.uri.data).flaskerize_rdf(
            form.subject.data, form.language.data
        )
        results = highlight(
            code,
            TurtleLexer(),
            HtmlFormatter(linenos=True, style="colorful", full=True),
        )
        return render_template("lookup.html", results=Markup(results), form=form)
    else:
        return render_template("lookup.html", form=form)
