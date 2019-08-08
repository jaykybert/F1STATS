from flask import Flask, render_template, request
# API Requests.
import current_standings
import grand_prix
import season
# Get today's date.
import utils

app = Flask(__name__)


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/driver-standings')
def driver_standings():
    d = current_standings.current_driver_standings()
    return render_template('driver_standings.html', d_standings=d)


@app.route('/constructor-standings')
def constructor_standings():
    c = current_standings.current_constructor_standings()
    return render_template('constructor_standings.html', c_standings=c)


@app.route('/race')
def race():
    round_n = request.args.get('round_n')
    year = request.args.get('season')
    r = grand_prix.race_results(round_n, year)
    return render_template('race.html', results=r)


@app.route('/qualifying')
@app.route('/quali')
def qualifying():
    round_n = request.args.get('round_n')
    year = request.args.get('season')
    q = grand_prix.qualifying_results(round_n, year)
    return render_template('qualifying.html', results=q)


@app.route('/calender')
def calender():
    yr = request.args.get('year')
    race_list = season.race_calendar(yr)
    date_today = utils.current_date()
    return render_template('race_calender.html', races=race_list, today=date_today)


@app.errorhandler(404)
def invalid_page(error):
    return render_template('invalid_page.html', error=error)


if __name__ == '__main__':
    app.run()
