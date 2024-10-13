import logging

from authlib.oidc.core import UserInfo
from flask import Blueprint, abort, session, url_for, redirect, request, render_template
from flask import current_app
from authlib.integrations.flask_client import OAuth

from src.constants.config import GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET, STRIPE_PUBLISHABLE_KEY
from src.constants.prices import PRICES
from src.db.user_dao import UserDao

bp = Blueprint('bill', __name__)


@bp.get("/pricing.html")
def pricing():
    return render_template('bill/pricing.html', **{
        "prices": PRICES,
        "stripePublicKey": STRIPE_PUBLISHABLE_KEY
    })
