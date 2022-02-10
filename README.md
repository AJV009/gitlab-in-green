# gitlab-in-green
Add your GitLab activity to GitHub contribution charts

## Requirements
- Python 3
- python-dotenv (pip install python-dotenv)
## Usage
### NOTE: To use correctly, please fork this repo first or it wont work as expected.
### Steps:
- Fork this repo.
- Git clone the repo from your account.
- Copy the .env.sample to .env and fill in the expected values. You will need a private token with API access from your gitlab instance and a gitlab base url looks like git.qed42.net. refer https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html
- Run the following commands.
```bash
$ python gitlab-in-green.py
```