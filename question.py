import requests


class QuestionRDF:
    def __init__(self, uri: str):
        self.uri = uri
        self.content_type = "Unknown"
        self.rdf = self.__get_rdf()

    def __get_rdf(self):
        headers = {
            "Accept": "text/turtle, application/turtle, application/x-turtle, application/json, text/json, text/n3,"
            "text/rdf+n3, application/rdf+n3, application/rdf+xml, application/n-triples"
        }
        r = requests.get(self.uri, headers=headers, verify=False)
        self.__check_if_valid(r.headers["Content-Type"])
        self.content_type = r.headers["Content-Type"]
        return r.content.decode("utf-8"), r.headers["Content-Type"]

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
            raise ValueError("This is not valid RDF! Check your URI.")


if __name__ == "__main__":
    x = QuestionRDF("http://rightsstatements.org/vocab/CNE/1.0/")
