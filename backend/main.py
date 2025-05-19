"""
Main entry point for the backend. Monkey patches eventlet to allow for asynchronous event handling.
"""

import eventlet

eventlet.monkey_patch()


if __name__ == '__main__':
    from server import run_server
    run_server()
