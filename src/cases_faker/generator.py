"""Core generator. Deterministic given a seed; iterable; schema-aware."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Iterator, Optional

from cases_faker import pools
from cases_faker.schemas import get_schema


@dataclass
class GeneratorConfig:
    rows: int = 1000
    schema: str = "servicenow"
    seed: Optional[int] = None
    days: int = 365
    end: Optional[datetime] = None

    # Optional pool overrides — pass your own lists to customise the output
    accounts: list[str] = field(default_factory=lambda: list(pools.ACCOUNTS))
    products: list[str] = field(default_factory=lambda: list(pools.PRODUCTS))
    assignees: list[str] = field(default_factory=lambda: list(pools.ASSIGNEES))
    short_descriptions: list[str] = field(
        default_factory=lambda: list(pools.SHORT_DESCRIPTIONS)
    )
    comment_snippets: list[str] = field(
        default_factory=lambda: list(pools.COMMENT_SNIPPETS)
    )
    resolution_methods: list[str] = field(
        default_factory=lambda: list(pools.RESOLUTION_METHODS)
    )


class CaseGenerator:
    """Iterable of synthetic case dicts in the requested schema.

    Example:
        >>> from cases_faker import CaseGenerator
        >>> gen = CaseGenerator(rows=100, seed=42)
        >>> cases = list(gen)
        >>> cases[0]["number"]
        'CS0100000'
    """

    def __init__(self, config: Optional[GeneratorConfig] = None, **kwargs):
        if config is None:
            config = GeneratorConfig(**kwargs)
        elif kwargs:
            raise ValueError("Pass either config or kwargs, not both.")
        self.config = config
        self.schema = get_schema(config.schema)
        self._rng = random.Random(config.seed)

    @property
    def fields(self) -> list[str]:
        return list(self.schema["fields"])

    def __iter__(self) -> Iterator[dict]:
        cfg = self.config
        end = cfg.end or datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)
        start = end - timedelta(days=cfg.days)
        for i in range(cfg.rows):
            yield self._generate_row(i, start, end)

    # ------------------------------------------------------------------
    # internals
    # ------------------------------------------------------------------

    def _weighted_priority(self) -> str:
        r = self._rng.random()
        cum = 0.0
        for value, weight in self.schema["priorities"]:
            cum += weight
            if r <= cum:
                return value
        return self.schema["priorities"][-1][0]

    def _random_dt(self, start: datetime, end: datetime) -> datetime:
        delta = end - start
        return start + timedelta(seconds=self._rng.randint(0, int(delta.total_seconds())))

    def _build_comments(self, opened: datetime, resolved: Optional[datetime]) -> str:
        if resolved is None:
            resolved = opened + timedelta(hours=self._rng.randint(1, 72))
        n = self._rng.choices([0, 1, 2, 3, 4, 5], weights=[10, 25, 30, 20, 10, 5])[0]
        if n == 0:
            return ""

        parts: list[str] = []
        current = opened + timedelta(minutes=self._rng.randint(5, 120))
        window = max((resolved - current).total_seconds(), 60)
        step_max = max(window / max(n, 1), 600)

        for _ in range(n):
            ts = current.strftime(self.schema["timestamp_format"])
            who = self._rng.choice(self.config.assignees)
            channel = self._rng.choice(self.schema["comment_channels"])
            body = self._rng.choice(self.config.comment_snippets)
            parts.append(
                self.schema["comment_line_format"].format(
                    ts=ts, who=who, channel=channel, body=body
                )
            )
            current += timedelta(seconds=self._rng.randint(600, int(step_max) or 600))
            if current >= resolved:
                break

        return self.schema["comment_separator"].join(parts)

    def _generate_row(self, idx: int, start: datetime, end: datetime) -> dict:
        cfg = self.config
        schema = self.schema

        opened = self._random_dt(start, end)
        priority = self._weighted_priority()

        if self._rng.random() < schema["resolution_rate"]:
            lo, hi = schema["sla_hours"].get(priority, (24, 168))
            hours = self._rng.uniform(lo, hi)
            resolved = opened + timedelta(hours=hours)
            if resolved > end + timedelta(days=14):
                resolved = None
        else:
            resolved = None

        close_notes = self._rng.choice(cfg.resolution_methods) if resolved else ""

        number = (
            f"{schema['number_prefix']}{idx:0{schema['number_width']}d}"
            if schema["number_width"]
            else str(idx + 1)
        )

        ts_fmt = schema["timestamp_format"]
        row_common = {
            "opened_at": opened.strftime(ts_fmt),
            "resolved_at": resolved.strftime(ts_fmt) if resolved else "",
            "priority": priority,
            "account": self._rng.choice(cfg.accounts),
            "sold_product": self._rng.choice(cfg.products),
            "short_description": self._rng.choice(cfg.short_descriptions),
            "assigned_to": self._rng.choice(cfg.assignees),
            "comments": self._build_comments(opened, resolved),
            "close_notes": close_notes,
        }

        if schema["name"] == "servicenow":
            return {
                "number": number,
                "opened_at": row_common["opened_at"],
                "account": row_common["account"],
                "sold_product": row_common["sold_product"],
                "short_description": row_common["short_description"],
                "priority": row_common["priority"],
                "resolved_at": row_common["resolved_at"],
                "assigned_to": row_common["assigned_to"],
                "comments": row_common["comments"],
                "close_notes": row_common["close_notes"],
            }

        if schema["name"] == "zendesk":
            return {
                "id": idx + 1,
                "created_at": row_common["opened_at"],
                "requester_organization": row_common["account"],
                "subject": row_common["short_description"],
                "priority": row_common["priority"],
                "solved_at": row_common["resolved_at"],
                "assignee": row_common["assigned_to"],
                "description": row_common["short_description"],
                "comments": row_common["comments"],
                "tags": ",".join(self._rng.sample(
                    ["auth", "api", "performance", "email", "ui", "data", "integration"],
                    k=self._rng.randint(1, 3),
                )),
            }

        raise ValueError(f"Unhandled schema {schema['name']!r}")
