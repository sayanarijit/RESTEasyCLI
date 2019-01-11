# Contributing to RESTEasyCLI

This is a new born project and has lots of scope for improvements.

If you feel that you can help with any of above TODO list or if you have a totally unique idea, feel free to jump right in.

## Some tips
Here are some tips to start contributing to this project right away.

- Instead of directly creating pull requests, [create a issue](https://github.com/rapidstack/RESTEasyCLI/issues/new) first to check it's relevence and save efforts. However,
- If you find a bug, feel free to directly create pull requests by forking master branch
- Awesome if commit messages and pull request description are clear and concise
- One of it's depedency [RESTEasy](https://github.com/rapidstack/RESTEasy) has [a gitter channel](https://gitter.im/rapidstack/RESTEasy) for any doubt or discussion related to this project or [RESTEasy](https://github.com/rapidstack/RESTEasy)
- Use [pipenv](https://github.com/pypa/pipenv) to install/update dependencies
- Do not modify `README.rst` file. It's auto generated using [m2r](https://github.com/miyakogi/m2r) (Installed as a dev dependency). While updating `README.md` file.
- Run `./tools/before_commit.sh` before committing changes. It will take care of house keeping stuffs like generating `README.rst`, checking if VERSOIN info is updated correctly in all files etc.
- Create separate branches for separate issues or concerns.
- Keep updating your progress on the issue to let everyone know what you are working on.


## Setting up development environment

Before starting with any of the following steps make sure you have Python 3 installed

Steps:

1. Fork this project in your personal acount

2. Clone the project locally

```bash
git clone https://github.com/{your_username}/RESTEasyCLI
cd RESTEasyCLI
```

3. Install Pipenv other dependencies

```bash
sudo pip install pipenv
pipenv install --dev
```

4. Activate virtualenv and add current path in Python's library search path

```bash
pipenv shell
export PYTHONPATH=$PWD

# If required, install module using:
# python setup.py install
```

5. Do your stuff. Debug commands using `--debug` and `--verbose` options.

6. Test your stuff (if applicable)

```bash
sh tests/units/unit_tests.sh
python tests/e2e/execute_all_commands.py
```

7. Run before push

```bash
chmod +x tools/before_push.sh
./tools/before_push.sh
```

8. Push the code and raise pull request
