# Model 1  \                                                       accurate 
#           \                                                  y / 
# Model 2 --->  Choose the best Model --> Meet the threshold?   /
#           /                                                  n \ 
# Model 3  /                                                      \  inaccurate
#

from airflow import DAG
from datetime import datetime

# create a DAG instance with context manager WITH. 
# catchup parameter: only the latest non-trigger DAG will be automatically triggered. It avoids many DAG runs between the start date and current date 
with DAG("my_dag", start_date=datetime(2021,1,1), 
schedule_interval="@daily",catchup=False) as dag: