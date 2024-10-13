import logging

from authlib.oidc.core import UserInfo
from flask import Blueprint, abort, session, url_for, redirect, request
from flask import current_app
from authlib.integrations.flask_client import OAuth

from src.constants.config import GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET
from src.db.user_dao import UserDao

bp = Blueprint('auth', __name__, url_prefix="/auth")

provider_name = 'google'

oauth = OAuth(current_app)
oauth.register(
    name=provider_name,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=GOOGLE_OAUTH_CLIENT_ID,
    client_secret=GOOGLE_OAUTH_CLIENT_SECRET,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@bp.route('/login/google')
def login():
    client = oauth.create_client(provider_name)
    if not client:
        abort(404)

    session["next"] = request.headers.get('Referer')

    redirect_uri = url_for('auth.callback', _external=True)
    logging.info(f"Redirect uri for login server [{provider_name}] is [{redirect_uri}]")
    return client.authorize_redirect(redirect_uri)


@bp.route('/callback/google')
def callback():
    client = oauth.create_client(provider_name)
    if not client:
        abort(404)

    token = client.authorize_access_token()
    userinfo: UserInfo = token.get('userinfo')

    session['user'] = UserDao.get_or_add_user(userinfo)

    next_uri = session.get("next", None)
    if next_uri:
        return redirect(next_uri)

    return redirect('/')


@bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')