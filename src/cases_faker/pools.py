"""Pools of realistic-looking strings used when a schema doesn't override them."""

ACCOUNTS = [
    "Acme Corp", "Globex", "Initech", "Umbrella Labs", "Hooli",
    "Massive Dynamic", "Soylent", "Stark Industries", "Wayne Enterprises",
    "Wonka Industries", "Tyrell Corp", "Cyberdyne", "Pied Piper",
    "Vandelay Industries", "Dunder Mifflin", "Los Pollos", "Bluth Company",
    "Oscorp", "Gringotts", "Aperture Science", "Black Mesa", "InGen",
    "Nakatomi Trading", "Rekall", "Weyland-Yutani",
]

PRODUCTS = [
    "Platform Core", "Analytics Module", "Reporting Service",
    "Integration Gateway", "Notification Engine", "Mobile Client",
    "Admin Console", "API Gateway",
]

ASSIGNEES = [
    "A. Morgan", "B. Patel", "C. Nguyen", "D. Rossi", "E. Kowalski",
    "F. Hernandez", "G. Tanaka", "H. Schmidt", "I. Andersson", "J. O'Brien",
    "K. Dubois", "L. Silva", "M. Yilmaz", "N. Johansson", "O. Ahmed",
]

SHORT_DESCRIPTIONS = [
    "Login fails intermittently for a subset of users",
    "Scheduled report arrives empty",
    "API returning 500 on bulk endpoint",
    "Email notifications not delivered",
    "Dashboard loads slowly after upgrade",
    "User cannot reset password via SSO",
    "Export to CSV produces corrupted file",
    "Background job stuck in running state",
    "Audit log missing entries for last week",
    "Webhook deliveries failing with 401",
    "File upload fails for files over 10MB",
    "Search results incomplete for certain filters",
    "Timezone incorrect on scheduled reports",
    "Multi-factor auth prompt not appearing",
    "Data import job aborts halfway through",
    "User permissions not applying after sync",
    "PDF export missing charts",
    "Session expires unexpectedly mid-task",
    "Duplicate records created on form submit",
    "Third-party integration token rejected",
    "Print job fails from remote session",
    "Mobile app crashes on launch after update",
    "Configuration change not taking effect",
    "Disk usage alert on application server",
    "Memory leak suspected in worker process",
    "SMTP throttling errors during nightly send",
    "Database connection pool exhausted",
    "Sync lag between primary and replica",
    "UI freezes when loading large list",
    "License count mismatch reported",
    "Scheduled task skipped overnight run",
    "User locked out after password change",
    "Bulk update operation timed out",
    "Incorrect data shown on analytics widget",
    "Two-factor code email arrives 10 minutes late",
]

COMMENT_SNIPPETS = [
    "Reproduced the issue on staging. Gathering logs.",
    "Reviewed application logs, see recurring timeout on the auth service.",
    "Escalated to infrastructure team for network trace.",
    "Applied configuration change, monitoring for recurrence.",
    "Customer confirms issue resolved after restart.",
    "Root cause identified: stale cache entry after deployment.",
    "Added workaround in documentation, permanent fix tracked in backlog.",
    "Awaiting customer confirmation before closing.",
    "Unable to reproduce with provided steps, requested more detail.",
    "Patch scheduled for next release window.",
    "Increased timeout value from 30s to 90s as a mitigation.",
    "Tailed service logs during failure window, narrowed to one worker node.",
    "Rolled back recent config change, issue persists. Investigating further.",
    "Paired with on-call engineer, narrowed to a DNS resolution delay.",
    "Opened upstream ticket with vendor, reference attached.",
    "Memory graph shows steady climb over 48 hours prior to incident.",
    "Confirmed with database team that long-running query was the cause.",
    "Firewall rule updated to permit traffic from the new subnet.",
    "Credentials rotated and downstream clients updated.",
]

RESOLUTION_METHODS = [
    "Configuration change applied",
    "Service restarted",
    "Patch deployed",
    "Data corrected manually",
    "User error — guidance provided",
    "Permissions updated",
    "Cache cleared",
    "Workaround documented",
    "No action required — resolved itself",
    "Third-party fix applied",
    "Infrastructure capacity increased",
    "Credentials rotated",
]
