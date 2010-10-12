
__description__ = "Security limits"
__config__ = {
    "limits": dict(
        description = "List of dictionaries with keys domain, type, item, and value.",
        default = [
            dict(domain="root", type="soft", item="nofile", value="30000"),
            dict(domain="root", type="hard", item="nofile", value="30000"),
        ],
    ),
}
