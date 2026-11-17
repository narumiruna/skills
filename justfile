# Link this checkout's global skills directory into the local agent directory.

skills_script := justfile_directory() + "/scripts/manage-skills.sh"
target := env('HOME') + "/.agents/skills"

[default]
install:
    {{ quote(skills_script) }} install {{ quote(target) }}

uninstall:
    {{ quote(skills_script) }} uninstall {{ quote(target) }}

reinstall: install
