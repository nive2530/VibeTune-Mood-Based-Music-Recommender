from kafka.errors import KafkaError
import socket
import time
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider

class MSKTokenProvider():
    def token(self):
        token, _ = MSKAuthTokenProvider.generate_auth_token('us-east-1')
        return token

tp = MSKTokenProvider()

producer = KafkaProducer(
    bootstrap_servers='<my bootstrap string>',
    security_protocol='SASL_SSL',
    sasl_mechanism='OAUTHBEARER',
    sasl_oauth_token_provider=tp,
    client_id=socket.gethostname(),
)


# ✅ Read and send messages from CSV
try:
    tracks = pd.read_csv('spotify_tracks.csv')

    for dt in tracks.to_dict(orient='records'):
        data = json.dumps(dt).encode('utf-8')

        try:
            result = producer.send('tracks', data).get(timeout=60)    
            print("✅ Message produced:", result)
        except Exception as e:
            print(f"❌ Error producing message: {e}")

finally:
    producer.close()
