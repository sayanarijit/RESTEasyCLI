#!/bin/bash


rm README.rst || exit 1
m2r README.md || exit 1

setup_py_v=$(grep 'VERSION = ' setup.py | awk '{print $3}' | sed "s/'//g")
config_v=$(grep 'VERSION = ' resteasycli/config.py | awk '{print $3}' | sed "s/'//g")

echo "setup.py: $setup_py_v"
echo "resteasycli/config.py: $config_v"

[ "v$setup_py_v" != "$config_v" ] && echo 'ERROR: VERSION not in sync: setup.py, resteasycli/config.py' && exit 1

echo 'all seems OK'
