from flask import Flask, render_template
import current_standings
app = Flask(__name__)


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    d_standings = current_standings.current_driver_standings()
    return render_template('index.html', d_standings=d_standings)


if __name__ == '__main__':
    app.run()
