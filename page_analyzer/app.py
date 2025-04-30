import os

from flask import Blueprint, Flask  # noqa: F401

from page_analyzer.controllers.check_route import check_page
from page_analyzer.controllers.routes import main_page

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


app.register_blueprint(main_page)
app.register_blueprint(check_page)

if __name__ == '__main__':
    app.run(debug=True)
