#!/bin/bash

# Schemas
for x in $(ls tests/units/schema); do
    echo "* $x  -------------------"
    python tests/units/schema/$x || exit 1
done

# Libraries
for x in $(ls tests/units/lib); do
    echo "* $x  -------------------"
    python tests/units/lib/$x || exit 1
done
