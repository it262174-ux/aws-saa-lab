import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

def get_aws_metadata():
    """Retrieve Instance ID and AZ from AWS EC2 IMDSv2. Returns local dummy if not on EC2."""
    try:
        # Step 1: Get IMDSv2 Token (Valid for 60 seconds)
        token_headers = {"X-aws-ec2-metadata-token-ttl-seconds": "60"}
        token_resp = requests.put(
            "http://169.254.169.254/latest/api/token", 
            headers=token_headers, 
            timeout=1
        )
        token = token_resp.text

        # Step 2: Fetch Instance ID and AZ using Token
        meta_headers = {"X-aws-ec2-metadata-token": token}
        instance_id = requests.get(
            "http://169.254.169.254/latest/meta-data/instance-id", 
            headers=meta_headers, 
            timeout=1
        ).text
        az = requests.get(
            "http://169.254.169.254/latest/meta-data/placement/availability-zone", 
            headers=meta_headers, 
            timeout=1
        ).text
        return instance_id, az
    except Exception:
        return "local-dev-instance", "local-dev-az"

@app.route("/", methods=["GET"])
def hello():
    instance_id, az = get_aws_metadata()
    return jsonify({
        "message": "Hello from AWS SAA Lab!",
        "instance_id": instance_id,
        "availability_zone": az
    }), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
