
__description__ = "SSH Service"
__config__ = {
    "sshd.allow_password_login_for_users": dict(
        description = "Allows password logins for the given users.",
        default = [],
    ),
    "sshd.password_authentication": dict(
        description = "Allow password authentication",
        default = False,
    ),
    "sshd.service_name": dict(
    	description = "Name of the ssh service",
    	default = None,
    ),
}
