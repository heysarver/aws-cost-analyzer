# aws-cost-analyzer

An easier way to break down AWS costs by account.

## Setup

Create a .env file from the example.  You will need an AWS Access Key and Secret Access Key along with your organization account ID.

https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html

```
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_ORG_ID=your-org-id
```

## Usage

### Docker (recommended)
Local Image
```bash
$ docker build -t local/aws-cost-analyzer:dev .
$ docker run --env-file=.env -p 5000:5000 local/aws-cost-analyzer:dev
```
Docker Hub Image
```bash
$ docker run --env-file=.env -p 5000:5000 heysarver/aws-cost-analyzer:dev
```

The application will be available at http://localhost:5000/

### Python venv

Python 3.10

```bash
$ python -m venv venv && source venv/bin/activate
$ python app.py
```
