import json
import boto3
import csv

# boto3 S3 initialization
s3_client = boto3.client("s3")


def lambda_handler(event, context):
    destination_bucket_name = 'teststreamesgi'

    # event contains all information about uploaded object
    print("Event :", event)

    # Bucket Name where file was uploaded
    source_bucket_name = event['Records'][0]['s3']['bucket']['name']

    # Filename of object (with path)
    file_key_name = event['Records'][0]['s3']['object']['key']
   
    destination_file_key_name = file_key_name.replace("tmp/", "")

    # Copy Source Object
    copy_source_object = {'Bucket': source_bucket_name, 'Key': file_key_name}

    # S3 copy object operation
    #s3_client.copy_object(CopySource=copy_source_object, Bucket=destination_bucket_name, Key="1/health/"+destination_file_key_name)
   
    obj = s3_client.get_object(Bucket=source_bucket_name, Key=file_key_name)
    lines = obj['Body'].read().decode('utf-8').split()
    
    info = lines[0].split(",")
    id = str(info[0])
    date = str(info[9])

    stripped = (line.strip() for line in lines)
    lines = (line.split(",") for line in stripped if line)
    with open('/tmp/health_data.csv', 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('iduser', 'gender', 'age', 'height', 'weight', 'steps', 'heartbeat', 'blood_pressure', 'temperature', 'date', 'hour'))
        writer.writerows(lines)
        
    s3_client.upload_file('/tmp/health_data.csv', destination_bucket_name,''+id+'/health/'+date+'/health_data.csv')
   
    s3_client.delete_object(Bucket=source_bucket_name, Key=file_key_name)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from S3 events Lambda!')
    }