# MovieBase
RUN
==
```
git clone git@github.com:KingaBK/MovieBase.git
cd MovieBase
docker-compose up --build
```

DONE
==
Created functionalities:
- creating movie and comment resources;
- filtering and sorting based on a query;

Webservice is based on:
- Django;
- MySql,
- Docker.

TO DO/ TO CHANGE
==
- implement GET /top
- fetch movies data from http://www.omdbapi.com/ and add it to Response to POST /movies
- create automatic tests
- use Heroku


AUTHOR
==
Kinga Budziak