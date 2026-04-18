# cases-faker

Realistic synthetic helpdesk/support ticket data. Deterministic, schema-aware,
zero dependencies in the base install.

Built because every analytics / triage / ML-on-tickets project needs fake data
that actually looks like tickets — not `lorem ipsum` with a `priority` column.

## Install

```bash
pip install cases-faker
# Optional parquet output:
pip install 'cases-faker[parquet]'
```

## Quickstart

### Library

```python
from cases_faker import CaseGenerator

for case in CaseGenerator(rows=10, seed=42):
    print(case["number"], case["short_description"])
```

Deterministic given a seed. Returns an iterator of dicts — streams cleanly into
pandas, CSV writers, parquet, whatever.

### CLI

```bash
# 1000 ServiceNow-shaped tickets to CSV
cases-faker --rows 1000 --seed 42 --out tickets.csv

# Zendesk shape, JSONL, to stdout
cases-faker --schema zendesk --rows 500 --format jsonl --out -

# Parquet (requires the [parquet] extra)
cases-faker --rows 10000 --format parquet --out tickets.parquet
```

## What it generates

Multi-turn comments, realistic priority distributions, SLA-aware resolution
times, and close-note categories. Priority mix mirrors a real support queue
(low-priority dominates, criticals are rare).

Supported schemas:

- `servicenow` — customer-case shape: `number, opened_at, account, sold_product, short_description, priority, resolved_at, assigned_to, comments, close_notes`
- `zendesk` — ticket shape: `id, created_at, requester_organization, subject, priority, solved_at, assignee, description, comments, tags`

Comment threads use each platform's native format (ServiceNow's
`DD/MM/YYYY HH:MM:SS - Name (Channel)` lines, Zendesk's public/internal tags)
so you can unit-test parsers against them.

## Customising pools

Pass your own lists of accounts, products, assignees, etc:

```python
from cases_faker import CaseGenerator, GeneratorConfig

cfg = GeneratorConfig(
    rows=500,
    seed=1,
    accounts=["Acme", "Globex", "Initech"],
    short_descriptions=["Widget broken", "Widget on fire", "Widget missing"],
)
for case in CaseGenerator(cfg):
    ...
```

## Development

```bash
pip install -e '.[dev]'
pytest
```

## License

MIT.
# cases-faker
# cases-faker
# cases-faker
# cases-faker
# cases-faker
