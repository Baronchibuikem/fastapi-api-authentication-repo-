## About the project

A fastapi project with api integration for Login, Registration, Logout and ChangePassword with Celery configured to send out welcome mail upon successful registration

### env values

copy the code below into a .env and fill in the missing value

        DATABASE_URL=''
        SECRET_KEY=''
        ALGORITHM=HS256
        ACCESS_TOKEN_EXPIRE_MINUTES=60
        DATABASE_HOSTNAME=localhost
        DATABASE_PORT=5432
        DATABASE_PASSWORD=''
        DATABASE_NAME=''
        DATABASE_USERNAME=''
        DATABASE_TYPE=postgresql
