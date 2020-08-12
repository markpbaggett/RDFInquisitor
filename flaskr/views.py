from flaskr import app
from flask import render_template, request, Markup
from inquisitor.question import RDFInquisitor
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers.rdf import TurtleLexer
from pygments.lexers.data import JsonLdLexer
from pygments.lexers.html import XmlLexer
from .forms import RDFLookup, LabelLookup, QueryProperties


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/lookup", methods=["GET", "POST"])
def lookup():
    form = RDFLookup(request.form)
    if request.method == "POST":
        code = RDFInquisitor(form.uri.data).flaskerize_rdf(
            form.subject.data, form.language.data
        )
        lexers = {
            "ttl": TurtleLexer(),
            "json-ld": JsonLdLexer(),
            "xml": XmlLexer(),
            "nt": TurtleLexer(),
        }
        results = highlight(
            code,
            lexers[form.language.data],
            HtmlFormatter(linenos=True, style="colorful", full=True),
        )
        return render_template("lookup.html", results=Markup(results), form=form)
    else:
        return render_template("lookup.html", form=form)


@app.route("/labels", methods=["GET", "POST"])
def labels():
    form = LabelLookup(request.form)
    if request.method == "POST":
        if form.language.data == "" or form.language.data is None:
            labels = RDFInquisitor(form.uri.data).get_labels()
            return render_template("labels.html", results=labels, form=form)
        else:
            labels = [
                RDFInquisitor(form.uri.data).get_label_by_language(
                    form.uri.data, form.language.data
                )
            ]
            return render_template("labels.html", results=labels, form=form)
    else:
        return render_template("labels.html", form=form)


@app.route("/ranges", methods=["GET", "POST"])
def ranges():
    form = QueryProperties(request.form)
    if request.method == "POST":
        if form.property.data:
            return render_template(
                "ranges.html",
                results=RDFInquisitor(form.uri.data).get_range(form.property.data),
                form=form,
            )
        else:
            return render_template(
                "ranges.html",
                results=RDFInquisitor(form.uri.data).get_range(),
                form=form,
            )
    else:
        return render_template("ranges.html", form=form)


@app.route("/domains", methods=["GET", "POST"])
def domains():
    form = QueryProperties(request.form)
    if request.method == "POST":
        if form.property.data:
            return render_template(
                "domains.html",
                results=RDFInquisitor(form.uri.data).get_range(form.property.data),
                form=form,
            )
        else:
            return render_template(
                "domains.html",
                results=RDFInquisitor(form.uri.data).get_range(),
                form=form,
            )
    else:
        return render_template("domains.html", form=form)


@app.route("/objects", methods=["GET", "POST"])
def objects():
    form = QueryProperties(request.form)
    if request.method == "POST":
        if form.property.data:
            return render_template(
                "objects.html",
                results=RDFInquisitor(form.uri.data).get_objects(
                    subject=form.uri.data, predicate=form.property.data
                ),
                form=form,
            )
        else:
            return render_template(
                "objects.html",
                results=RDFInquisitor(form.uri.data).get_objects(subject=form.uri.data),
                form=form,
            )
    else:
        return render_template("objects.html", form=form)

@app.route("/types", methods=["GET", "POST"])
def types():
    form = QueryProperties(request.form)
    if request.method == "POST":
        return render_template(
            "types.html",
            results=RDFInquisitor(form.uri.data).recurse_types(),
            form=form,
        )
    else:
        return render_template("types.html", form=form)
