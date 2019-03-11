import iup_server
from flask_gopher import GopherRequestHandler
application = iup_server.create_app()

if __name__ == "__main__":
    application.run(request_handler=GopherRequestHandler)
