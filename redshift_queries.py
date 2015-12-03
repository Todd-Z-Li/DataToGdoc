'''
Created on Dec 1, 2015

@author: TODD !!! YAY!
'''
# modules for making life easier to query redshift

import pandas as pd
from sqlalchemy import create_engine
import datetime
import json


creds=json.load(open("cred.json"))

name=creds["redshift"]["name"]
pw=creds["redshift"]["pw"]

#default chain in case of no input is bellyHQ
chain_id = 12944

year=2011
ENGINE_STRING = "postgresql+psycopg2://"+name+":"+pw+"@belly-dw.ccv9wuksfoxg.us-east-1.redshift.amazonaws.com:5439/belly_dw?sslmode=require"
today = datetime.datetime.now()


#lets put down some queries

#for the first couple, we should do some where we need it in a monthly view for the sake of that multichart html generator

#these return a pandas dataframe (for now...)

def monthly_checkins_and_new_users (chain_id):
    engine = create_engine(ENGINE_STRING)
    result = pd.read_sql_query("""SELECT EXTRACT(YEAR FROM bc.created_at) AS year,
                                    EXTRACT(MONTH FROM bc.created_at) AS month,
                                    EXTRACT(YEAR FROM bc.created_at)::varchar || '-' || EXTRACT(MONTH FROM bc.created_at)::varchar as year_month,
                                    COUNT(DISTINCT bc.id) AS checkin_count,
                                    COUNT(DISTINCT CASE WHEN (prev_checkin.id IS NULL) THEN bc.user_id ELSE NULL END) AS new_member_count
                                  FROM bellyflop_businesses bb
                                    JOIN bellyflop_checkins bc ON bc.business_id = bb.id
                                    LEFT OUTER JOIN bellyflop_checkins prev_checkin
                                      ON prev_checkin.business_id IN (SELECT id FROM bellyflop_businesses WHERE chain_id = %s)
                                        AND prev_checkin.user_id = bc.user_id
                                        AND prev_checkin.created_at <= bc.created_at
                                        AND prev_checkin.id != bc.id
                                  WHERE bb.chain_id = %s and bc.created_at >= dateadd(day, -365, getdate())
                                    AND bc.points > 0
                                  GROUP BY 1,2,3
                                  ORDER BY 1,2
        """ % (chain_id, chain_id), engine)
    return result



def total_checkin_and_users (chain_id):
    engine = create_engine(ENGINE_STRING)
    result = pd.read_sql_query("""select bb.id as business_id, bb.name as business_name, COUNT(DISTINCT bc.id) AS checkins,
                                   COUNT(DISTINCT bc.user_id) AS users
                                  FROM bellyflop_businesses bb
                                    JOIN bellyflop_checkins bc ON bc.business_id = bb.id
                                  WHERE bb.chain_id = %s
                                    AND bc.points > 0
                                  GROUP BY 1,2
                                  ORDER BY 1
        """ % (chain_id), engine)
    return result

def avg_monthly_checkins_and_users (chain_id):
    engine = create_engine(ENGINE_STRING)
    result = pd.read_sql_query("""SELECT bb.id AS business_id,
                                    bb.name AS business_name,
                                    30*COUNT(DISTINCT bc.id)/datediff(day, min(bc.created_at), getdate()) AS avg_monthly_checkin_count,
                                    30*COUNT(DISTINCT bc.user_id)/datediff(day, min(bc.created_at), getdate()) AS avg_monthly_new_member_count,
                                    bb.sub_category_id as sub_category,
                                    datediff(day, min(bc.created_at), getdate()) as age
                                  FROM bellyflop_businesses bb
                                    LEFT OUTER JOIN bellyflop_checkins bc ON bc.business_id = bb.id
                                  WHERE bb.chain_id = %s
                                    AND bc.points > 0
                                  GROUP BY 1,2,5
                                  ORDER by 1
        """ % (chain_id), engine)
    return result

def current_rewards (chain_id):
    engine = create_engine(ENGINE_STRING)
    result = pd.read_sql_query("""SELECT
                                    br.description AS reward_description,
                                    br.created_at AS reward_created_at,
                                    br.deleted_at AS reward_deleted_at,
                                    br.points AS points,
                                    COUNT(DISTINCT bp.id) AS redemption_count,
                                    COUNT(DISTINCT bp.user_id) AS purchaser_count
                                  FROM bellyflop_businesses bb
                                    LEFT OUTER JOIN bellyflop_business_rewards bbr ON bbr.business_id = bb.id
                                    LEFT OUTER JOIN bellyflop_rewards br ON br.id = bbr.reward_id
                                    LEFT OUTER JOIN bellyflop_purchases bp ON bp.reward_id = br.id
                                  WHERE bb.chain_id = %s
                                  GROUP BY 1,2,3,4
                                  ORDER BY 5 DESC;
        """ % (chain_id), engine)
    return result

def time_between_visits (chain_id):
    engine = create_engine(ENGINE_STRING)
    result = pd.read_sql_query("""WITH checkins_with_sequence_and_last AS (
                                  SELECT
                                    c.id,
                                    c.user_id,
                                    c.created_at,
                                    ROW_NUMBER() OVER (PARTITION BY c.user_id ORDER BY c.created_at) AS sequence,
                                    LAG(c.created_at) OVER (PARTITION BY c.user_id ORDER BY c.created_at) as last_checkin_created_at
                                  FROM bellyflop_checkins c
                                  INNER JOIN bellyflop_businesses b
                                    ON b.id = c.business_id
                                  WHERE b.chain_id = %s
                                  ORDER BY 2, 3, 4
                                ),
                                checkins_from_users_with_10 AS (
                                  SELECT
                                    pc.*
                                  FROM checkins_with_sequence_and_last pc
                                  INNER JOIN (
                                    SELECT DISTINCT(user_id)
                                    FROM checkins_with_sequence_and_last
                                    WHERE sequence > 11
                                    ) limiter
                                    ON limiter.user_id = pc.user_id
                                  ORDER BY pc.user_id, pc.created_at
                                ),
                                checkins_bucketed AS (
                                  SELECT
                                    '1 to 2' AS milestone,
                                    user_id,
                                    DATEDIFF(hour, last_checkin_created_at, created_at)/24.0 days_between_visits
                                  FROM checkins_from_users_with_10
                                  WHERE sequence = 2

                                  UNION ALL

                                  SELECT
                                    '4 to 5' AS milestone,
                                    user_id,
                                    DATEDIFF(hour, last_checkin_created_at, created_at)/24.0 days_between_visits
                                  FROM checkins_from_users_with_10
                                  WHERE sequence = 5

                                  UNION ALL

                                  SELECT
                                    '9 to 10' AS milestone,
                                    user_id,
                                    DATEDIFF(hour, last_checkin_created_at, created_at)/24.0 days_between_visits
                                  FROM checkins_from_users_with_10
                                  WHERE sequence = 10
                                ),
                                checkins_pivoted AS (
                                  SELECT
                                    user_id,
                                    SUM(CASE WHEN milestone = '1 to 2' THEN days_between_visits END) AS one_to_two,
                                    SUM(CASE WHEN milestone = '4 to 5' THEN days_between_visits END) AS four_to_five,
                                    SUM(CASE WHEN milestone = '9 to 10' THEN days_between_visits END) AS nine_to_ten
                                  FROM checkins_bucketed
                                  GROUP BY 1
                                )
                                select * from (
                                SELECT
                                  'First to Second Visit', AVG(one_to_two)
                                FROM checkins_pivoted
                                  group by 1
                                UNION ALL
                                SELECT
                                  'Fourth to Fifth Visit', AVG(four_to_five)
                                FROM checkins_pivoted
                                  GROUP BY 1
                                UNION ALL
                                SELECT
                                  'Ninth to Tenth Visit',  AVG(nine_to_ten)
                                FROM checkins_pivoted
                                  GROUP BY 1) subq order by 1
        """ % (chain_id), engine)
    return result

