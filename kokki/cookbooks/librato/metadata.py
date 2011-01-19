
__description__ = "Librato Silverline process monitoring and management"
__config__ = {
    "librato.api_token": dict(
        description = "API token for account",
        default = "0",
    ),
    "librato.server_id_cmd": dict(
        description = "Command to run to generate server ID",
        default = None,
    ),
    "librato.template_id": dict(
        description = "Template ID for this server",
        default = None,
    ),
    "librato.email_address": dict(
        description = "Email address of account",
        default = None,
    ),
}
