# Accuknox-drf-test
This is a full-stack social networking platform built with Django, providing essential features for user registration, authentication, and social interactions. Users can create accounts, connect with friends, send and receive friend requests, and manage their social connections. The platform offers a RESTful API for seamless integration with front-end applications.


## How to run the project
1. clone the project <br>
``` git clone git@github.com:utkarshrathore2000/Accuknox-drf-test.git ```
2. Change your current directory <br>
```cd social_media```
3. Create a .env file from the .env.example file <br>
```cp .env.example .env```

4. Modify the variables in `.env` file:
- Replace the <POSTGRES_NAME>(database name) with yours 
- Replace the <POSTGRES_USER> with yours 
- Replace the <POSTGRES_PASSWORD_> with yours
- 
5.  Make a build <br>
```make build```

6.  Create a migrations file <br>
``` make makemigrations ```

7.  Apply the migrations <br>
``` make migrate```

5. Run your server <br>
```make runserver```

   
## How to run the test cases
``` make test```