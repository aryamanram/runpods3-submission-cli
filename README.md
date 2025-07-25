(1) Install dependancies
pip install boto3
pip install client
pip install pytest

(2) Create Isolated Interpreter
python -m venv .venv

(3) Launch Docker Throw-Away s3
docker run -d --name localstack -p 4566:4566 -p 4571:4571 localstack/localstack

export S3_ENDPOINT_URL = http://localhost:4566
export AWS_REGION = us-east-1

(4) Sanity Check
pip install awscli-local
awslocal s3 mb s3://sandbox-check
awslocal s3 ls

(5) Submit Job through CLI
python -m src.submit_job --kernel sample_data/example_kernel.py --data   sample_data/example_input.json --meta   '{"description":"local test"}'

(6) Inspect what landed 
awslocal s3 ls s3://job-artifacts/88c1… --recursive

(7) Testing
pytest -q