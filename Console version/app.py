import csv
from datetime import datetime
import collections
from collections import defaultdict
import dateutil.parser
import pytz


def median(date,time):

    with open('pickup_times.csv', 'r') as f:
        d = defaultdict(list)
        reader = csv.reader(f)
        next(reader, None)  # skip the headers
        data_read = [row for row in reader]
        for item in data_read:
            t = dateutil.parser.parse(item[1])
            utc=pytz.UTC
            if t.strftime("%d-%m")== date and t.strftime("%H")== time:
                d[item[0]].append(item[2])

    with open('medians.csv', mode='w') as y:
        fieldnames = ['restourant_id', 'pickup_time_median']
        writer = csv.DictWriter(y, fieldnames=fieldnames)
        writer.writeheader()
        medians = {}
        for k,v in d.items():
            median = sorted(v)[len(v) // 2]
            medians[int(k)]= median
        sorted_medians = dict(sorted(medians.items()))
        for k,v in sorted_medians.items():
                writer.writerow({'restourant_id': k, 'pickup_time_median': v})

date = input("Enter date in a format dd-mm: ")
time = input("Enter a hour in 24h format: ")
print("Wait... The window will be closed automatically.")

median(date,time)
