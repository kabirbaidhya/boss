boss-cli
=========

Yet another pythonic deployment tool built on top of [fabric](http://www.fabfile.org/).

Deploy like a boss.

## Installation

```bash
$ pip install fabric
$ pip install boss-cli
```

## Usage
Comming soon ;)

## Configuration

Check out the [configuration](https://github.com/kabirbaidhya/boss-cli/docs/configuration.md) page.

### Custom Scripts
Custom scripts are scripts/commands that could be defined directly in the config file without having to write any line of python in the `fabfile.py`. They're similar to the [npm scripts](https://docs.npmjs.com/misc/scripts), if you're familiar with them.

You can define the custom scripts under the `scripts` field in the `boss.yml`.

**For instance:**
```yaml
# boss.yml
stages:
  prod:
    host: your-server.com
    public_url: 'https://your-server.com'
    branch: master

scripts:
  hello: 'echo "Hello World!"'
  build: npm run build
  logs: pm2 logs
```

Boss comes out of the box with a task `run` which you can use to run these scripts on the remote server like this:
```bash
$ fab prod run:hello
$ fab prod run:build
$ fab prod run:logs
```

## Deployment

### 1. Remote Source Deployment

This is a generic deployment preset, where the remote host also contains the project source code and the git repository. The deploy task would synchronize the remote with the latest changes of the provided branch from the origin. It then builds the project and restarts the service if needed.

This is general and could be used for deploying any kind of projects and languages. You just need to specify the relevent `build` script to build your project in the remote and if it requires service restart then you'll need to define a `reload` script as well.

You'll need to set the deployment preset as `remote-source` in your configuration.

```yml
deployment:
  preset: remote-source
```

#### Configuration
Your `boss.yml` file for remote source deployment would look similar to this:
```yml
project_name: my-app
project_description: 'My App'
repository_url: 'https://github.com/username/repository'
branch_url: '{repository_url}/tree/{branch}'
# The SSH user through which the project is deployed.
user: deploy_user
# Application path on the remote host where the project is cloned.
app_dir: /source/my-app

deployment:
  preset: remote-source

stages:
  prod:
    host: your-server.com
    public_url: 'https://your-server.com'
    branch: master

scripts:
  install: 'npm install'
  build: 'npm run build'
  start: 'pm2 start dist/myapp.js'
  stop: 'pm2 stop dist/myapp.js'
  reload: 'pm2 reload dist/myapp.js'

notifications:
  slack:
    enabled: true
    endpoint: ${BOSS_SLACK_ENDPOINT}
```

The above configuration is specific to nodejs project deployment. But you can deploy projects built with other languages like PHP, python, java etc too. All you need to do is change the scripts `install`, `build`, `reload`.

#### Available tasks
You can check the available tasks for `remote-source` preset with `fab --list`.

```bash
 ➜ fab --list

Available commands:

    build    Build the application.
    check    Check the current remote branch and the last commit.
    deploy   Deploy to remote source.
    prod      Configures the prod server environment.
    logs     Tail the logs.
    restart  Restart the service.
    run      Run a custom script.
    status   Get the status of the service.
    stop     Stop the systemctl service.
    sync     Sync the changes on the branch with the remote (origin).
```

#### Deploy
Now to deploy the the application to the `prod` server that you've configured in the `stages` above. You can do:
```bash
 ➜ fab prod deploy
```

This would deploy the default branch `master` in this case. In case you need to deploy specific branch, you provide that too.
```bash
 ➜ fab prod deploy:branch=my-branch
```

## Change Log
Check the [CHANGELOG](CHANGELOG.md) for full release history.

## License
Licensed under [The MIT License](LICENSE).
