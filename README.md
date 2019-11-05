# MovieBase

AUTHOR
==
Kinga Budziak

# DATE
2019.10.31

### RUN
```
git clone git@github.com:KingaBK/MovieBase.git
cd MovieBase
docker-compose up --build
```

### DONE
Created functionalities:
- creating movie and comment resources;
- filtering and sorting based on a query;

Webservice is based on:
- Django;
- MySql,
- Docker.

### TO DO/ TO CHANGE
- implement GET /top;
- fetch movies data from http://www.omdbapi.com/ and add it to Response to POST /movies;
- create automatic tests;
- use Heroku.

# DATE
2019.11.05

### RUN
Run server
```
git clone git@github.com:KingaBK/MovieBase.git
cd MovieBase
cp .env.example .env
# Set environment variables
docker-compose up --build
```

Run server tests

```
docker-compose up --build
docker-compose exec db bash
mysql -u root -p
> GRANT ALL PRIVILEGES ON test_movie_base.* TO '${MYSQL_USER}'@'%';

docker-compose exec web bash
python ./manage.py test 
```

### DONE
Created functionalities:
- creating movie and comment resources;
- filtering and sorting based on a query;
- creating statistics (GET /top);
- fetching movies data from http://www.omdbapi.com/ and add it to Response to POST /movies.
- creating some automatic tests (/movies POST and GET);
- using AWS.

Webservice is based on:
- Django;
- MySql,
- Docker.

### TO DO/ TO CHANGE
- create automatic tests for rest of functionalities;

