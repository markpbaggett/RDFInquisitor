import requests
from rdflib import Graph, URIRef, RDFS
from rdflib.namespace import RDF, SKOS
import io
import mimetypes


class RDFInquistior:
    def __init__(self, uri: str):
        self.uri = uri
        self.content_type = "Unknown"
        self.rdf = ""
        self.graph = self.__process_rdf()

    def __process_rdf(self):
        headers = {
            "Accept": "text/turtle, application/turtle, application/x-turtle, application/json, text/json, text/n3,"
            "text/rdf+n3, application/rdf+n3, application/rdf+xml, application/n-triples"
        }
        r = requests.get(self.uri, headers=headers)
        self.content_type = self.__get_content_type(
            r.headers["Content-Type"].split(";")[0]
        )
        self.__check_if_valid(self.content_type)
        self.rdf = r.content.decode("utf-8")
        g = Graph()
        return g.parse(io.StringIO(self.rdf), format=self.content_type)

    @staticmethod
    def __get_content_type(content_type):
        return content_type.split(";")[0]

    @staticmethod
    def __check_if_valid(mime_type):
        if mime_type not in (
            "text/turtle",
            "application/turtle",
            "application/x-turtle",
            "application/json",
            "text/json",
            "text/n3",
            "text/rdf+n3",
            "application/rdf+n3",
            "application/rdf+xml",
            "application/n-triples",
        ):
            raise ValueError(
                f"This is not valid RDF! Check your URI. Mime type is {mime_type}."
            )

    def download_rdf(self, path):
        with open(f"{path}{mimetypes.guess_extension(self.content_type)}", "w") as rdf:
            rdf.write(self.rdf)

    def get_labels(self, subject=None):
        """Get labels from your graph.

        Accepts a subject and returns either all labels from a graph or labels related to a particular subject
        (if one is specified).

        Args:
            subject (str): Optional.  This is None by default, but should be the full URI of a subject as a string.

        Returns:
             list: A list of labels as rdflib.terms.

        Examples:
            >>> RDFInquistior("http://rightsstatements.org/vocab/InC/1.0/").get_labels()
            [rdflib.term.Literal('In Copyright', lang='en'), rdflib.term.Literal('Auteursrechtelijk beschermd',
            lang='nl'), rdflib.term.Literal('Kehtiv autoriõigus', lang='et'),
            rdflib.term.Literal('Autorių teisės saugomos', lang='lt'), rdflib.term.Literal('प्रतिलिप्यधिकार (कॉपीराइट) में',
            lang='hi'), rdflib.term.Literal('Objęty pełną ochroną prawnoautorską', lang='pl'),
            rdflib.term.Literal('Tekijänoikeuden piirissä', lang='fi'), rdflib.term.Literal('Underkastad upphovsrätt',
            lang='sv-fi'), rdflib.term.Literal("Protégé par le droit d'auteur", lang='fr'),
            rdflib.term.Literal('Urheberrechtsschutz', lang='de'), rdflib.term.Literal('Protegido por derecho de autor',
            lang='es')]

            >>> RDFInquistior("http://purl.org/dc/terms/valid").get_labels("http://purl.org/dc/terms/valid")
            [rdflib.term.Literal('Date Valid', lang='en')]

        """
        if subject is not None:
            subject = URIRef(subject)
        labels = []
        for s, p, o in self.graph.triples((subject, SKOS.prefLabel, None)):
            labels.append(o)
        for s, p, o in self.graph.triples((subject, RDFS.label, None)):
            labels.append(o)
        return labels

    def get_range(self, rdf_property=None):
        """Get range of properties from your graph.

        Accepts a RDF property and returns either all ranges in a graph or the ranges related to a property
        (if one is specified).

        Args:
            rdf_property (str): Optional. This is None by default, but should be the full URI of a property as a string.

        Returns:
             list: A list of ranges as strings.

        Examples:
            >>> RDFInquistior("http://purl.org/dc/terms/valid").get_range("http://purl.org/dc/terms/valid")
            ['http://www.w3.org/2000/01/rdf-schema#Literal']

        """
        if rdf_property is not None:
            rdf_property = URIRef(rdf_property)
        ranges = [
            str(o) for s, p, o in self.graph.triples((rdf_property, RDFS.range, None))
        ]
        return ranges


if __name__ == "__main__":
    print(
        RDFInquistior("http://purl.org/dc/terms/valid").get_range(
            "http://purl.org/dc/terms/valid"
        )
    )
