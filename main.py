from ui import Application
from logic import RequestHandler

if __name__ == "__main__":
    app = Application()
    request_handler = RequestHandler(app)

    # Bind the methods from RequestHandler to Application
    app.send_post_request = request_handler.send_post_request
    app.send_requests = request_handler.send_requests

    app.mainloop()