from datetime import datetime


def test(header):
    return header == ["date_readable", "type", "euro", "cents", "to", "from"]


def convert(record):
    if len(record) != 6:
        raise ValueError(f"Record has incorrect length: {len(record)} (expected: 6)")
    return {
        "date": datetime.strptime(record[0], "%d %b %Y").strftime("%Y-%m-%d"),
        "type": record[1],
        "amount": float(record[2]) + float(record[3]) / 100,
        "from": int(record[4]),
        "to": int(record[5]),
    }
