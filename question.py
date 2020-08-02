import requests
from rdflib import Graph, URIRef, RDFS
from rdflib.namespace import RDF, SKOS
import io


class RDFInquistior:
    def __init__(self, uri: str):
        self.uri = uri
        self.content_type = "Unknown"
        self.rdf_string = ""
        self.rdf = self.__process_rdf()

    def __process_rdf(self):
        headers = {
            "Accept": "text/turtle, application/turtle, application/x-turtle, application/json, text/json, text/n3,"
            "text/rdf+n3, application/rdf+n3, application/rdf+xml, application/n-triples"
        }
        r = requests.get(self.uri, headers=headers, verify=False)
        self.content_type = self.__get_content_type(
            r.headers["Content-Type"].split(";")[0]
        )
        self.__check_if_valid(self.content_type)
        self.rdf_string = r.content.decode("utf-8")
        g = Graph()
        return g.parse(io.StringIO(self.rdf_string), format=self.content_type)

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

    def get_labels(self, subject=None):
        """Returns all labels or labels related to a particular subject for your RDF."""
        if subject is not None:
            subject = URIRef(subject)
        labels = []
        for s, p, o in self.rdf.triples((subject, SKOS.prefLabel, None)):
            labels.append(o)
        for s, p, o in self.rdf.triples((subject, RDFS.label, None)):
            labels.append(o)
        return labels

    # def get_range(self, subject=None):


if __name__ == "__main__":
    x = RDFInquistior("http://rightsstatements.org/vocab/CNE/1.0/")
    print(x.get_labels("http://rightsstatements.org/vocab/CNE/1.0/"))
