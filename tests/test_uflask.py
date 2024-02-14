import io

import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir+'/src')
from uflask import Flask


def test_route_dictionary_starts_empty():
    app = Flask()

    assert len(app.routes) == 0


def test_route_annotation_adds_entry_to_route_dictionary():
    app = Flask()

    @app.route("/")
    def my_route():
        pass

    assert len(app.routes) == 1


def test_find_handler_returns_handler_matching_uri_pattern():
    app = Flask()

    @app.route("/one.*")
    def my_route_one(uri_match):
        return "my_route_one"

    @app.route("/two.*")
    def my_route_two(uri_match):
        return "my_route_two"

    assert app.find_handler("/one_for_the_money")() == "my_route_one"
    assert app.find_handler("/two_for_the_show")() == "my_route_two"


def test_find_handler_passes_matched_uri_to_handler():
    app = Flask()

    @app.route("/one(.*)")
    def my_route_one(uri_match):
        return f"my_route_one {uri_match.group(1)}"

    assert app.find_handler("/one_for_the_money")() == "my_route_one _for_the_money"


def test_handle_writes_404_status_line_to_stream_when_uri_not_matched():
    app = Flask()
    stream = io.BytesIO()

    app.handle("/not_found", stream)

    assert stream.getvalue().startswith(b"HTTP/1.1 404 NOT FOUND\r\n")


def test_handle_writes_200_status_line_to_stream_when_uri_matched():
    app = Flask()
    stream = io.BytesIO()

    @app.route("/found")
    def my_route_found(uri_match):
        return ""

    app.handle("/found", stream)

    assert stream.getvalue().startswith(b"HTTP/1.1 200 OK\r\n")


def test_handle_writes_blank_line_and_atomic_message_body_to_stream_if_uri_matched():
    app = Flask()
    stream = io.BytesIO()

    @app.route("/found")
    def my_route_found(uri_match):
        return "message body"

    app.handle("/found", stream)

    assert stream.getvalue().endswith(b"\r\n\r\nmessage body")


def test_handle_writes_blank_line_and_generated_message_body_to_stream_if_uri_matched():
    app = Flask()
    stream = io.BytesIO()

    @app.route("/found")
    def my_route_found(uri_match):
        yield "message body"

    app.handle("/found", stream)

    assert stream.getvalue().endswith(b"\r\n\r\nmessage body")
