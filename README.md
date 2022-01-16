# Python BaseSpace Lambda API
> Krishna Kumar

## Set-up VirtualEnv

```
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

## Environment Variables

Pass BaseSpace Access Token and Project ID as JSON

```json
{
  "accessToken": "<secret-token>",
  "projectId": "<projectid>",
  "uuid": "dee9e361-d241-4465-9e27-a097b79f5e94"
}
```

AWS S3 variables
```
export AWS_S3_BUCKET=cgx-lambda-uploader
```

## How to get Illumina BaseSpace AccessToken

1. Go to [https://developer.basespace.illumina.com/](https://developer.basespace.illumina.com/) and log in.
2. From the toolbar, select My Apps.
3. In the applications tab, select Create a New Application.
4. Fill out the Applications Details and then select Create Application.
5. On the application page, select the Credentials tab and copy the Access Token. No need to submit the app for review.


## AWS Lambda deploy
```shell
pip install --target packages -r requirements.txt 
cd packages/
zip -r ../deploy.zip .
cd ..
zip -g deploy.zip basespace_api.py http_session.py lambda_function.py timeout_adapter.py 
```
