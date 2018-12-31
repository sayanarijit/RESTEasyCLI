#!/bin/sh

for x in $(ls tests/units/lib); do
    echo "* $x  -------------------"
    python tests/units/lib/$x || exit 1
done
