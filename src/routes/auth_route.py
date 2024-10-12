import logging

from flask import Blueprint, abort, session, url_for, redirect
from flask import current_app
from authlib.integrations.flask_client import OAuth

from src.config import GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET

bp = Blueprint('auth', __name__, url_prefix="/auth")

oauth = OAuth(current_app)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=GOOGLE_OAUTH_CLIENT_ID,
    client_secret=GOOGLE_OAUTH_CLIENT_SECRET,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@bp.route('/login/<name>')
def login(name: str):
    if not OAuthServer.contains(name):
        abort(404)

    client = oauth.create_client(name)
    if not client:
        abort(404)

    session["next"] = request.headers.get('Referer')

    redirect_uri = url_for('auth.auth', name=name, _external=True)
    logging.info(f"Redirect uri for login server [{name}] is [{redirect_uri}]")
    return client.authorize_redirect(redirect_uri)


@bp.route('/auth/<name>')
def auth(name: str):
    if not OAuthServer.contains(name):
        abort(404)

    client = oauth.create_client(name)
    if not client:
        abort(404)

    token = client.authorize_access_token()
    userinfo = token.get('userinfo')
    if not userinfo:
        userinfo = client.userinfo()
        if not userinfo["email"]:
            if name == OAuthServer.GITHUB.value:
                data = client.get("user/emails").json()
                userinfo["email"] = next(email['email'] for email in data if email['primary'])
            elif name == OAuthServer.GITEE.value:
                data = client.get("emails").json()
                userinfo["email"] = next(email['email'] for email in data if email['state'] == 'confirmed')

    # download avatar
    userinfo["server"] = name
    session['user_id'] = user_service.save_oauth_info(userinfo)
    user_dao.update_last_login_at(to_int(session['user_id']))

    next_uri = session.get("next", None)
    if next_uri:
        return redirect(next_uri)

    return redirect('/')


@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')