#!/bin/bash

which python3 > /dev/null || exit 1
which virtualenv > /dev/null || exit 1


export CLICOLOR=1
export LSCOLORS=gxBxhxDxfxhxhxhxhxcxcx


DEMO_DIR="~/recli_demo"

SKIP_INSTALL=false
echo $* | grep -wq 'skipinstall' && SKIP_INSTALL=true

SKIP_SERVE=false
echo $* | grep -wq 'skipserve' && SKIP_SERVE=true


green() {
    printf "\e[32m$1\e[0m"
}

blue() {
    printf "\e[34m$1\e[0m"
}

ul() {
    printf "\e[4m$1\e[0m"
}

p() {
    echo -n $(green "$ $1")
    read -s x
    echo
    eval "$1" || exit 1
    echo
}

c() {
    echo $(blue "# $1")
}


clear
c '====================================='
c 'Starting RESTEasyCLI interactive demo'
c '====================================='
echo
c 'Press [ENTER] key to continue with each step'
c 'Press ^c to exit demo at any time'
echo
read -sp '> understood'
echo
echo

c 'Create workspace'
p "mkdir -p $DEMO_DIR/workspace && cd $DEMO_DIR/workspace"

if ! $SKIP_INSTALL; then
    c 'Create and activate virtual environment'
    p "virtualenv -p python3 $DEMO_DIR/venv"

    p "source $DEMO_DIR/venv/bin/activate"

    c "Install package in $VIRTUAL_ENV"
    p 'pip install -U resteasycli'
fi

c 'Initialize workspace'
p 'recli init'

c 'See what did it actually do'
p 'ls'

c 'Check auto generated sites file'
p 'cat sites.yaml'

c 'Check auto generated auth file'
p 'cat auth.yaml'

c 'Check auto generated headers file'
p 'cat headers.yaml'

c 'Check auto generated saved requests file'
p 'cat saved.yaml'

c 'Check out the help menu'
p 'recli help'

c 'List available endpoints from sites file'
p 'recli list-endpoints'

c "Do GET request to $(ul https://jsonplaceholder.typicode.com/todos)"
p 'recli get testing/t'

c 'See help menu for "list" command'
p 'recli help list'

c 'Do the earlier GET request with parameter "userId=1" and format the output as a table'
p 'recli list testing/t --kwargs "userId: 1" --fit-width' x

c 'Add a slug "1" to previous request and format the output as a table'
p 'recli show testing/t/1 --fit-width'

c "Do DELETE request to $(ul https://jsonplaceholder.typicode.com/todos/1) (saved as testing/t1)"
p 'recli delete testing/t1'

c 'List saved requests from auto generated file'
p 'recli list-saved'

c 'Show details of a saved request'
p 'recli show-saved remind_shopping'

c 'Invoke this request'
p 'recli do remind_shopping'

c 'Fake the previous request with modified payload'
p 'recli redo remind_shopping --update_kwargs "{userId: 1, title: watch naruto}" --fake'

c 'Add "-s" or "--save_as" with an ID to save the request for later use'
p 'recli redo remind_shopping --update_kwargs "{userId: 1, title: watch naruto}" --fake --save_as my_request'

c 'Verify the newly saved request'
p 'recli show-saved my_request'

c 'Check where and how it is saved'
p 'cat saved.yaml'

c 'Invoke the saved request'
p 'recli do my_request'

c 'Generate API documentation automatically from workspace files'
p 'recli doc index.html --hide_cred'

if ! $SKIP_SERVE; then
    c "Serve the generated document on $(ul http://localhost:8080)"
    p 'python -m http.server -b 0.0.0.0 8080'
fi

c '==========================================================='
c 'CONGRATULATIONS...! you have completed the interactive demo'
c '==========================================================='
echo
$SKIP_INSTALL || c "This package currently is installed inside virtual environment: $DEMO_DIR/venv"
c "You can access your demo workspace here: $DEMO_DIR/workspace"
c 'You can install this tool globally by running: sudo pip install -U resteasycli'
c 'Or install it locally by running: pip install -U --user resteasycli'
