# Contributing

### Table Of Contents

[What should I know before I get started?](#what-should-i-know-before-i-get-started)
 * [Code of Conduct](#code-of-conduct)

[How can I contribute?](#how-can-i-contribute)
 * [Reporting Bugs](#reporting-bugs)
 * [Feature Requests](#feature-requests)
 * [Documentation](#documentation)

[Style Guidelines](#style-guidelines)
  * [Git Commit Messages](#git-commit-messages)
  * [Code Format](#code-format)
  * [PEP8](#pep8)
  * [DocStrings](#docstrings)

## What should I know before I get started?

### Code of Conduct

This project adheres to the Contributor Covenant [code of conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How can I contribute?

### Reporting Bugs

Please make sure you go through the [issues](https://github.com/kabirbaidhya/boss-cli/issues) and [pull requests](https://github.com/kabirbaidhya/boss-cli/pulls) before reporting a bug. There could be a chance that someone might already have reported a bug. When you are creating a bug report, please include as many details as possible to help us reproduce the problem easily.

### Feature Requests

If you have any suggestions or feature requests, create an [issue](https://github.com/kabirbaidhya/boss-cli/issues). Try to explain why the feature is important and how it helps.

### Documentation

If you think the docs for some features are missing or incomplete and you'd like to contribute, you're more than welcome to create a PR. You can also contribute for typo fixes or grammatical errors in the docs if you do find them.

## Style Guidelines

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move file to..." not "Moves file to...")

### Code Format

**Be Consistent.** If you're writing/editing code, take a few minutes to look at the code around you and determine it's style. If the code use spaces around if clauses, you should too.

If the code you add to a file looks drastically different from the existing code around it, it throws readers out of their rhythm when they to read it.

### PEP8
We are following the code style conventions as described in [PEP8](http://pep8.org/), make sure you're following these conventions too.

### DocStrings

When you write some code, make sure you have documented the code you've written. For more information on how to properly document your code using docstrings click [here](http://docs.python-guide.org/en/latest/writing/documentation/).

Example:

```python
def do_something():
    ''' This does something. '''
    pass


def do_something_else():
    '''
    This does something else.
    And something else.
    '''
    pass

```
