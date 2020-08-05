import requests
from rdflib import Graph, URIRef, RDFS, Literal
from rdflib.namespace import RDF, SKOS


class RDFInquisitor:
    def __init__(self, uri: str):
        self.uri = uri
        self._response = self.__request_data()
        self.content_type = self.__get_content_type(
            self._response.headers["Content-Type"].split(";")[0]
        )
        self._valid = self.__check_if_valid(self.content_type)
        self.rdf = self._response.content.decode("utf-8")
        self.graph = self.__process_rdf()

    def __request_data(self):
        headers = {
            "Accept": "text/turtle, application/turtle, application/x-turtle, application/json, text/json, text/n3,"
            "text/rdf+n3, application/rdf+n3, application/rdf+xml, application/n-triples"
        }
        return requests.get(self.uri, headers=headers)

    def __process_rdf(self):
        if "json" in self.content_type:
            return Graph().parse(data=self.rdf, format="json-ld")
        else:
            return Graph().parse(data=self.rdf, format=self.content_type)

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
        return True

    @staticmethod
    def __convert_fragment(fragment):
        if fragment is None:
            return fragment
        elif fragment.startswith("http"):
            return URIRef(fragment)
        else:
            return Literal(fragment)

    def __get_objects(self, subject=None, predicate=None):
        return [
            o
            for s, p, o in self.graph.triples(
                self.__convert_fragment(subject), predicate, None
            )
        ]

    def download_rdf(self, path, file_format="ttl"):
        """Download the negotiated RDF to a specific path.

        Requires a path and serializes the negotiated RDF from a web server to disk.

        Args:
            path (str): Required.  The path with filename (no extension) for where to serialize your file.
            file_format (str): Optional. The format you want to serialize your rdf as (ttl, xml, json-ld, nt).

        Returns:
            str: A message stating where the file was serialized.

        Example:
            >>> RDFInquisitor("http://rightsstatements.org/vocab/InC/1.0/").download_rdf("../rdf/InC")
            'File was successfully serialized as ../rdf/InC.ttl'

            >>> RDFInquisitor("http://rightsstatements.org/vocab/InC/1.0/").download_rdf("../rdf/InC", "ttl")
            'File was successfully serialized as ../rdf/InC.ttl'

            >>> RDFInquisitor("http://rightsstatements.org/vocab/InC/1.0/").download_rdf("../rdf/InC", "json-ld")
            'File was successfully serialized as ../rdf/InC.json-ld'

            >>> RDFInquisitor("http://rightsstatements.org/vocab/InC/1.0/").download_rdf("../rdf/InC", "xml")
            'File was successfully serialized as ../rdf/InC.xml'

            >>> RDFInquisitor("http://rightsstatements.org/vocab/InC/1.0/").download_rdf("../rdf/InC", "nt")
            'File was successfully serialized as ../rdf/InC.nt'

        """
        with open(f"{path}.{file_format}", "wb") as rdf:
            rdf.write(self.graph.serialize(format=file_format, indent=4))
        return f"File was successfully serialized as {path}.{file_format}"

    def get_label_by_language(self, subject, language_tag):
        """Get the label of a subject in a specific language.

        Requires a subject and a language code and returns the label in that language or a message saying the label in
        that language could not be found.

        Args:
            subject (str): The URI of the subject being queried.
            language_tag (str): The IETF language tag for the label.

        Returns:
            str: Either the label or a message indicating that no label could be found.

        Examples:
            >>> RDFInquisitor("http://rightsstatements.org/vocab/InC/1.0/").get_label_by_language(
            ... "http://rightsstatements.org/vocab/InC/1.0/", "en")
            'In Copyright'

            >>> RDFInquisitor("http://rightsstatements.org/vocab/InC/1.0/").get_label_by_language(
            ... "http://rightsstatements.org/vocab/InC/1.0/", "ja")
            'No label for http://rightsstatements.org/vocab/InC/1.0/ in ja.'

        """
        result = f"No label for {subject} in {language_tag}."
        labels = self.get_labels(subject)
        for label in labels:
            if label.language == language_tag:
                result = str(label)
        return result

    def get_labels(self, subject=None):
        """Get a list of labels from your graph.

        Accepts a subject and returns either all labels from a graph or labels related to a particular subject
        (if one is specified).

        Args:
            subject (str): Optional.  This is None by default, but should be the full URI of a subject as a string.

        Returns:
             list: A list of labels as rdflib.terms.

        Examples:
            >>> RDFInquisitor("http://rightsstatements.org/vocab/InC/1.0/").get_labels()
            [rdflib.term.Literal('In Copyright', lang='en'), rdflib.term.Literal('Auteursrechtelijk beschermd',
            lang='nl'), rdflib.term.Literal('Kehtiv autoriõigus', lang='et'),
            rdflib.term.Literal('Autorių teisės saugomos', lang='lt'), rdflib.term.Literal('प्रतिलिप्यधिकार (कॉपीराइट) में',
            lang='hi'), rdflib.term.Literal('Objęty pełną ochroną prawnoautorską', lang='pl'),
            rdflib.term.Literal('Tekijänoikeuden piirissä', lang='fi'), rdflib.term.Literal('Underkastad upphovsrätt',
            lang='sv-fi'), rdflib.term.Literal("Protégé par le droit d'auteur", lang='fr'),
            rdflib.term.Literal('Urheberrechtsschutz', lang='de'), rdflib.term.Literal('Protegido por derecho de autor',
            lang='es')]

            >>> RDFInquisitor("http://purl.org/dc/terms/valid").get_labels("http://purl.org/dc/terms/valid")
            [rdflib.term.Literal('Date Valid', lang='en')]

        """
        labels = []
        for s, p, o in self.graph.triples(
            (self.__convert_fragment(subject), SKOS.prefLabel, None)
        ):
            labels.append(o)
        for s, p, o in self.graph.triples(
            (self.__convert_fragment(subject), RDFS.label, None)
        ):
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
            >>> RDFInquisitor("http://purl.org/dc/terms/valid").get_range("http://purl.org/dc/terms/valid")
            ['http://www.w3.org/2000/01/rdf-schema#Literal']

            >>> RDFInquisitor("http://www.w3.org/2004/02/skos/core#inScheme").get_range(
            ... "http://www.w3.org/2004/02/skos/core#inScheme")
            ['http://www.w3.org/2004/02/skos/core#ConceptScheme']

            >>> RDFInquisitor("http://id.loc.gov/ontologies/bibframe/grantingInstitution").get_range()
            ['http://id.loc.gov/ontologies/bibframe/Agent']

        """
        return [
            str(o)
            for s, p, o in self.graph.triples(
                (self.__convert_fragment(rdf_property), RDFS.range, None)
            )
        ]

    def get_types(self, rdf_class=None):
        """State the type of a particular RDF class.

        Accepts a RDF class and returns either all types in a graph or the types associated with the specified class.

        Args:
            rdf_class (str): Optional. This is None by default, but should be the full URI of a class as a string.

        Returns:
            list: A list of types as URI strings.

        Example:
            >>> RDFInquisitor("http://rightsstatements.org/vocab/InC/1.0/").get_types()
            ['http://purl.org/dc/terms/RightsStatement', 'http://www.w3.org/2004/02/skos/core#Concept']

        """
        return [
            str(o)
            for s, p, o in self.graph.triples(
                (self.__convert_fragment(rdf_class), RDF.type, None)
            )
        ]

    def serialize_fragment(self, path, subject="", file_format="ttl"):
        """Serialize to disk a RDF fragment.

        While download_rdf() downloads the entire RDF negotiated from a web server, this method serializes a particular
        fragment.  This can be useful when you're working with an ontology that uses Fragment Identifiers.

        Todo: If the fragment contains blank nodes, the content of the nodes are returned empty.

        Args:
             subject (str): The subject URI that you want to serialize.
             path (str):  The place on disk you want to serialize things (without extension).
             file_format (str): The format you want to serialize in. Defaults to ttl.

        Returns:
            str: A message stating where the file was serialized.

        Examples:
            >>> RDFInquisitor("http://purl.org/dc/terms/modified").serialize_fragment("../rdf/modified",
            ... "http://purl.org/dc/terms/modified", "ttl")
            'File was successfully serialized as ../rdf/modified.ttl'

            >>> RDFInquisitor("http://id.loc.gov/authorities/names/no2018075117").serialize_fragment(
            ... "../rdf/thompson", "http://id.loc.gov/authorities/names/no2018075117", "ttl")
            'File was successfully serialized as ../rdf/thompson.ttl'

        """
        if subject == "":
            subject = self.uri
        test_fragment = [
            (s, p, o)
            for s, p, o in self.graph.triples(
                (self.__convert_fragment(subject), None, None)
            )
        ]
        g = Graph()
        for fragment in test_fragment:
            g.add(fragment)
        with open(f"{path}.{file_format}", "wb") as rdf:
            rdf.write(g.serialize(format=file_format, indent=4))
        return f"File was successfully serialized as {path}.{file_format}"

    def get_domain(self, rdf_property):
        """Returns the domain of a property if one exists.

        Requires an RDF property and returns a list of domains if they exist.

        Args:
            rdf_property (str): The full URI of your RDF property.

        Returns:
            list: A list of domains as URI strings.

        """
        return [
            str(o)
            for s, p, o in self.graph.triples(
                (self.__convert_fragment(rdf_property), RDFS.domain, None)
            )
        ]

    def recurse_types(self, _starting_types=None):
        """Get the types of a class and the types it inherits.

        Recursively pull back all inherited types for the subject of a piece of RDF.

        Returns:
            list: A list of all inherited types.

        Example:
            >>> RDFInquisitor("http://rightsstatements.org/vocab/InC/1.0/").recurse_types()
            ['http://www.w3.org/2004/02/skos/core#Concept', 'http://www.w3.org/2002/07/owl#Class',
            'http://www.w3.org/2000/01/rdf-schema#Class', 'http://purl.org/dc/terms/RightsStatement']

        """
        if _starting_types is None:
            all_types = []
        else:
            all_types = _starting_types
        initial_types = RDFInquisitor(self.uri).get_types(self.uri)
        for unique in initial_types:
            if unique not in all_types:
                all_types.append(unique)
                RDFInquisitor(unique).recurse_types(all_types)
        return all_types


if __name__ == "__main__":
    import doctest

    doctest.testmod()
