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

### Basic Configuration
The basic configuration includes all the minimal configuration to deploy the app successfully. Create a file named `boss.yml` in your project's root directory.

##### `project_name`
`string`

The title or name of the project or application.
```yml
project_name: PROJECT_NAME
```

##### `project_description`
`string`

A short description about your project.
```yml
project_description: PROJECT_DESCRIPTION
```

##### `repository_url`
`string`

The location of repository where you or your team mates push the project.
```yml
repository_url: https://github.com/<username>/<project-name>
```

##### `username`
`string`

The user used to access the servers through SSH.
```yml
user: USERNAME
```
_Note:_ This user will be used to access all the servers mentioned in stages below.

##### `port`
`integer`

The port used to access the servers through SSH.
```yml
port: SERVER_SSH_PORT
```
_Note:_ This port will be used to access all the servers mentioned in stages below.

### Stages
Stages refer to the configured remote servers where you would like to deploy your application. E.g. `dev`, `qa`, `uat`, `staging`, `production`.

##### `stages`
`array/list`

The list of different stages of your application with their details.
```yml
stages:
    dev:
        ...
    uat:
        ...
```

##### `stages`.`<stage>`.`host`
`string`

Address of the hosted server for the defined stage.
```yml
host: <stage>.your-app.com
```

##### `stages`.`<stage>`.`user` `optional`
`string`

The user to access the defined staged server. This user overrides the user defined in [basic configuration](https://github.com/kabirbaidhya/boss-cli#basic-configutation). If not defined, the user defined in [basic configuration](https://github.com/kabirbaidhya/boss-cli#basic-configutation) will be used.
```yml
user: <stage>_SERVER_USERNAME
```

##### `stages`.`<stage>`.`port` `optional`
`integer`

The port to access the defined staged server. This port overrides the port defined in [basic configuration](https://github.com/kabirbaidhya/boss-cli#basic-configutation). If not defined, the port defined in [basic configuration](https://github.com/kabirbaidhya/boss-cli#basic-configutation) will be used.
```yml
port: <stage>_SERVER_SSH_PORT
```


##### `stages`.`<stage>`.`public_url`
`string`

The public url to access this website.
```yml
public_url: http://dev.your-app.com
```

##### `stages`.`<stage>`.`app_dir`
`string`

The absolute path of the project root directory in the server.
```yml
app_dir: /path/to/your/app
```yml

##### `stages`.`<stage>`.`logging`
`array/list`

The list of files to view server logs.
```yml
logging:
    ...
```

##### `stages`.`<stage>`.`logging`.`files`
`array/list`

The list of log files. It may include host server logs, database log and others.
```yml
files:
    - /path/to/access/log/file
    - /path/to/error/log/file
    - /path/to/database/log/file
```

### Notifications
You can configure to be notified when deployment starts to succeeds.

##### `notifications`
`array/list`

The list of different chat/IRC clients through which notifications can be sent.
```yml
notifications:
    slack:
        ...
    hipchat:
        ...
```

Currently, only hipchat and slack are supported. Further integrations are welcome through pull-requests.


#### Slack

##### `notifications`.`slack`.`enabled`
`boolean`

Enable/disable notification from slack.
```yml
enabled: true
```

##### `notifications`.`slack`.`endpoint`
`string`

Slack channel endpoint token to let boss-cli access the slack for sending notifications.
```yml
endpoint: SLACK_ENDPOINT
```

#### Hipchat

##### `notifications`.`hipchat`.`enable`
`boolean`

Enable/disable notifications from hipchat.
```yml
enabled: true
```

##### `notifications`.`hipchat`.`notify`
`boolean`

Enable/disable 'Do Not Disturb' mode for boss-cli notifications in hipchat.
```yml
notify: true
```

##### `notifications`.`hipchat`.`company_name`
`string`

Name of the company/organization/team you are involved in Hipchat.
```yml
company_name: HIPCHAT_COMPANY_NAME
```

##### `notifications`.`hipchat`.`room_id`
`integer`

The id of the room to which the notifications should be sent to.
```yml
room_id: HIPCHAT_ROOM_ID
```

##### `notifications`.`hipchat`.`auth_token`
`string`

Auth token to access the defined room by boss-cli for notifications.
```yml
auth_token: HIPCHAT_TOKEN
```

You can also use the applications's environment variables from `.env` file.
```yml
room_id: ${HIPCHAT_ROOM_ID}
auth_token: ${HIPCHAT_AUTH_TOKEN}
```

A sample of final configuration file:
```yml
#boss.yml
project_name: PROJECT_NAME
project_description: PROJECT_DESCRIPTION
repository_url: https://github.com/<username>/<project-name>
user: ${USERNAME}
port: ${SERVER_SSH_PORT}

stages:
    dev:
        host: dev.your-app.com
        public_url: http://dev.your-app.com
        app_dir: /path/to/your/app
        logging:
            files:
                - /path/to/error/log/file
                - /path/to/access/log/file
    uat:
        host: uat.your-app.com
        public_url: http://uat.your-app.com
        app_dir: /path/to/your/app
        logging:
            files:
                - /path/to/error/log/file
                - /path/to/access/log/file
    production:
        host: your-app.com
        port: ${PRODUCTION_SERVER_SSH_PORT}
        username: ${PRODUCTION_SERVER_USERNAME}
        public_url: http://your-app.com
        app_dir: /path/to/your/app
        logging:
            files:
                - /path/to/error/log/file
                - /path/to/access/log/file

notifications:
    slack:
        enabled: true
        endpoint: ${SLACK_ENDPOINT}
    hipchat:
        enabled: true
        notify: true
        company_name: ${HIPCHAT_COMPANY_NAME}
        room_id: ${HIPCHAT_ROOM_ID}
        auth_token: ${HIPCHAT_TOKEN}
```

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

## Contributing

Read our [contributing guide](CONTRIBUTING.md) to learn about our development process, how to propose bugs and improvements.

## Change Log
Check the [CHANGELOG](CHANGELOG.md) for full release history.

## License
Licensed under [The MIT License](LICENSE).
