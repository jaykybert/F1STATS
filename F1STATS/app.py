from flask import Flask, render_template, request
# API Requests.
import current_standings
import grand_prix
import grand_prix_experimental
import season
# Get today's date.
import utils

app = Flask(__name__)


@app.route('/')
@app.route('/calender')
def index():
    year = request.args.get('year')
    race_list = season.race_calendar(year)
    date_today = utils.current_date()
    return render_template('calender.html', races=race_list, today=date_today)


@app.route('/driver-standings')
def driver_standings():
    round_no = request.args.get('round')
    year = request.args.get('year')
    d = current_standings.current_driver_standings(round_no, year)
    return render_template('driver_standings.html', results=d)


@app.route('/constructor-standings')
def constructor_standings():
    round_no = request.args.get('round')
    year = request.args.get('year')
    c = current_standings.current_constructor_standings(round_no, year)
    return render_template('constructor_standings.html', results=c)


@app.route('/race')
def race():
    round_no = request.args.get('round')
    year = request.args.get('year')
    r = grand_prix.race_results(round_no, year)
    return render_template('race.html', results=r)


@app.route('/qualifying')
def qualifying():
    round_no = request.args.get('round')
    year = request.args.get('year')
    q = grand_prix_experimental.qualifying_results(round_no, year)
    return render_template('qualifying.html', results=q)


@app.errorhandler(404)
def invalid_page(error):
    return render_template('invalid_page.html', error=error)


if __name__ == "__main__":
    app.run()

# TODO: Add point deficit to the next driver (?) in the standings - consider branching for this, will be a lot of work.
# TODO: Un-restrict the number of responses of the API - current limit to 30.
