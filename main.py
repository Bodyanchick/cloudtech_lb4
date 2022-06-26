import boto3 
import botocore 
import pandas 
import os


def Create_key_pair(): 
    ec2_client = boto3.client("ec2", region_name="us-east-2")
    try:
        key_pair = ec2_client.create_key_pair(KeyName="ec2-key-pair")
    except botocore.exceptions.ClientError as e:	
        if e.response['Error']['Code'] == "InvalidKeyPair.Duplicate": 
            print("Sorry, KeyPair already exists!")
        else:
            print("Unknown error occured")
    else:
        private_key = key_pair["KeyMaterial"] 
        f = open(f"./ec2-key-pair.pem", "w")
        f.write(private_key)	
        print("Key pair ec2-key-pair been created")

def Create_instance():
    ec2_client = boto3.client("ec2", region_name="us-east-2")  
    instances = ec2_client.run_instances(
        ImageId="ami-02d1e544b84bf7502", 
        MinCount=1,
        MaxCount=1, 
        InstanceType="t2.micro", 
        KeyName="ec2-key-pair"
    )

    print("New instance been  created") 
    print("Instance id: ", instances["Instances"][0]["InstanceId"])

def Get_ip(): 
    ec2_client = boto3.client("ec2", region_name="us-east-2") 
    reservations = ec2_client.describe_instances(
        InstanceIds=['i-0a9100e56eb2fa992']).get("Reservations") 
    for reservation in reservations:
        for instance in reservation['Instances']: 
            print(instance.get("PublicIpAddress"))

def Get_running_instances():	
    ec2_client = boto3.client("ec2", region_name="us-east-2")
    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["running"],
        },
        {
            "Name": "instance-type",
            "Values": ["t2.micro"]
        }]).get("Reservations")

    for reservation in reservations:
        for instance in reservation["Instances"]: 
            instance_id = instance["InstanceId"] 
            instance_type = instance["InstanceType"] 
            public_ip = instance["PublicIpAddress"] 
            private_ip = instance["PrivateIpAddress"]
            print(f"{instance_id}, {instance_type}, {public_ip}, {private_ip}")

def Stop_instance():
    ec2_client = boto3.client("ec2", region_name="us-east-2")
    response = ec2_client.stop_instances(InstanceIds=["i-0a9100e56eb2fa992"])
    print(response)

def Terminate_instance():	
    instance_id = input("Paste ID of instance you want to delete: ") 
    ec2_client = boto3.client("ec2", region_name="us-east-2")
    try:
        response = ec2_client.terminate_instances(InstanceIds=[instance_id]) 
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "InvalidInstanceID.Malformed":
             print("Instance with such ID doesn't exist")
        else:
            print("Unknown error occured")
    else:
        print("Instance been terminated")


def Create_bucket():
    bucket_name = input("Enter new bucket name: ") 
    s3_client = boto3.client('s3', region_name='us-east-2') 
    s3 = boto3.resource('s3')
    location = {'LocationConstraint': 'us-east-2'} 
    bucket = s3.Bucket(bucket_name)
    if bucket.creation_date is None:
        try:
            response = s3_client.create_bucket(
            Bucket=bucket_name, CreateBucketConfiguration=location)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "InvalidBucketName": 
                print("Invalid bucket name, try another one")
            else:
                print("Bucket named", bucket_name, "already exists in global!")
        else:
            print("New bucket been successfully created")
    else:
        print("Bucket named", bucket_name, "already exists!")

def Bucket_list():
    s3 = boto3.client('s3') 
    response = s3.list_buckets() 
    print('Existing buckets:')
    for bucket in response['Buckets']: 
        print(f' {bucket["Name"]}')        


def Upload_file():
    file_name = './CurrencyCode.csv'
    bucket_name = "lb4bucket"
    s3_obj_name = "tablichka"
    s3_client = boto3.client('s3')
    s3 = boto3.resource('s3')
    response = s3_client.upload_file(
        Filename=file_name, Bucket=bucket_name, Key=s3_obj_name) 
    print("File been successfully uploaded")



def Read_data():
    bucket_name = "lb4bucket"
    s3_obj_name = "tablichka"
    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')
    obj = s3_client.get_object( 
            Bucket=bucket_name, 
            Key=s3_obj_name
        )
    data = pandas.read_csv(obj['Body'])
    print('Printing the data frame...') 
    print(data.to_string())


def Destroy_bucket():	
    bucket_name = "lb4bucket"
    s3_client = boto3.client('s3') 
    response = s3_client.delete_bucket(Bucket=bucket_name)
    print("Bucket been successfully destroyed")

if __name__   == "__main__":
    
    #Create_key_pair()
    #Create_instance()
    #Get_ip()
    #Get_running_instances()
    #Stop_instance()
    #Terminate_instance()
    #Create_bucket()
    #Bucket_list()
    #Upload_file()
    #Read_data()
    Destroy_bucket()

