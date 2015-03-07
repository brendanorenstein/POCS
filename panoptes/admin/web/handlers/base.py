import tornado.auth
import tornado.escape
import tornado.web

import zmq
import pymongo
import bson.json_util as json_util

import numpy as np

from panoptes.utils import config, database, messaging, logger


@config.has_config
class BaseHandler(tornado.web.RequestHandler):

    """
    BaseHandler is inherited by all Handlers and is responsible for any
    global operations. Provides the `db` property and the `get_current_user`
    """
    @property
    def db(self):
        """ Simple property to access the DB easier """
        return self.settings['db']

    def get_current_user(self):
        """
        Looks for a cookie that shows we have been logged in. If cookie
        is found, attempt to look up user info in the database
        """
        # Get email from cookie
        email = tornado.escape.to_unicode(self.get_secure_cookie("email"))
        if not email:
            return None

        # Look up user data
        user_data = self.db.admin.find_one({'username': email})
        if user_data is None:
            return None

        return user_data


class MainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        user_data = self.current_user

        webcams = self.config.get('webcams')

        self.render("main.html", user_data=user_data, webcams=webcams)


class SensorHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("sensor_status.html")