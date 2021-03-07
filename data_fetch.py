import pandas as pd
import sqlalchemy as sq
import numpy as np
from datetime import datetime, timedelta
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
engine = sq.create_engine('oracle://AMDSMTR:AMDSMTR@143.0.143.47:1521/AUTDBAMD')
conn = engine.connect()

def get_date_str(date, dialect):
    if dialect == 'oracle':
        return "to_date('{}', 'YYYY-MM-DD HH24:MI')".format(date.strftime(format='%Y-%m-%d %H:%M'))
    if dialect == 'mysql':
        return "'{}'".format(date.strftime(format='%Y-%m-%d %H:%M'))


eqno = 28
dialect = 'oracle'
start_date = '2020-11-16 00:00:00'
start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')


#AMDS DATA -- Input table
q = """
        select * from V_AMDS_DATA
        where id_plc_data_seq in (5000,5001,5002,5003,5004)
            and data_received_moment > {}
    """.format(get_date_str(start_date, dialect))

amds = pd.read_sql(q, con=conn)
amds.columns = [_c.upper() for _c in amds.columns]
amds.sort_values(by = 'DATA_RECEIVED_MOMENT', inplace = True)
amds.reset_index(inplace = True, drop = True)



#Equip Output
q = """
        select * from T_AI_EQUIP_OUTPUT 
        where eqno={}
            and data_received_moment > {}
    """.format(eqno, get_date_str(start_date, dialect))

equip = pd.read_sql(q, con=conn)
equip.columns = [_c.upper() for _c in equip.columns]
equip.sort_values(by = 'DATA_RECEIVED_MOMENT', inplace = True)
equip.reset_index(inplace = True, drop = True)


#Param Output
sensor = 18020
q = """
        select data_received_moment, id_plc_data_seq, predicted_value, predicted_thresh_one,
        predicted_thresh_two, regression_flag, consistency_flag
        from T_AI_PARAM_OUTPUT
        where id_plc_data_seq={} and scenario = 'LOAD'
            and data_received_moment > {}
    """.format(sensor, get_date_str(start_date, dialect))

param = pd.read_sql(q, con=conn)
param.columns = [_c.upper() for _c in param.columns]
param.sort_values(by = 'DATA_RECEIVED_MOMENT', inplace = True)
param.reset_index(inplace = True, drop = True)