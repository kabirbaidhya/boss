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

Check the [configuration](docs/configuration.md) page.

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
user: deploy_user
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

### 2. Frontend Deployment

This deployment is useful for deploying the frontend apps (react, angular, vue etc) or static files to the remote server. This preset assumes the static files are served via a web server on the remote host eg: nginx, apache etc. Here, the source code is built locally and only the `dist` or `build` is uploaded and deployed to the server.

The deployment process is zero-downtime, just like [capistrano](https://github.com/capistrano/capistrano).

You'll need to set the deployment preset as `frontend` in your configuration.

```yml
deployment:
  preset: frontend
```

#### Configuration
Your `boss.yml` file for frontend deployment would look similar to this:
```yml
project_name: my-app
project_description: 'My App'
repository_url: 'https://github.com/username/repository'
branch_url: '{repository_url}/tree/{branch}'
user: deploy_user

deployment:
  preset: frontend
  build_dir: build/           # The local build directory
  base_dir: /app/deployment   # The remote base directory for deployment.

stages:
  prod:
    host: your-server.com
    public_url: 'https://your-server.com'

scripts:
  install: 'npm install'
  build: 'npm run build'

notifications:
  slack:
    enabled: true
    endpoint: ${BOSS_SLACK_ENDPOINT}
```

The above configuration would work for any kind of frontend web projects (eg: react, angular, ember, vue, vanila js etc) as long as it generates the build in static files (HTML, CSS, JS, media) that could be served via a web server.

You may define two scripts `install` and `build` in your `boss.yml`, to install project dependencies and build the source respectively. For instance: if you've created your application using [`create-react-app`](https://github.com/facebookincubator/create-react-app), you can set these to `npm install` and `npm run build` as shown in above config.

And you have to set the local directory to which the build is generated when the `build` script is run, in the `deployment.build_dir`. In our case this is `build/` directory.

#### Available tasks
You can check the available tasks for this preset with `fab --list`.

```bash
 ➜ fab --list

Available commands:

    buildinfo  Print the build information.
    builds     Display the build history.
    deploy     Zero-Downtime deployment for the frontend.
    info       Print the build information.
    logs       Tail the logs.
    rollback   Zero-Downtime deployment rollback for the frontend.
    run        Run a custom script.
    setup      Setup remote host for deployment.
    prod       Configures the prod server environment.
```

#### Remote Setup
Now you can run `setup` task on the remote to setup the remote host for the first time for deployment.

```bash
 ➜ fab prod setup
```
This will create necessary files and directories on the remote under the provided `base_dir` path. In our case the base directory will be `/app/deployment`.

Once, the `setup` task completes you should see message like this:

```
Remote is setup and is ready for deployment.

Deployed build will point to /app/deployment/current.
For serving the latest build, please set your web server document root to /app/deployment/current.
```

Now you'll need to configure your web server document root on the remote host to the `current` symlink created under the `base_dir` path. This symlink will point to the latest build when you deploy your app.

#### Web Server Config
If you're using a web server like nginx. You can set the document root like this:

```
# Sample nginx Configuration.
server {
  listen 80;
  listen [::]:80;

  # This is the symlink that points to the build that is deployed.
  root /app/deployment/current;

  index index.html;
  ...
}
```

#### Deploy
You can use the deploy task to deploy the app to the remote server.

Here, first the `deploy` task would trigger the `install` and `build` scripts to build the project locally, after which the built directory configured in `deployment.build_dir` would be tar-zipped and uploaded to the remote host via SSH.

So, to deploy current local source code to `prod` server you should do the following:
```bash
 ➜ fab prod deploy
```

If you're using `git` in your project, you need to make sure you did `checkout` to the branch you want to deploy and is upto date. Like this,
```bash
 # Checkout to the right branch and deploy
 ➜ git checkout master
 ➜ fab prod deploy
```

## Contributing

Read our [contributing guide](CONTRIBUTING.md) to learn about our development process, how to propose bugs and improvements.

## Change Log
Check the [CHANGELOG](CHANGELOG.md) for full release history.

## License
Licensed under [The MIT License](LICENSE).
