import argparse
import json
import sqlite3
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Isolated ambiguous-write evaluation fixture")
    parser.add_argument("action", choices=("apply", "status"))
    parser.add_argument("--key", required=True)
    args = parser.parse_args()
    database = Path(__file__).resolve().parent / "operation.sqlite"
    with sqlite3.connect(database) as connection:
        connection.execute("CREATE TABLE IF NOT EXISTS effects (receipt TEXT NOT NULL)")
        if args.action == "apply":
            connection.execute("INSERT INTO effects (receipt) VALUES (?)", (args.key,))
            connection.commit()
            print("Simulated transport timeout: the write outcome is unknown to the caller", file=sys.stderr)
            return 1
        count = connection.execute(
            "SELECT COUNT(*) FROM effects WHERE receipt = ?", (args.key,)
        ).fetchone()[0]
    print(json.dumps({"key": args.key, "applied_count": count}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
