from flask import Flask, render_template
import current_standings
app = Flask(__name__)


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/driver-standings')
def driver_standings():
    return render_template('driver_standings.html', d_standings=d)


@app.route('/constructor-standings')
def constructor_standings():
    return render_template('constructor_standings.html', c_standings=c)


global d, c
d = current_standings.current_driver_standings()
c = current_standings.current_constructor_standings()


if __name__ == '__main__':
    app.run()
