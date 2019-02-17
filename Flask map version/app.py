from flask import Flask, render_template, url_for,session,redirect
import time
import csv
from collections import defaultdict
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField
import dateutil.parser
import pytz

app = Flask(__name__)


app.config['SECRET_KEY'] = 'mysecretkey'

class InfoForm(FlaskForm):
    day = SelectField('Enter the date: ', choices=[('07-01', '7/01'), ('08-01', '8/01'),('09-01', '9/01'),('10-01', '10/01'),('11-01', '11/01'),('12-01', '12/01'),('13-01', '13/01')])
    hour = SelectField('What hour do you need?: ', choices=[('10', '10-11'),('11', '11-12'),('12', '12-13'),('13', '13-14'),('14', '14-15'),('15', '15-16'),('16', '16-17'),('17', '17-18'),('18', '18-19'),('19', '19-20')])
    submit = SubmitField('Submit')



@app.route("/", methods=['GET', 'POST'])
def index():
    form = InfoForm()
    if form.validate_on_submit():
        session['day'] = form.day.data
        session['hour'] = form.hour.data
        return redirect(url_for('index'))

    with open('locations.csv', 'r') as f:
        locations = defaultdict(list)
        reader = csv.reader(f)
        next(reader, None)
        data_read = [row for row in reader]
        for item in data_read:
            id = int(item[0])
            lng = item[1]
            lat = item[2]
            locations[id].append([lng,lat])

        day = session['day']
        hour = session['hour']
        with open('pickup_times.csv', 'r') as f:
            d = defaultdict(list)
            reader = csv.reader(f)
            next(reader, None)
            data_read = [row for row in reader]
            for item in data_read:
                t = dateutil.parser.parse(item[1])
                utc=pytz.UTC
                if t.strftime("%d-%m")== day and t.strftime("%H")== hour:
                    d[item[0]].append(item[2])

            medians = {}
            for k,v in d.items():
                median = sorted(v)[len(v) // 2]
                medians[int(k)]= median
            sorted_medians = dict(sorted(medians.items()))

    return render_template("app.html",form=form, locations=locations,d=d,medians=medians)


if __name__ == '__main__':
    app.run(debug=True)
