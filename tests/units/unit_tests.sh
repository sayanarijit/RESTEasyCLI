#!/bin/bash

# Schemas
for x in $(ls tests/units/schema/*_test.py); do
    echo "* $x  -------------------"
    python $x || exit 1
done

# Libraries
for x in $(ls tests/units/lib/*_test.py); do
    echo "* $x  -------------------"
    python $x || exit 1
done
