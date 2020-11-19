import os
import time
import base64

from flask import url_for, flash, render_template, redirect, session, request, make_response
req = request
mkresp = make_response

from . import main
from ..paths import conpath
from .now import now
#from .. import mail
#from ..sdml import sdml
#from .forms import NameForm, PasswordForm, LoginForm, RegistForm

from jeefies import context
con = context(conpath, 'user')


def render(file, **kwargs):
    n = session.get(req.remote_addr + 'name', None)
    if n:
        kwargs['name'] = base64.urlsafe_b64decode(n)
    return render_template(file, **kwargs)

@main.route('/')
def index():
    t = now()
    return render('greet.html', tm=t)

