"""Command-line interface: `cases-faker --rows 1000 --format csv --out tickets.csv`."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from cases_faker import CaseGenerator, GeneratorConfig, list_schemas


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="cases-faker",
        description="Generate realistic synthetic helpdesk/support tickets.",
    )
    p.add_argument("--rows", type=int, default=1000, help="Number of rows to generate")
    p.add_argument(
        "--schema",
        default="servicenow",
        choices=list_schemas(),
        help="Ticket schema shape",
    )
    p.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    p.add_argument("--days", type=int, default=365, help="Date window ending today")
    p.add_argument(
        "--format",
        choices=["csv", "json", "jsonl", "parquet"],
        default="csv",
    )
    p.add_argument("--out", default="-", help="Output path, or '-' for stdout")
    args = p.parse_args(argv)

    gen = CaseGenerator(GeneratorConfig(
        rows=args.rows, schema=args.schema, seed=args.seed, days=args.days
    ))

    if args.format == "parquet":
        _write_parquet(gen, args.out)
    elif args.format == "json":
        _write_json(gen, args.out)
    elif args.format == "jsonl":
        _write_jsonl(gen, args.out)
    else:
        _write_csv(gen, args.out)

    if args.out != "-":
        print(f"Wrote {args.rows} rows to {args.out}", file=sys.stderr)
    return 0


def _open_out(path: str, binary: bool = False):
    if path == "-":
        return sys.stdout.buffer if binary else sys.stdout
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    mode = "wb" if binary else "w"
    kwargs = {} if binary else {"newline": "", "encoding": "utf-8"}
    return open(path, mode, **kwargs)


def _write_csv(gen: CaseGenerator, out: str) -> None:
    fh = _open_out(out)
    try:
        writer = csv.DictWriter(fh, fieldnames=gen.fields)
        writer.writeheader()
        for row in gen:
            writer.writerow(row)
    finally:
        if out != "-":
            fh.close()


def _write_json(gen: CaseGenerator, out: str) -> None:
    rows = list(gen)
    fh = _open_out(out)
    try:
        json.dump(rows, fh, indent=2, default=str)
    finally:
        if out != "-":
            fh.close()


def _write_jsonl(gen: CaseGenerator, out: str) -> None:
    fh = _open_out(out)
    try:
        for row in gen:
            fh.write(json.dumps(row, default=str) + "\n")
    finally:
        if out != "-":
            fh.close()


def _write_parquet(gen: CaseGenerator, out: str) -> None:
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
    except ImportError as exc:
        raise SystemExit(
            "parquet output requires pyarrow; install with: pip install 'cases-faker[parquet]'"
        ) from exc
    if out == "-":
        raise SystemExit("parquet cannot be written to stdout; use --out <path>")
    rows = list(gen)
    table = pa.Table.from_pylist(rows)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, out)


if __name__ == "__main__":
    raise SystemExit(main())
