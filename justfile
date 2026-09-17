# Install this checkout as the local agent skills collection with GNU Stow.

stow_flags := "--restow --verbose"
stow_dir := justfile_directory()
target := env('HOME') + "/.agents"
package := ".agents"

[default]
install:
    mkdir -p "{{ target }}"
    stow {{ stow_flags }} --dir "{{ stow_dir }}" --target "{{ target }}" {{ package }}

uninstall:
    if [ -d "{{ target }}" ]; then stow --delete --verbose --dir "{{ stow_dir }}" --target "{{ target }}" {{ package }}; fi
