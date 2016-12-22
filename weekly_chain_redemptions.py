'''
Created on Sep 24, 2015

@author: Belly Strategy
'''
# export DYLD_FALLBACK_LIBRARY_PATH=$HOME/anaconda/lib/:$DYLD_FALLBACK_LIBRARY_PATH

import pandas as pd
from sqlalchemy import create_engine
import datetime
import numpy as np
import sys
import json


creds=json.load(open("cred.json"))

name=creds["redshift"]["name"]
pw=creds["redshift"]["pw"]

chain_id = 12944
year=2011
ENGINE_STRING = "postgresql+psycopg2://"+name+":"+pw+"@###URL FOR DATABSE###?sslmode=require"
today = datetime.datetime.now()

# business_id = 13035

#pull results for query
def get_biz_users(chain_id, year):

    engine = create_engine(ENGINE_STRING)
    business_users_results = pd.read_sql_query("""
        select cl.business_id as business_id, extract(year from p.created_at) as year, extract(week from p.created_at) as week, p.created_at::date as purchase_date, r.description as description, p.points as points, count(distinct p.id) as purchase_count
        from bellyflop_purchases p left join bellyflop_clients cl on cl.id = p.client_id
        left join bellyflop_businesses b on b.id = cl.business_id
        left join bellyflop_rewards r on r.id = p.reward_id
         where r.chain_id = %d and extract(year from p.created_at) >= %d
         group by 1,2,3,4,5,6
        """ % (chain_id,year), engine)

    return business_users_results

def main(chain_id, year):
    chain_id=chain_id
    year=year
    if len(sys.argv)>1:
        chain_id =  int(sys.argv[1])
        if len(sys.argv)>2:
            year=int(sys.argv[2])
    result = get_biz_users(chain_id,year)
    rs=[1,2]
    print json.loads("["+json.dumps([result.columns.tolist(),result.columns.tolist()])+"]")
 #   print result.to_dict()
 #   print result.msgpack()
#    print result.to_string()

    resultpiv= pd.pivot_table(result, values='purchase_count', index=['business_id','description'], columns=['year','week'], aggfunc=np.sum)
    resultpiv.to_csv(path_or_buf=str(chain_id)+" "+str(year)+" weekly redemption report CREATED AT "+str(today.date())+".csv",encoding='utf-8')
    #print resultpiv
    print "successfully created " + str(chain_id)+" "+str(year)+" weekly redemption report "+str(today.date())+".csv"



if __name__ == '__main__':
    main(chain_id,year)
    pass
