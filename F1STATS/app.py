from flask import Flask, render_template
import current_standings
import last_grand_prix
import next_grand_prix

app = Flask(__name__)


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    r = next_grand_prix.next_race_info()
    return render_template('index.html', race=r)


@app.route('/driver-standings')
def driver_standings():
    d = current_standings.current_driver_standings()
    return render_template('driver_standings.html', d_standings=d)


@app.route('/constructor-standings')
def constructor_standings():
    c = current_standings.current_constructor_standings()
    return render_template('constructor_standings.html', c_standings=c)


@app.route('/last-race')
def last_race():
    r = last_grand_prix.last_race_results()
    return render_template('last_race.html', results=r)


@app.route('/last-qualifying')
@app.route('/last-quali')
def last_qualifying():
    q = last_grand_prix.last_quali_results()

    return render_template('last_quali.html', results=q)


@app.errorhandler(404)
def invalid_page(error):
    return render_template('invalid_page.html', error=error)


if __name__ == '__main__':
    app.run()
