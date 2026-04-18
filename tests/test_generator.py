import csv
import io
import re
from collections import Counter

from cases_faker import CaseGenerator, GeneratorConfig, list_schemas


def test_default_generates_requested_rows():
    rows = list(CaseGenerator(rows=50, seed=1))
    assert len(rows) == 50


def test_deterministic_given_seed():
    a = list(CaseGenerator(rows=20, seed=42))
    b = list(CaseGenerator(rows=20, seed=42))
    assert a == b


def test_different_seeds_diverge():
    a = list(CaseGenerator(rows=20, seed=1))
    b = list(CaseGenerator(rows=20, seed=2))
    assert a != b


def test_servicenow_schema_fields():
    gen = CaseGenerator(rows=5, seed=1, schema="servicenow")
    row = next(iter(gen))
    expected = {
        "number", "opened_at", "account", "sold_product", "short_description",
        "priority", "resolved_at", "assigned_to", "comments", "close_notes",
    }
    assert set(row.keys()) == expected


def test_zendesk_schema_fields():
    gen = CaseGenerator(rows=5, seed=1, schema="zendesk")
    row = next(iter(gen))
    expected = {
        "id", "created_at", "requester_organization", "subject",
        "priority", "solved_at", "assignee", "description", "comments", "tags",
    }
    assert set(row.keys()) == expected


def test_servicenow_comment_line_format():
    """cai's loader parses comments with this exact regex — contract-test it."""
    commenter_re = re.compile(
        r"(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}) - ([^\r\n(]+?) \(([^)]*)\)"
    )
    rows = list(CaseGenerator(rows=200, seed=7))
    non_empty = [r["comments"] for r in rows if r["comments"]]
    assert non_empty, "expected some tickets to have comments"
    matches = sum(1 for c in non_empty if commenter_re.search(c))
    assert matches == len(non_empty), "every non-empty comment must be parseable"


def test_priority_distribution_roughly_matches():
    rows = list(CaseGenerator(rows=5000, seed=3))
    dist = Counter(r["priority"] for r in rows)
    # "4 - Low" is weighted at 0.59 — expect it to dominate
    assert dist.most_common(1)[0][0] == "4 - Low"


def test_unknown_schema_raises():
    import pytest
    with pytest.raises(ValueError):
        CaseGenerator(rows=1, schema="madeup")


def test_list_schemas_returns_known():
    schemas = list_schemas()
    assert "servicenow" in schemas
    assert "zendesk" in schemas


def test_pool_override():
    cfg = GeneratorConfig(
        rows=30, seed=1,
        accounts=["OnlyThis"],
        products=["OnlyProduct"],
    )
    rows = list(CaseGenerator(cfg))
    assert all(r["account"] == "OnlyThis" for r in rows)
    assert all(r["sold_product"] == "OnlyProduct" for r in rows)


def test_cli_csv_roundtrip(tmp_path):
    from cases_faker.cli import main
    out = tmp_path / "out.csv"
    rc = main(["--rows", "10", "--seed", "1", "--out", str(out)])
    assert rc == 0
    with open(out, newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 10


def test_cli_stdout_csv(capsys):
    from cases_faker.cli import main
    rc = main(["--rows", "3", "--seed", "1", "--out", "-"])
    assert rc == 0
    captured = capsys.readouterr()
    reader = csv.reader(io.StringIO(captured.out))
    rows = list(reader)
    assert rows[0][0] == "number"  # header
    assert len(rows) == 4  # header + 3
