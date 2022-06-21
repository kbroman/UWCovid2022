#!/usr/bin/env python
# from Dan Fitch, https://gist.github.com/dgfitch/b6ca1cc61b4795e698cefdf672a90f23

import re
import requests
from requests_html import HTMLSession
import pandas as pd

session = HTMLSession()

r = session.get('https://covidresponse.wisc.edu/dashboard/')


def extract_regex(pattern, value):
    m = re.search(pattern, value)
    if m:
        g = m.groups()
        return [int(g[0])]
    else:
        return [0]

def extract_numbers(s):
    # In the format: '93 positive tests' or '853 tests'
    # But may be missing employees
    value = extract_regex(r"(\d+) ", s)
    return value

def pad_with_zero(val):
    val = int(val)
    if val < 10:
        return "0" + str(val)
    else:
        return str(val)

def reform_date(s):
    m = re.search("^Week of ([A-Za-z]+) (\d+)", s)
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

    if m:
        g = m.groups()
        month = pad_with_zero(months.index(g[0])+1)
        year = '2022'
        day = pad_with_zero(g[1])
        return(year + "-" + month + "-" + day)
    else:
        return["NA"]

def extract_data(chart):
    # grab date (like "August 7")
    dates = chart.xpath('//g/@data-tooltip_label')
    dates = [reform_date(x) for x in dates]
    dates_data = pd.DataFrame(dates)
    dates_data.columns = ['date']

    tooltips = chart.xpath('//g/@data-tooltip_annotation')
    data = pd.DataFrame([extract_numbers(x) for x in tooltips])
    data.columns = ['total']

    return pd.concat([dates_data, data], axis=1)

positive_chart = r.html.find('.svg-bar-chart', first=True)
tests_chart = r.html.find('#chart-covid-tests', first=True)

positive = extract_data(positive_chart)
tests = extract_data(tests_chart)

positive.columns = ['Date', 'Positive']
tests.columns = ['date', 'Total']
tests = tests[['Total']]

data = pd.concat([positive, tests], axis=1)
data = data[["Date","Total","Positive"]]
data.to_csv('uw_covid_2022.csv', index=False)
