boss-cli
=========

Yet another pythonic deployment tool built on top of [fabric](http://www.fabfile.org/).

Deploy like a boss.

## Installation

```bash
$ pip install boss-cli
```

## Usage
Comming soon ;)

## Configuration

### Custom Scripts
Custom scripts are scripts/commands that could be defined directly in the config file without having to write any line of python in the `fabfile.py`. They're similar to the [npm scripts](https://docs.npmjs.com/misc/scripts), if you're familiar with them.

You can define the custom scripts under the `scripts` field in the `boss.yml`.

**For instance:**
```yaml
# boss.yml
scripts:
  hello: 'echo "Hello World!"'
  build: npm run build
  logs: pm2 logs
```

Boss comes out of the box with a task `run` which you can use to run these scripts on the remote server like this:
```bash
$ fab dev run:hello
$ fab dev run:build
$ fab dev run:logs
```

## Change Log
Check the [CHANGELOG](CHANGELOG.md) for full release history.

## License
Licensed under [The MIT License](LICENSE).
