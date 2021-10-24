# Python BaseSpace API
> Krishna Kumar

## Set-up VirtualEnv

```
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

## Environment Variables

Set BaseSpace variables and S3

BaseSpace AccessToken
```
accessToken=
projId=
```

AWS S3 variables
```
export AWS_KEY=
export AWS_SECRET=
```


## Run script
```
python3 main.py -p $projId -a $accessToken
```

## How to get Illumina BaseSpace AccessToken

1. Go to [https://developer.basespace.illumina.com/](https://developer.basespace.illumina.com/) and log in.
2. From the toolbar, select My Apps.
3. In the applications tab, select Create a New Application.
4. Fill out the Applications Details and then select Create Application.
5. On the application page, select the Credentials tab and copy the Access Token. No need to submit the app for review.

