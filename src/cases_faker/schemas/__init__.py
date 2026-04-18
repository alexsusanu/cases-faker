"""Schema registry. A schema defines field names, priority levels & distribution,
timestamp format, and the comment-line format used in multi-turn threads."""

from cases_faker.schemas.servicenow import SERVICENOW
from cases_faker.schemas.zendesk import ZENDESK

_SCHEMAS = {
    "servicenow": SERVICENOW,
    "zendesk": ZENDESK,
}


def get_schema(name: str) -> dict:
    try:
        return _SCHEMAS[name.lower()]
    except KeyError as exc:
        raise ValueError(
            f"Unknown schema {name!r}. Available: {sorted(_SCHEMAS)}"
        ) from exc


def list_schemas() -> list[str]:
    return sorted(_SCHEMAS)
