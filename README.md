# Prinder
Pull Request reminder for Github.

## Installation and Configuration
On *nix systems:-

1. Install Prinder using pip. 
```bash
pip install prinder
```
2. Create a configuration file with the name **prinder_config.yaml**. Fill in all the fields or leave them empty if you don't need them. Copy the config template from here - [prinder_config.yaml.template](https://github.com/masterlittle/Prinder/blob/master/prinder_config.yaml.template)

3. Get a github auth token with relevant access and assign it to the environment variable **PRINDER_GITHUB_API_TOKEN** or assign it in the configuration file to **github_api_token**. (Copying the token in the file is not recommended) 

4. Run the command with the file name as argument.
```bash
prinder run --config_file=<your-configuration-file-path>
eg - prinder run --config_file=prinder_config.yml
```
Prinder has a number of configurations using which you can configure hooks to Slack or Email. Some important ones are:

1. *organization_name*: The organization name for which to get pull requests.
2. *list_of_repos*: Provide a list of repos for which to get pending pull requests.
3. *topics*: Provide a list of topics attached to repositories for which to get pending pull requests.
4. *ignore_repos*: List of repos which should be ignored.
5. *slack:post_as_user*: The name which will be shown on Slack.

### Send pull request reminders to Slack
Get a slack token and assign it to the environment variable **PRINDER_SLACK_API_TOKEN** or assign it in the configuration file to **slack_api_token**. (Copying the token in the file is not recommended)

### Send pull request reminders in email
Configure a SMTP on your host and provide the details in the configuration file. 

