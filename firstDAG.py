# Model 1  \                                                       accurate 
#           \                                                  y / 
# Model 2 --->  Choose the best Model --> Meet the threshold?   /
#           /                                                  n \ 
# Model 3  /                                                      \  inaccurate
#

from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator, BranchPythonOperator


from random import randint
def _training_model():
    return randint(1,10)

from airflow.operators.bash import BashOperator
def _choose_best_model(ti): #use task instance objec to fetch the data from the db
    accuracies=ti.xcom_pull(task_ids=['training_model_A','training_model_B','training_model_C'])
    best_accuracy=max(accuracies)
    if (best_accuracy>8): # How to pass the accuracy from the training model to best_accuray accuracy ? Need to share the data from training_model_X tasks into choose_best_model task. Using xcom
        return 'accurate' # the task_id
    return 'inaccurate' # the task_id

# create a DAG instance with context manager WITH. 
# catchup parameter: only the latest non-trigger DAG will be automatically triggered. It avoids many DAG runs between the start date and current date 
with DAG("my_dag", start_date=datetime(2021,1,1), 
schedule_interval="@daily",catchup=False) as dag:
    
    training_model_A=PythonOperator(
        task_id="training_model_A", #each task in the DAG needs to have a unique identifier
        python_callable=_training_model

    )

    training_model_B=PythonOperator(
        task_id="training_model_B", #each task in the DAG needs to have a unique identifier
        python_callable=_training_model

    )

    training_model_C=PythonOperator(
        task_id="training_model_C", #each task in the DAG needs to have a unique identifier
        python_callable=_training_model

    )

    choose_best_model=BranchPythonOperator( # need to share the data from training_model_X tasks into choose_best_model task. Using xcom
        task_id="choose_best_model",
        python_callable=_choose_best_model

    )

    accurate =BashOperator(
        task_id="accurate",
        bash_command="echo 'accurate'"
    )

    inaccurate =BashOperator(
        task_id="inaccurate",
        bash_command="echo 'inaccurate'"
    )

[training_model_A,training_model_B,training_model_C]>>choose_best_model>>[accurate,inaccurate]