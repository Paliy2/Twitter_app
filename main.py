from flask import Flask
from twitter2 import main
app = Flask(__name__)


@app.route('/')
def index():
    return 'hello'


@app.route('/map/')
def render_t():
    return render_template('Map.html')


if __name__ == '__main__':
    # debug for server living while changing
    main()
    app.run(debug=True)
