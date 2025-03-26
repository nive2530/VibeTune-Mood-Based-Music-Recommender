import json
import pandas as pd
import socket
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from kafka.sasl.oauth import AbstractTokenProvider
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider
import boto3
import random
import string
from io import StringIO
import os
import datetime


# ✅ Implement AbstractTokenProvider for AWS MSK IAM authentication
class MSKTokenProvider(AbstractTokenProvider):
    def token(self):
        token, _ = MSKAuthTokenProvider.generate_auth_token('us-east-1')
        return token

tp = MSKTokenProvider()

# ✅ Kafka Bootstrap Servers
bootstrap_servers = [
    'boot-dci.vibetune.1snc32.c6.kafka.us-east-1.amazonaws.com:9098',
    'boot-i2h.vibetune.1snc32.c6.kafka.us-east-1.amazonaws.com:9098',
    'boot-xse.vibetune.1snc32.c6.kafka.us-east-1.amazonaws.com:9098'
]

# ✅ Create Kafka Consumer
consumer = KafkaConsumer(
    'albums',  # Topic Name
    bootstrap_servers=bootstrap_servers,
    security_protocol='SASL_SSL',
    sasl_mechanism='OAUTHBEARER',
    sasl_oauth_token_provider=tp,
    client_id=socket.gethostname(),
    auto_offset_reset='earliest',  # Start reading from the beginning if no offset is stored
    enable_auto_commit=True,
    #value_deserializer=lambda v: json.loads(v.decode('utf-8'))  # Deserialize JSON messages
)


# Generate a random string for unique filenames
def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

# Initialize S3 client
s3_client = boto3.client('s3')

# Specify the S3 bucket and object key
bucket_name = 'vibe-tune'

DATA = []
try:
    for message in consumer:
        if isinstance(message.value, dict):  # ✅ Check if it's already a dictionary
            DATA.append(message.value)
        else:
            DATA.append(json.loads(message.value))
        if len(DATA)>=10:
            df = pd.DataFrame(DATA)
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)
            s3_key = "staging/albums/"+generate_random_string(20)+".csv"
            s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=csv_buffer.getvalue())
            print(f"DataFrame uploaded successfully to S3 bucket: {bucket_name} with key: {s3_key}")    
            DATA = []
except KeyboardInterrupt:
    pass
finally:
    consumer.close()