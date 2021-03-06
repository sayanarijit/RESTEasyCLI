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

* Fork this project in your personal acount

* Clone the project locally

```bash
git clone https://github.com/{your_username}/RESTEasyCLI
cd RESTEasyCLI
```

* Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

* Install recli along with development requirements keeping source files editable

```bash
pip install -e '.[develop]'
```

* Install pre-commit hooks

```bash
pre-commit install
```


## After setting up

* Do your stuff. Debug commands using `--debug` and `--verbose` options.

* Test your stuff (if applicable)

```bash
pytest --pdb --cov=resteasycli

### Use tox if you want to test on all python platforms (see tox docs).
# tox
```

* If required, run `./dev/bin/last_minute_check.sh` to take care of house keeping stuffs and perform basic checks.

* Commit and push the code and raise pull request
