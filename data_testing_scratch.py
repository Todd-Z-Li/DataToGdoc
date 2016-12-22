'''
Created on Dec 2, 2015

@author: Belly Strategy
'''
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
ENGINE_STRING = "postgresql+psycopg2://"+name+":"+pw+"###DATABASE URL###"
today = datetime.datetime.now()

#need to get the HTML template for google charts:
temp=open("google_charts_template.txt",'r').read()
pd=rq.monthly_checkins_and_new_users(chain_id)
monthly_trend_header=["Month and Year","Checkins","Users"]
assemb=pd[pd.columns[2:5]]
assemb2=assemb.values.tolist()
assemb2.insert(0,monthly_trend_header)


#print type(monthly_trend_header), monthly_trend_header
monthly_trend=json.dumps(assemb2)

print temp % (gt.monthly_checkin_combo(monthly_trend, 1, 1), chain_id)
