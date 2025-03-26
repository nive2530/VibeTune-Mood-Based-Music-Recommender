import json
import pandas as pd
import socket
from kafka import KafkaProducer
from kafka.errors import KafkaError
from kafka.sasl.oauth import AbstractTokenProvider
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider

# ✅ Implement AbstractTokenProvider properly
class MSKTokenProvider(AbstractTokenProvider):
    def token(self):
        token, _ = MSKAuthTokenProvider.generate_auth_token('us-east-1')
        return token

tp = MSKTokenProvider()

# Kafka Bootstrap Servers
bootstrap_servers = [
    'boot-dci.vibetune.1snc32.c6.kafka.us-east-1.amazonaws.com:9098',
    'boot-i2h.vibetune.1snc32.c6.kafka.us-east-1.amazonaws.com:9098',
    'boot-xse.vibetune.1snc32.c6.kafka.us-east-1.amazonaws.com:9098'
]

# Kafka Producer with SASL IAM Authentication
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    security_protocol='SASL_SSL',
    sasl_mechanism='OAUTHBEARER',
    sasl_oauth_token_provider=tp,
    client_id=socket.gethostname(),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize JSON
)

# ✅ Read and send messages from CSV
try:
    albums = pd.read_csv('spotify_albums.csv')

    for record in albums.to_dict(orient='records'):
        try:
            result = producer.send('albums', record).get(timeout=60)
            print("Message produced:", result)
        except KafkaError as e:
            print(f"Kafka error: {e}")
        except Exception as e:
            print(f"Error producing message: {e}")

except FileNotFoundError:
    print("Error: spotify_albums.csv not found.")
except Exception as e:
    print(f"Error reading CSV: {e}")
finally:
    producer.close()
