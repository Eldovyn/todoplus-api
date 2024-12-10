from flask_bcrypt import Bcrypt
from .__init__ import create_app

app = create_app()
bcrypt = Bcrypt(app)
