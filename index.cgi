#!/usr/local/bin/python3
from wsgiref.handlers import CGIHandler
from .line.app.app import app
CGIHandler().run(app) 
