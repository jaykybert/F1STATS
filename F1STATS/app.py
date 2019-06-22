from flask import Flask, render_template
import current_standings
app = Flask(__name__)


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():

    return render_template('index.html', d_standings=d, c_standings=c)


global d, c
d = current_standings.current_driver_standings()
c = current_standings.current_constructor_standings()

if __name__ == '__main__':
    app.run()


