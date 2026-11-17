#!/usr/bin/env bash
# Manage the local symlink to this checkout's global skills directory.
set -euo pipefail

if (( $# != 2 )) || [[ "$1" != "install" && "$1" != "uninstall" ]]; then
  printf 'Usage: %s <install|uninstall> <target>\n' "$0" >&2
  exit 2
fi

target="$2"
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
skills_dir="${repo_dir}/skills"

case "$1" in
  install)
    if [[ -L "${target}" && "$(readlink -- "${target}")" == "${skills_dir}" ]]; then
      exit 0
    fi
    if [[ -d "${target}" && ! -L "${target}" ]]; then
      physical_repo_dir="$(cd -- "${repo_dir}" && pwd -P)"
      target_dir="$(cd -- "${target}" && pwd -P)"
      if [[ "${physical_repo_dir}/" == "${target_dir%/}/"* ]]; then
        printf '%s\n' \
          "Refusing to replace ${target}: it contains this checkout." >&2
        exit 1
      fi
      printf '%s\n' "${target} already exists as a directory." \
        "1. Back up" "2. Delete (permanently remove its contents)" "3. Cancel" >&2
      printf 'Choose [1-3] (default: 3): ' >&2
      IFS= read -r choice || choice=3
      case "${choice}" in
        1)
          backup="$(mktemp -d "${target}.backup.XXXXXX")"
          mv -- "${target}" "${backup}/"
          printf '%s\n' "Backed up ${target} into ${backup}/"
          ;;
        2)
          rm -rf -- "${target}"
          ;;
        3 | "")
          printf '%s\n' "Cancelled." >&2
          exit 1
          ;;
        *)
          printf '%s\n' "Invalid selection. Cancelled." >&2
          exit 1
          ;;
      esac
    fi
    if [[ -e "${target}" || -L "${target}" ]]; then
      printf '%s\n' "Refusing to replace ${target}. Move it aside first." >&2
      exit 1
    fi
    mkdir -p -- "$(dirname -- "${target}")"
    if ! ln -sT -- "${skills_dir}" "${target}"; then
      if [[ -L "${target}" && "$(readlink -- "${target}")" == "${skills_dir}" ]]; then
        exit 0
      fi
      printf '%s\n' "Could not create ${target}." >&2
      exit 1
    fi
    ;;
  uninstall)
    if [[ -L "${target}" && "$(readlink -- "${target}")" == "${skills_dir}" ]]; then
      rm -- "${target}"
    elif [[ -e "${target}" || -L "${target}" ]]; then
      printf '%s\n' "Refusing to remove ${target}: not a symlink to ${skills_dir}." >&2
      exit 1
    fi
    ;;
esac
