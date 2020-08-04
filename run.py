from inquisitor.question import RDFInquisitor
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Question your Remote RDF")
    parser.add_argument(
        "-u", "--uri", dest="uri", help="URI to negotiate", required=True
    )
    parser.add_argument(
        "-o",
        "--operation",
        dest="operation",
        help="Operation you want to run: download_rdf, get_labels, get_label_by_lang, get_types, get_range",
        required=True,
    )
    parser.add_argument(
        "-f",
        "--file_format",
        dest="file_format",
        help="When downloading rdf, specify how you want to serialize things.",
        default="ttl",
    )
    parser.add_argument(
        "-p",
        "--file_path",
        dest="file_path",
        help="When downloading rdf, where you want to serialize to disk without extension",
        default="rdf",
    )
    parser.add_argument(
        "-s",
        "--subject",
        dest="subject",
        help="Specify a subject.  See docs for details.",
    )
    parser.add_argument(
        "-x", "--extra", dest="extra", help="Specify an extra.  See docs for details."
    )
    args = parser.parse_args()

    x = RDFInquisitor(args.uri)
    if args.operation == "download_rdf":
        print(x.download_rdf(args.file_path, args.file_format))
    elif args.operation == "get_labels":
        if args.subject is not None:
            print(x.get_labels(args.subject))
        else:
            print(x.get_labels())
    elif args.operation == "get_label_by_lang":
        if args.extra is not None:
            print(x.get_label_by_language(args.subject, args.extra))
        else:
            print(x.get_label_by_language(args.subject, "en"))
    elif args.operation == "get_range":
        if args.extra is not None:
            print(x.get_range(args.extra))
        else:
            print(x.get_range())
    elif args.operation == "get_types":
        if args.extra is not None:
            print(x.get_types(args.extra))
        else:
            print(x.get_types())
    else:
        print("Operation not valid.")
