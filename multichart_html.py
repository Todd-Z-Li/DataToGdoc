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
import gcharts_templates as gt

creds=json.load(open("cred.json"))

name=creds["redshift"]["name"]
pw=creds["redshift"]["pw"]

#default chain in case of no input is bellyHQ
chain_id = 12944

year=2011
ENGINE_STRING = "postgresql+psycopg2://"+name+":"+pw+"@belly-dw.ccv9wuksfoxg.us-east-1.redshift.amazonaws.com:5439/belly_dw?sslmode=require"
today = datetime.datetime.now().date().isoformat()

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
    chain_id=str(chain_id)
    temp=open("google_charts_template.txt",'r').read()
    if len(sys.argv)>1:
        chain_id =  str(sys.argv[1])

    #step 1: Run a bunch of queries
    #step 2: get the result into an array of lists, with the first array being the columns
    #step 3: send each result into respective templates
    #step 4: get all the templates joined together
    #step 5: create .html file with the template and inserted info

    pd=rq.monthly_checkins_and_new_users(chain_id)
    monthly_trend_header=["Month and Year","Checkins","Users"]
    step1=pd[pd.columns[2:5]]
    step2=step1.values.tolist()
    step2.insert(0,monthly_trend_header)
    data=json.dumps(step2)
    monthly_trend=gt.monthly_checkin_combo(data, 1, 1)

    pd=rq.total_checkin_and_users(chain_id)
    checkins_and_users_header = ["Business Name", "Total Checkins", "Total Users"]
    step1=pd[pd.columns[1:4]]
    step2=step1.values.tolist()
    step2.insert(0,checkins_and_users_header)
    data=json.dumps(step2)
    checkins_and_users=gt.users_and_checkins_per_location_column(data, 1, 2)

    pd=rq.avg_monthly_checkins_and_users(chain_id)
    avg_monthly_checkins_and_users_header = ["Business Name", "Average Monthly Checkins", "Average Monthly Users","Subcategory ID", "Age of Business (Days)"]
    step1=pd[pd.columns[1:6]]
    step2=step1.values.tolist()
    step2.insert(0,avg_monthly_checkins_and_users_header)
    data=json.dumps(step2)
    avg_monthly_ckins_users=gt.avg_monthly_users_and_checkins_bubble(data, 2, 1)

    pd=rq.time_between_visits(chain_id)
    step2 = pd.values.tolist()
    header=["Visit Number", "Days Between Visits"]
    step2.insert(0,header)
    data=json.dumps(step2)
    print data
    time_between_visits=gt.time_between_visits_column(data, 2, 2)


    #rewards=json.dumps(rq.current_rewards(chain_id).values.tolist())


    final = monthly_trend+checkins_and_users+avg_monthly_ckins_users+time_between_visits#+rewards
    wf = open('Chain_Dashboard - %s %s.html' %(chain_id,str(today)),'w')
    wf.write(temp % (final, str(chain_id)))
    wf.close()



if __name__ == '__main__':
    main(chain_id)
    pass