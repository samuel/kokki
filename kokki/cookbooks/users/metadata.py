
__description__ = "Manage user accounts and sysadmins"
__config__ = {
    "users": dict(
        description = "Disctionary of sysadmins with username as the key and value as a dictionary of (id,sshkey_id,sshkey_type,sshkey)",
        default = {},
    )
}
