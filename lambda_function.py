import pandas as pd
import io
import os
import boto3

def lambda_handler(event, context):
    AWS_S3_BUCKET = "engel-tests-20851"
    #ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    #SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    s3_client = boto3.client(
        "s3"
        #aws_access_key_id=ACCESS_KEY_ID,
        #aws_secret_access_key=SECRET_ACCESS_KEY,
    )

    response = s3_client.get_object(Bucket=AWS_S3_BUCKET, Key="dataset_credit_risk.csv")
    
    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    
    if status == 200:
        print(f"Successful S3 get_object response. Status - {status}")
        df = pd.read_csv(response.get("Body"))

        df = df.sort_values(by=["id", "loan_date"])

        df = df.reset_index(drop=True)

        df["loan_date"] = pd.to_datetime(df.loan_date) 

        df_grouped = df.groupby("id")

        df["nb_previous_loans"] = df_grouped["loan_date"].rank(method="first") - 1 

        df['avg_amount_loans_previous'] = (
            df.groupby('id')['loan_amount'].apply(lambda x: x.shift().expanding().mean())
        )

        df['birthday'] = pd.to_datetime(df['birthday'], errors='coerce')

        df['age'] = (pd.to_datetime('today').normalize() - df['birthday']).dt.days // 365 

        df['job_start_date'] = pd.to_datetime(df['job_start_date'], errors='coerce') 

        df['years_on_the_job'] = (pd.to_datetime('today').normalize() - df['job_start_date']).dt.days // 365

        df['flag_own_car'] = df.flag_own_car.apply(lambda x : 0 if x == 'N' else 1)

        df = df[['id', 'age', 'years_on_the_job', 'nb_previous_loans', 'avg_amount_loans_previous', 'flag_own_car', 'status']]

        with io.StringIO() as csv_buffer:
            df.to_csv(csv_buffer, index=False)
        
            response = s3_client.put_object(
                Bucket=AWS_S3_BUCKET, Key="train_model.csv", Body=csv_buffer.getvalue()
            )
        
            status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        
            if status == 200:
                print(f"Successful S3 put_object response. Status - {status}")
            else:
                print(f"Unsuccessful S3 put_object response. Status - {status}")
                
    else:
        print(f"Unsuccessful S3 get_object response. Status - {status}")


event = {}

lambda_handler(event, context=None)
