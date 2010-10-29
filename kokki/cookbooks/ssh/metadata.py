
__description__ = "SSH Service"
__config__ = {
    "sshd.allow_password_login_for_users": dict(
        description = "Allows password logins for the given users.",
        default = [],
    ),
}
