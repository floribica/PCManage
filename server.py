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
    change_password,
    trace_requests,
    hr_requests,
    users
)
from application.controllers.it.inventory import (
    computers,
    monitors,
    headsets,
    others,
    add_set
)
from application.controllers.it.del_headsets import (
    headsets,
    add_headset,
)


load_dotenv()
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
