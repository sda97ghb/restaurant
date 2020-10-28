#!/usr/bin/env bash
if [[ $# == 0 ]]; then
  echo "Usage: $0 <executable> [<args>]"
else
  while read p; do export "${p?}"; done < .env
  "$@"
fi
