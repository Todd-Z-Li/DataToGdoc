'''
Created on Dec 1, 2015

@author: todd
'''
#takes input of chain_id, generate output of HTML report with charts (up to to 4 charts with 1 table)

# with input, it makes multiple queries to redshift, thus we need to get the redshift stuff:
import pandas as pd
from sqlalchemy import create_engine
import datetime
import numpy as np
import sys
import json
import redshift_queries as rq

creds=json.load(open("cred.json"))

name=creds["redshift"]["name"]
pw=creds["redshift"]["pw"]

#default chain in case of no input is bellyHQ
chain_id = 12944

year=2011
ENGINE_STRING = "postgresql+psycopg2://"+name+":"+pw+"@belly-dw.ccv9wuksfoxg.us-east-1.redshift.amazonaws.com:5439/belly_dw?sslmode=require"
today = datetime.datetime.now()

#need to get the HTML template for google charts:
temp=open("google_charts_template.txt",'r').read()
print temp % ("test text asd;lkasdfospahgpaoshgaspoghdaspodhgfaposdifh", "possible title for everything (get chain name from query)")



#insert this with modifications, one for each chart. this is not a complete set there is much more on the gcharts_template file:

def drawchart_fn (chart_title, array_data, charttype,chartrow, chartcol):
    fn_txt= """

        var %s_data = new google.visualization.arrayToDataTable(%s , false);

        var %s_options = {'title':'%s',
                       'width':500,
                       'height':300};

        var %s_chart = new google.visualization.%s(document.getElementById('chart_div%d%d'));
        %s_chart.draw(%s_data, %s_options);


    """ % (chart_title, array_data, chart_title, chart_title,chart_title, charttype, chartrow, chartcol,chart_title, chart_title, chart_title)

    return fn_txt

def main(chain_id):
    year=2011
    chain_id=chain_id
    if len(sys.argv)>1:
        chain_id =  int(sys.argv[1])
        if len(sys.argv)>2:
            year=int(sys.argv[2])


if __name__ == '__main__':
    main()
    pass