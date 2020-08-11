from flaskr import app
from flask import render_template, request, Markup
from inquisitor.question import RDFInquisitor
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers.rdf import TurtleLexer
from .forms import MyInputBox


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = MyInputBox(request.form)
    if request.method == 'POST':
        #print(form.language.data)
        print(form.subject.data)
        code = RDFInquisitor(form.uri.data).flaskerize_rdf(form.language.data)
        results = highlight(code, TurtleLexer(), HtmlFormatter(linenos=True, style="colorful", full=True))
        return render_template('test.html', results=Markup(results), form=form)
    else:
        return render_template("test.html", form=form)
