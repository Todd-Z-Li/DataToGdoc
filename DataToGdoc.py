'''
Created on Sep 24, 2015

@author: Belly Strategy
'''
# export DYLD_FALLBACK_LIBRARY_PATH=$HOME/anaconda/lib/:$DYLD_FALLBACK_LIBRARY_PATH

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import datetime
import numpy as np

business_id = 21271
# business_id = 13035
today = datetime.datetime.now()
engine = create_engine("postgresql+psycopg2://belly_user:REDACTEDg@10.35.0.206:5439/dev")

print "hello"

if __name__ == '__main__':
    pass