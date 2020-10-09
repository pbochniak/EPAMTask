import logging
import json
import sys
from pathlib import Path
from argparse import ArgumentParser
from converters import TESTS, CONVERTERS


class Unifier:
    def __init__(self):
        self._records = []

    def loadRecords(self, records_path):
        format_label = None
        with records_path.open(mode="r") as f:
            header = f.readline().strip().split(",")
            for label, test in TESTS.items():
                if test(header):
                    format_label = label
                    break
            else:
                logging.warning(
                    "unsupported CSV format %s found in: %s",
                    str(header),
                    str(records_path),
                )
                return
            for line in f.readlines():
                line = line.strip()
                try:
                    record = CONVERTERS[format_label](line.split(","))
                    self._records.append(record)
                except Exception as ex:
                    logging.warning(
                        "incorrect raw '%s' (reason: %s) found in: %s",
                        line,
                        str(ex),
                        str(records_path),
                    )
        self._records.sort(key=lambda k: k["date"])

    def getRecords(self, record_format):
        output = ""
        if record_format == "csv":
            output = "date,type,amount,from,to"
            for r in self._records:
                output += (
                    f"\n{r['date']},{r['type']},{r['amount']},{r['from']},{r['to']}"
                )
        elif record_format == "json":
            output = json.dumps(self._records)
        elif record_format == "xml":
            raise NotImplementedError("XML format not implemented yet")
        return output


def command_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--input",
        "-i",
        metavar="INPUT",
        help="Directory contains bank's reports in  CSV format",
    )
    parser.add_argument(
        "--output",
        "-o",
        metavar="OUTPUT",
        help="File contains unified reports in chosen format",
    )
    parser.add_argument(
        "--format",
        "-f",
        metavar="FORMAT",
        help="Output file format (default: csv, available: csv, json, xml)",
        default="csv",
        choices=["csv", "json", "xml"],
    )
    return parser.parse_args()


def main():
    args = command_parser()
    unifier = Unifier()
    for transactions_file in Path(args.input).iterdir():
        if transactions_file.suffix != ".csv":
            logging.warning("not CSV file found: %s", str(transactions_file))
            continue
        unifier.loadRecords(transactions_file)
    content = unifier.getRecords(args.format)
    with open(args.output, "w") as f:
        f.write(content)


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        logging.error(ex)
        sys.exit(1)
