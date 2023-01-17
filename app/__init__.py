import os, sys
import logging
import logging.config

import json

from flask import Flask, render_template, Response, request, abort

import ellipses

if sys.platform.lower() == "win32":
    os.system('color')

level = os.environ.get("LOG_LEVEL", "INFO")

logging.info('LOG_LEVEL has value %s', level)

LOG_CONFIG = {
    'version': 1,
    'formatters': {'default': {
        'format': "%(asctime)s [%(process)s] %(levelname)s: %(message)s"},
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default',
            "level": level,
        },
        "console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": "INFO",
        },
        "console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": "DEBUG",
        }
    },
    "root": {"handlers": ["wsgi"], "level": level},
}

logging.config.dictConfig(LOG_CONFIG)

LOGGER = logging.getLogger("wsgi")

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():  # put application's code here
        return render_template("index.html", ellipses=json.dumps(ellipses.generate_ellipses(), separators=(',', ':')))

    @app.route('/preview/')
    def preview():  # put application's code here
        axes_only = False
        ellipses_only = False

        args = request.args
        ell = args.get("json")
        ell = json.loads(ell)

        page = args.get("page", type=int)
        if page is not None:
            if page == 2:
                axes_only = True
            elif page == 3:
                ellipses_only = True


        # Constuct raw bytes string
        bytes_str = ellipses.generate_preview(ell, axes_only=axes_only, ellipses_only=ellipses_only)

        # Create response given the bytes
        response = Response(bytes_str.getvalue(), mimetype='image/png')
        # response.headers['Content-Type: image/png']
        # response.headers['Content-Disposition: inline; filename="preview.png']

        return response

    @app.route('/getpdf/')
    def getpdf():
        args = request.args
        ell = args.get("json")
        ell = json.loads(ell)

        # Constuct raw bytes string
        bytes_str = ellipses.generate_pdf(ell)

        # Create response given the bytes
        response = Response(bytes_str.getvalue(), mimetype='application/pdf')
        # response.headers['Content-Type: image/png']
        # response.headers['Content-Disposition: attachment; filename="better_ellipses.pdf']

        return response

    @app.route('/ellipses/')
    def get_ellipses():
        MIN_N = 1
        MAX_N =20
        args = request.args
        n = args.get("n", type=int)
        if n is None or n < MIN_N or n > MAX_N:
            abort(400, f'Incorrect no of ellipses requested: [{n}], should be between {MIN_N} and {MAX_N}')

        resp = ellipses.generate_ellipses(n=n)

        response = Response(json.dumps(resp), mimetype='application/json')
        return response

    LOGGER.debug("App created")
    return app






