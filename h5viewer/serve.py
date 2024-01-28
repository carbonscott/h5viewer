#!/usr/bin/env python

import yaml
import logging
import argparse

from bokeh.server.server                 import Server
from bokeh.application                   import Application
from bokeh.application.handlers.function import FunctionHandler

from h5viewer.data   import H5Graph
from h5viewer.viewer import H5Viewer

def create_h5_viewer(path_h5):
    graph  = H5Graph(path_h5)
    viewer = H5Viewer(graph)

    return viewer


def create_document(doc, path_h5):
    viewer = create_h5_viewer(path_h5)
    doc.add_root(viewer.final_layout)


def run_bokeh_server(path_h5, port, websocket_origin):
    logging.basicConfig(level=logging.INFO)
    bokeh_logger = logging.getLogger('bokeh')
    bokeh_logger.setLevel(logging.INFO)

    # Create a Bokeh Application with the specified yaml
    bokeh_app = Application(FunctionHandler(lambda doc: create_document(doc, path_h5)))

    try:
        # Define server settings
        server_settings = {
            'port': port,
            'allow_websocket_origin': [websocket_origin]
        }

        # Create and start the Bokeh server
        server = Server({'/': bokeh_app}, **server_settings)
        server.start()

        server.io_loop.start()

    except KeyboardInterrupt:
        print("Shutting down...")
        server.stop()
        server.io_loop.stop()


def main():
    parser = argparse.ArgumentParser(description='Run the Bokeh PeakDiff Visualizer.')
    parser.add_argument('h5', help='Path to the HDF5 file')
    parser.add_argument('--port', help='Port to serve the application on', type=int, default=5000)
    parser.add_argument('--websocket-origin', help='WebSocket origin', default='localhost:5000')
    args = parser.parse_args()

    print(f"Starting H5 Viewer on http://localhost:{args.port}...")

    run_bokeh_server(args.h5, args.port, args.websocket_origin)


if __name__ == '__main__':
    main()
