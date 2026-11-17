# Link this checkout's global skills directory into the local agent directory.

skills_dir := justfile_directory() + "/skills"
target := env('HOME') + "/.agents/skills"

[default]
install:
    #!/bin/sh
    set -eu
    if [ -L "{{ target }}" ] && [ "$(readlink "{{ target }}")" = "{{ skills_dir }}" ]; then
      exit 0
    fi
    if [ -d "{{ target }}" ] && [ ! -L "{{ target }}" ]; then
      printf '%s\n' "{{ target }} already exists as a directory." \
        "1. Back up" "2. Delete (permanently remove its contents)" "3. Cancel" >&2
      printf 'Choose [1-3] (default: 3): ' >&2
      IFS= read -r choice || choice=3
      case "${choice}" in
        1)
          backup="$(mktemp -d "{{ target }}.backup.XXXXXX")"
          mv "{{ target }}" "${backup}/"
          printf '%s\n' "Backed up {{ target }} into ${backup}/"
          ;;
        2)
          rm -rf -- "{{ target }}"
          ;;
        3|"")
          printf '%s\n' "Cancelled." >&2
          exit 1
          ;;
        *)
          printf '%s\n' "Invalid selection. Cancelled." >&2
          exit 1
          ;;
      esac
    fi
    if [ -e "{{ target }}" ] || [ -L "{{ target }}" ]; then
      printf '%s\n' "Refusing to replace {{ target }}. Move it aside first." >&2
      exit 1
    fi
    mkdir -p "$(dirname "{{ target }}")"
    ln -s "{{ skills_dir }}" "{{ target }}"

uninstall:
    #!/bin/sh
    set -eu
    if [ -L "{{ target }}" ] && [ "$(readlink "{{ target }}")" = "{{ skills_dir }}" ]; then
      rm "{{ target }}"
    elif [ -e "{{ target }}" ] || [ -L "{{ target }}" ]; then
      printf '%s\n' "Refusing to remove {{ target }}: not a symlink to {{ skills_dir }}." >&2
      exit 1
    fi

reinstall: install
