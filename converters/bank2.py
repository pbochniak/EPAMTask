from datetime import datetime


def test(header):
    return header == ["date", "transaction", "amounts", "to", "from"]


def convert(record):
    if len(record) != 5:
        raise ValueError(f"Record has incorrect length: {len(record)} (expected: 5)")
    return {
        "date": datetime.strptime(record[0], "%d-%m-%Y").strftime("%Y-%m-%d"),
        "type": record[1],
        "amount": float(record[2]),
        "from": int(record[4]),
        "to": int(record[3]),
    }
