# DontSueMe digital service


## Environment variables
Name | Default | Description
--- | --- | ---
*DB_DIR* | `APP_DIR` | Folder to hold `db.sqlite3` file
*APP_DEBUG* | `True` | True\False - Django Debug mode
*ALLOWED_HOSTS* | `*` | Django allowed hosts, splitted by `,`
*SECRET_KEY* | `django-insecure-iex560z2^#h18ea%w&ev3-tpad!$f=fb)!ca@aa@&3*8gnw^2d` | Django secret token for csfr. You can generate using <https://djecrety.ir/>
--- | --- | ---
*DEFAULT_SUPERUSER_NAME* | `dontsueme` | Default superuser
*DEFAULT_SUPERUSER_EMAIL* | `dont@sue.me` | Default superuser email
*DEFAULT_SUPERUSER_PASSWORD* | `dontsueme` | Default superuser password
--- | --- | ---
*YC_LOCKBOX_SECRET_ID* | `None` | Yandex Lockbox secret id to get S3 static key
--- | --- | ---
*YC_IAM_TOKEN* | `None` | IAM token, by default is claimed from metadata
*YC_IAM_TOKEN_METADATA_URL* | http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token | Metadata service url to claim IAM token
--- | --- | ---
*S3_KEY* | `None` | format `ACCESS_KEY:SECRET_KEY`. By default should be claimed from Lockbox
*S3_REGION* | `ru-central1` | S3-region. Not to be changed for Yandex Object Storage
*S3_ENDPOINT_URL* | `https://storage.yandexcloud.net` | S3-endpoint. Not to be changed for Yandex Object Storage
*S3_BUCKET_NAME* | `yc-auth-test` | S3 bucket name
*S3_BUCKET_FOLDER* | `reports` | S3-"folder" name. Prefix for object key
*S3_METADATA_FILENAME* | `metadata.json` | S3-file name to save app metadata
--- | --- | ---
*OIDC_ENABLED* | `False` | OIDC login enabled
*OIDC_BUTTON_NAME* | `OIDC` | OIDC button display name
*OIDC_DOMAIN* | `keycloak.example.com` | OIDC provider domain
*OIDC_REALM_NAME* | `master` | OIDC realm name to generate endpoints from <https://{keycloakhost}:{keycloakport}/realms/{realm}/.well-known/openid-configuration>
*OIDC_CLIENT_ID* | `dontsueme-app` | OIDC client id
*OIDC_CLIENT_SECRET* | `dontsueme-app` | OIDC client secret
*OIDC_SIGN_ALGO* | `RS256` | OIDC realm sign algorithm
## How to run

- Copy `docker-compose.example.yml`
```
cp docker-compose.example.yml docker-compose.yml
```
- Configure environment veriables in compose
- Run
```
docker-compose up -d
```
