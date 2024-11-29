# Luke Up
### 

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This project began as a way to deepen my understanding of full-stack web development and experiment with features that combine backend and frontend seamlessly.

- Backend with Django
- Plan on migrating front to React, right now It's built with Bootstrap with JS
- Mainly does API calls, some logic for OpenStreetMap, and stores messages on SQLlite


## Features

- IP Geolocation Lookup: Query and retrieve geolocation information based on IPs.
- DNS Lookup: Perform DNS record lookups for domain-related data.
- Data Storage: Collect and manage user messages with a SQLlite database.
- Future plans: Migrate the frontend to React.

## Installation

1 - Clone this repo, navigate to root and install requirements:

```sh
$ git clone https://github.com/lvl1rat/IP-Luke-UP.git
$ pip install -r requirements.txt
```

2 - Optional: Run a virtual env for better dependency management:

```sh
$ python3 -m venv env
$ source env/bin/activate
```

3 - If a venv folder comes withing the repo: (Might be more convinient)

```sh
$ source venv/bin/activate
```

Run the development server:

```sh
$ python3 manage.py runserver
```

Now simply access your local host at 8000 on your browser:

```sh
http://127.0.0.1:8000/
```


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/joemccann/dillinger>

