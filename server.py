import os

from dotenv import load_dotenv

from application import app
from application.controllers.login import (
    login,
    check
)
from application.controllers.admin import (
    dashboard,
    manage_user,
    register
)
from application.controllers.it import (
    dashboard,
    change_password,
    trace_requests,
    hr_requests,
    users,
    procesverbal
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
from application.controllers.recruiter import (
    dashboard,
    trace_requests,
    change_password,
    add_request
)
from application.controllers.planning import (
    dashboard,
    trace_requests,
    change_password,
    confirm_request
)
from application.controllers.receptionist import (
    dashboard,
    trace_requests,
    change_password,
    upload_procesverbal
)


load_dotenv()
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
