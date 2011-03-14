
env.include_recipe("boto")

# Mount volumes and format is necessary

for vol in env.config.aws.volumes:
    env.cookbooks.aws.setup_ebs_volume(**vol)
