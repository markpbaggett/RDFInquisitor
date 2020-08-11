from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, URL


class RDFLookup(FlaskForm):
    uri = StringField("uri", validators=[URL()])
    subject = StringField("subject")
    language = SelectField(
        u"Choose language",
        choices=[
            ("ttl", "ttl"),
            ("xml", "rdf/xml"),
            ("json-ld", "json-ld"),
            ("nt", "ntriples"),
        ],
        validators=[DataRequired()],
    )


class LabelLookup(FlaskForm):
    uri = StringField("uri", validators=[URL()])
    language = StringField("language")

