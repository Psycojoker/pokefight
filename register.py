from mastodon import Mastodon

login_email = input("Bot login email (eg: username@domain.com): ").strip()
account_password = input("Bot password (it won't be stored): ").strip()
api_base_url = input("Url of the mastodon instance (eg: https://mastodon.social): ").strip()
api_base_url = input("Url of the mastodon instance (eg: https://mastodon.social): ").strip()

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
