import sys
from getpass import getpass
from mastodon import Mastodon

login_email = raw_input("Bot login email (eg: username@domain.com): ").strip()

if "@" not in login_email:
    print "The login email should be an email, not a username"
    sys.exit(1)

account_password = getpass("Bot password (it won't be stored): ").strip()
api_base_url = raw_input("Url of the mastodon instance (eg: https://mastodon.social): ").strip()

if not api_base_url.startswith(("https://", "http://")):
    print "The url of the mastodon instance needs to start with either https:// or http://"
    sys.exit(1)

# Register app - only once!
Mastodon.create_app(
    'pokefight',
    api_base_url=api_base_url,
    to_file='pokefight.secret'
)

# Log in - either every time, or use persisted
mastodon = Mastodon(
    client_id='pokefight.secret',
    api_base_url=api_base_url
)

mastodon.log_in(
    login_email,
    account_password,
    to_file='user_pokefight.secret'
)
