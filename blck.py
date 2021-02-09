#!/usr/bin/env python3
# copyleft (c) 2017-2021 parazyd <parazyd@dyne.org>
# see LICENSE file for copyright and license details.

from os import remove, rename
from os.path import join
from random import choice
from string import ascii_uppercase, ascii_lowercase
from threading import Thread
from time import sleep

from flask import (Flask, Blueprint, render_template, request,
                   send_from_directory)
import magic

bp = Blueprint('blck', __name__, template_folder='templates')

@bp.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('index.html', root=args.r)
    return short(request.files)


@bp.route("<urlshort>")
def urlget(urlshort):
    thread = Thread(target=del_file, args=(urlshort,))
    thread.daemon = True
    thread.start()
    return send_from_directory('files', urlshort)


def del_file(f):
    sleep(10)
    remove(join('files', f))


def short(c):
    if not c or not c['c']:
        return "invalid paste\n"

    s = genid()
    f = c['c']
    f.save(join('files', s))

    mimetype = None
    if f.mimetype:
        mimetype = f.mimetype
    else:
        mimetype = magic.from_file(join('files', s), mime=True)

    if mimetype:
        t = s
        s = s + '.' + mimetype.split('/')[1]
        rename(join('files', t), join('files', s))

    if request.headers.get('X-Forwarded-Proto') == 'https':
        return request.url_root.replace('http://', 'https://') + \
                   args.r.lstrip('/') + s +'\n'
    return request.url_root + args.r.lstrip('/') + s + '\n'


def genid(size=4, chars=ascii_uppercase + ascii_lowercase):
    return ''.join(choice(chars) for i in range(size))


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-r', default='/', help='application root')
    parser.add_argument('-l', default='localhost', help='listen host')
    parser.add_argument('-p', default=13321, help='listen port')
    parser.add_argument('-d', default=False, action='store_true', help='debug')
    args = parser.parse_args()

    app = Flask(__name__)
    app.register_blueprint(bp, url_prefix=args.r)

    if args.d:
        app.run(host=args.l, port=args.p, threaded=True, debug=args.d)
    else:
        from bjoern import run
        run(app, args.l, int(args.p))
