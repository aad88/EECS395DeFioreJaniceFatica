from flask import Flask, redirect, url_for, session
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.social import Social, SQLAlchemyConnectionDatastore, login_failed
from flask.ext.social.utils import get_connection_values_from_oauth_response
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

