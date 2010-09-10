
__description__ = "Manage user accounts and sysadmins"
__config__ = {
    "sysadmins": dict(
        description = "List of sysadmins (id,username,sshkey_id,sshkey_type,sshkey)",
        default = [],
    )
}
