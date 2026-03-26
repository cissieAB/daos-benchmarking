#!/usr/bin/env bash

set -euo pipefail

REMOTE="${POSTER_REMOTE:-poster-2026}"
BRANCH="${POSTER_BRANCH:-main}"
PREFIX="${POSTER_PREFIX:-poster}"

usage() {
  cat <<EOF
Usage: $(basename "$0") <push|pull>

Environment overrides:
  POSTER_REMOTE   Remote name to sync with (default: ${REMOTE})
  POSTER_BRANCH   Branch name to sync with (default: ${BRANCH})
  POSTER_PREFIX   Subdirectory to sync (default: ${PREFIX})
EOF
}

if [[ $# -ne 1 ]]; then
  usage
  exit 1
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "This script must be run from inside the Git repository." >&2
  exit 1
fi

if ! git remote get-url "${REMOTE}" >/dev/null 2>&1; then
  echo "Remote '${REMOTE}' is not configured." >&2
  echo "Add it with:" >&2
  echo "  git remote add ${REMOTE} git@github.com:cissieAB/daos-poster-2026.git" >&2
  exit 1
fi

case "$1" in
  push)
    git subtree push --prefix="${PREFIX}" "${REMOTE}" "${BRANCH}"
    ;;
  pull)
    git subtree pull --prefix="${PREFIX}" "${REMOTE}" "${BRANCH}" --squash
    ;;
  *)
    usage
    exit 1
    ;;
esac
