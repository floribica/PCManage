import os

from dotenv import load_dotenv

from application import app
from application.controllers.login import (
    login,
    check
)
from application.controllers.admin import (
    dashboard,
    register,
    reset_password
)
from application.controllers.it import (
    dashboard,
    change_password
)


load_dotenv()
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
