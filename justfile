# Install this checkout's default skills into the local agent skills directory with GNU Stow.

stow_flags := "--restow --verbose"
stow_dir := justfile_directory() + "/skills"
target := env('HOME') + "/.agents/skills"
package := "default"

[default]
install:
    mkdir -p "{{ target }}"
    stow {{ stow_flags }} --dir "{{ stow_dir }}" --target "{{ target }}" {{ package }}

uninstall:
    if [ -d "{{ target }}" ]; then stow --delete --verbose --dir "{{ stow_dir }}" --target "{{ target }}" {{ package }}; fi
