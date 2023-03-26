import os
from dotenv import dotenv_values
from fastapi_sso.sso.github import GithubSSO

from dotenv import load_dotenv

load_dotenv()


sso = GithubSSO(
    client_id=os.environ.get('SSO_CLIENT_ID'),
    client_secret=os.environ.get('SSO_CLIENT_SECRET'),
    redirect_uri=os.environ.get('SSO_CALLBACK_URL'),
    allow_insecure_http=os.environ.get('SSO_ALLOW_INSECURE'),
)