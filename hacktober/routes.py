import os
import os.path
from flask import Flask, request, redirect, url_for, render_template, session, send_from_directory, send_file, flash, abort, make_response
from werkzeug.utils import secure_filename
from sqlalchemy.orm import sessionmaker
from sample import *
import DH
import pickle
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
app = Flask(__name__)
@app.route('/', methods=['GET'])
def create_user():
    """Create a user."""
    ...
    return render_template(
        'users.jinja2',
        users=User.query.all(),
        title="Show Users"
    )