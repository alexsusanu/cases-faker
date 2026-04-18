"""Zendesk ticket shape. Flatter than ServiceNow — fewer fields, simpler priority."""

ZENDESK = {
    "name": "zendesk",
    "fields": [
        "id", "created_at", "requester_organization", "subject",
        "priority", "solved_at", "assignee", "description", "comments", "tags",
    ],
    "number_prefix": "",
    "number_width": 0,
    "timestamp_format": "%Y-%m-%dT%H:%M:%SZ",
    "priorities": [
        ("low", 0.50),
        ("normal", 0.30),
        ("high", 0.15),
        ("urgent", 0.05),
    ],
    "sla_hours": {
        "urgent": (1, 8),
        "high": (4, 24),
        "normal": (8, 72),
        "low": (24, 168),
    },
    "resolution_rate": 0.90,
    "comment_channels": ["public", "internal"],
    # Zendesk-style public/internal comments
    "comment_line_format": "[{ts}] {who} ({channel}): {body}",
    "comment_separator": "\n",
}
