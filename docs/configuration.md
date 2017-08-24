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
_**NOTE:** This user will be used to access all the servers mentioned in stages below._

##### `port`
`integer`

The port used to access the servers through SSH.
```yml
port: SERVER_SSH_PORT
```
_**NOTE:** This port will be used to access all the servers mentioned in stages below._

### Stages
Stages refer to the configured remote servers where you would like to deploy your application. E.g. `dev`, `qa`, `uat`, `staging`, `production`.

##### `stages`
`array`

You can define stages for each of the remote servers you have. For instance:
```yml
stages:
  dev:
    host: dev.your-app.com
    ...
  uat:
    host: uat.your-app.com
    ...
  ...
```

For each of the stages, you can define the following configuration options:

##### `host`
`string`

Address of the hosted server for the defined stage.
```yml
host: dev.your-app.com
```

##### `user`    **[ optional ]**
`string`

The user to access the defined staged server. This user overrides the user defined in [basic configuration](https://github.com/kabirbaidhya/boss-cli#basic-configutation). If not defined, the user defined in [basic configuration](https://github.com/kabirbaidhya/boss-cli#basic-configutation) will be used.
```yml
user: DEV_SERVER_USERNAME
```

##### `port`    **[ optional ]**
`integer`

The port to access the defined staged server. This port overrides the port defined in [basic configuration](https://github.com/kabirbaidhya/boss-cli#basic-configutation). If not defined, the port defined in [basic configuration](https://github.com/kabirbaidhya/boss-cli#basic-configutation) will be used.
```yml
port: DEV_SERVER_SSH_PORT
```


##### `public_url`
`string`

The public url to access this website.
```yml
public_url: http://dev.your-app.com
```

##### `app_dir`
`string`

The absolute path of the project root directory in the server.
```yml
app_dir: /path/to/your/app
```

##### `logging`
`array`

The list of logs on your remote server.
```yml
logging:
  ...
```

The log files can be listed under logging as following:

##### `logging.files`
`array`

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
`array`

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

##### `slack.enabled`
`boolean`

Enable/disable notification from slack.
```yml
enabled: true
```

##### `slack.endpoint`
`string`

Slack channel endpoint token to let boss-cli access the slack for sending notifications.
```yml
endpoint: SLACK_ENDPOINT
```

#### Hipchat

##### `hipchat.enabled`
`boolean`

Enable/disable notifications from hipchat.
```yml
enabled: true
```

##### `hipchat.notify`
`boolean`

Enable/disable 'Do Not Disturb' mode for boss-cli notifications in hipchat.
```yml
notify: true
```

##### `hipchat.company_name`
`string`

Name of the company/organization/team you are involved in Hipchat.
```yml
company_name: HIPCHAT_COMPANY_NAME
```

##### `hipchat.room_id`
`integer`

The id of the room to which the notifications should be sent to.
```yml
room_id: HIPCHAT_ROOM_ID
```

##### `hipchat.auth_token`
`string`

Auth token to access the defined room by boss-cli for notifications.
```yml
auth_token: HIPCHAT_TOKEN
```

_**NOTE:** You can also use the applications's environment variables from `.env` file._
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