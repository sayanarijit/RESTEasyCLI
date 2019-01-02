#!/bin/bash

clear
echo '========================================='
echo '* Starting RESTEasyCLI interactive demo *'
echo '========================================='
echo
echo 'Press [ENTER] key to continue with each step'
echo 'Press ^c to exit demo at any time'
echo
read -sp '> understood' x
echo
echo

echo '# Create and activate virtual environment'
read -sp '> virtualenv ~/recli_demo_venv' x
echo
virtualenv ~/recli_demo_venv || exit 1
echo

read -sp '> source ~/recli_demo_venv/bin/activate' x
echo
source ~/recli_demo_venv/bin/activate || exit 1
echo

echo "# Install package in $VIRTUAL_ENV"
read -sp '> pip install resteasycli' x
echo
pip install resteasycli || exit 1
echo

echo '# Create workspace'
read -sp '> mkdir ~/recli_demo_workspace && cd ~/recli_demo_workspace' x
echo
mkdir ~/recli_demo_workspace && cd ~/recli_demo_workspace || exit 1
echo

echo '# Initialize workspace'
read -sp '> recli init' x
echo
recli init || exit 1
echo

echo '# See what did it actually do'
read -sp '> ls' x
echo
ls || exit 1
echo

echo '# Check auto generated sites file'
read -sp '> cat sites.yml' x
echo
cat sites.yml || exit 1
echo

echo '# Check auto generated auth file'
read -sp '> cat auth.yml' x
echo
cat auth.yml || exit 1
echo

echo '# Check auto generated headers file'
read -sp '> cat headers.yml' x
echo
cat headers.yml || exit 1
echo

echo '# Check auto generated saved requests file'
read -sp '> cat saved.yml' x
echo
cat saved.yml || exit 1
echo

echo '# Check out the help menu'
read -sp '> recli help' x
echo
recli help|| exit 1
echo

echo '# List available endpoints from sites file'
read -sp '> recli list-endpoints' x
echo
recli list-endpoints || exit 1
echo

echo '# Do GET request to https://jsonplaceholder.typicode.com/todos'
read -sp '> recli get testing/todos' x
echo
recli get testing/todos || exit 1
echo

echo '# See help menu for "list" command'
read -sp '> recli help list' x
echo
recli help list|| exit 1
echo

echo '# Do the earlier GET request with parameter "userId=1" and format the output as a table'
read -sp '> recli list testing/todos --kwargs userId=1 --fit-width' x
echo
recli list testing/todos --kwargs userId=1 --fit-width || exit 1
echo

echo '# Add a slug "1" to previous request and format the output as a table'
read -sp '> recli show testing/todos/1 --fit-width' x
echo
recli show testing/todos/1 --fit-width || exit 1
echo

echo '# Do DELETE request to https://jsonplaceholder.typicode.com/todos/1 (saved as testing/todo1)'
read -sp '> recli delete testing/todo1' x
echo
recli delete testing/todo1 || exit 1
echo

echo '# List saved requests from auto generated file'
read -sp '> recli list-saved' x
echo
recli list-saved || exit 1
echo

echo '# Show details of a saved request'
read -sp '> recli show remind_shopping' x
echo
recli show-saved remind_shopping || exit 1
echo

echo '# Invoke this request'
read -sp '> recli do remind_shopping' x
echo
recli do remind_shopping || exit 1
echo

echo '# Fake the previous request with modified payload'
read -sp '> recli redo remind_shopping --update_kwargs userId=1 "title=watch naruto" --fake' x
echo
recli redo remind_shopping --update_kwargs userId=1 "title=watch naruto" --fake || exit 1
echo

echo '# Add "-s" or "--save_as" with an ID to save the request for later use'
read -sp '> recli redo remind_shopping --update_kwargs userId=1 "title=watch naruto" --fake --save_as my_request' x
echo
recli redo remind_shopping --update_kwargs userId=1 "title=watch naruto" --fake --save_as my_request || exit 1
echo

echo '# Verify the newly saved request'
read -sp '> recli show-saved my_request' x
echo
recli show-saved my_request || exit 1
echo

echo '# Check where and how it is saved'
read -sp '> cat saved.yml' x
echo
cat saved.yml || exit 1
echo

echo '# Invoke the saved request'
read -sp '> recli do my_request' x
echo
recli do my_request || exit 1
echo

echo '==============================================================='
echo '* CONGRATULATIONS...! you have completed the interactive demo *'
echo '==============================================================='
echo
echo 'NOTE:'
echo '  This package currently is installed inside virtual environment: ~/recli_demo_venv'
echo '  You can access your demo workspace here: ~/recli_demo_workspace'
echo '  You can install this tool globally by running: sudo pip install -U resteasycli'
echo '  Or install it locally by running: pip install -U --user resteasycli'
