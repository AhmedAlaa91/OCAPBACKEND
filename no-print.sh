#!/usr/bin/env bash
# no-print.sh
if grep -q "print(" "$@"; then
 echo "Error: Found print statement in $@"
 exit 1
else
 echo "OK: No print statement in $@"
 exit 0
fi
