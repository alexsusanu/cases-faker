"""ServiceNow customer-case shape."""

SERVICENOW = {
    "name": "servicenow",
    "fields": [
        "number", "opened_at", "account", "sold_product", "short_description",
        "priority", "resolved_at", "assigned_to", "comments", "close_notes",
    ],
    "number_prefix": "CS",
    "number_width": 7,
    "timestamp_format": "%d/%m/%Y %H:%M:%S",
    "priorities": [
        ("4 - Low", 0.59),
        ("5 - Other", 0.17),
        ("3 - Moderate", 0.13),
        ("2 - Major", 0.08),
        ("1 - System Down", 0.02),
        ("1 - Critical", 0.01),
    ],
    "sla_hours": {
        "1 - Critical": (1, 8),
        "1 - System Down": (1, 12),
        "2 - Major": (4, 48),
        "3 - Moderate": (8, 120),
        "4 - Low": (24, 240),
        "5 - Other": (24, 360),
    },
    "resolution_rate": 0.85,
    "comment_channels": ["Additional comments", "Work notes", "Customer visible"],
    # Line shape: "DD/MM/YYYY HH:MM:SS - Name (Channel)\n<body>"
    "comment_line_format": "{ts} - {who} ({channel})\n{body}",
    "comment_separator": "\n\n",
}
