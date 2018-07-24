# Prinder
Pull Request reminder for Github with numerous configurations and templating feature using the powerful Jinja2

## Installation and Configuration
On *nix systems:-

1. Install Prinder using pip. 
```bash
pip install prinder
```
2. Create a configuration file. The default filename is **prinder_config.yaml** but you can name it whatever you want. Fill in all the fields or leave them empty if you don't need them. Copy the config template from here - [prinder_config.yaml.template](https://github.com/masterlittle/Prinder/blob/master/prinder_config.yaml.template)

3. Get a github auth token with relevant access and assign it to the environment variable **PRINDER_GITHUB_API_TOKEN** or assign it in the configuration file to **github_api_token**. (Copying the token to the file is not recommended)![token](https://github.com/masterlittle/Prinder/blob/update-readme/github_token_permissions.png)

4. Run the command with the file name as argument if required. If no argument is passed, it will try to find prinder_config.yaml in the working directory. The debug parameter can be passed to turn on detailed logging. 
```bash
prinder --config_file=<your-configuration-file-path>
eg -
    1. prinder
    2. prinder --config_file=prinder_config.yml
    3. prinder --debug
```

5. The logs of the service can be found at prinder.log in the working directory.

### Prinder has a number of configurations using which you can configure hooks to Slack or Email. Some important ones are:

1. *organization_name*: The organization name for which to get pull requests.
2. *list_of_repos*: Provide a list of repos for which to get pending pull requests.
3. *topics*: Provide a list of topics attached to repositories for which to get pending pull requests.
4. *ignore_repos*: List of repos which should be ignored.
5. *ignore_labels*: List of labels assigned to pull requests to be ignored.
6. *slack:post_as_user*: The name which will be shown on Slack.
7. *initial_message*: The text that will appear at the the top in the notification hooks.

### Formatting the notifications
 You can set your own look and feel of notifications and override the default using the templating files. The templating uses Jinja2 so everything is highly configurable.

 **For Slack**
 1. Create a template file. You can have a look at slack_template.template which is the default.
 2. Give the path to the template file in your configuration file.

  **For Mail**
 1. Create a template file. You can have a look at mail_template.html which is the default.
 2. Give the path to the template file in your configuration file.

 List of available information is :-
  1. Owner
  2. Initial Message
  3. List of pull request object
  4. A dictionary having pull requests with the repository name as the key
  5. *time_delta* function to calculate the number of days since pull request created


### Send pull request reminders to Slack
Get a slack token and assign it to the environment variable **PRINDER_SLACK_API_TOKEN** or assign it in the configuration file to **slack_api_token**. (Copying the token to the file is not recommended)

### Send pull request reminders in email
Configure a SMTP on your host and provide the details in the configuration file. 

# CONTRIBUTING
This started as a side project for a requirement that I had and as a way to improve my Python skills. I would warmly welcome any Pull requests and feature requests that you may have. Thanks  
