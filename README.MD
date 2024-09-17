# FastAPI Data-Science Project

This project is a FastAPI application that allows users to download PDF documents and make queries from that document.

## Features

- User registration and authentication with JWT tokens
- PostgreSQL database for data storage
- Email verification and password reset
- receiving answers to requests for a PDF document


## Getting Started

1. Clone the repository:

```bash
https://github.com/Hnatiak/DataScienceProject-back
```

2. Install the dependencies:

```bash
pip install poetry
poetry shell
poetry update
```

3. Please rename `.env.example` file to `.env` and set up the environment variables in it.

4. docker-compose up --build -d

for next steps:

```bash
cd app
```

5. Populate database schema:

```bash
alembic upgrade head
```

6. Run the application:

```bash
python main.py
```

### PyMagic team:

- [Roman Hnatiak](https://github.com/Hnatiak)
- [Gennadiy Shpak](https://github.com/gyshpak)
- [Olena Polkhova](https://github.com/ElenaPolkhovaS)
- [Mykyta Terpelovskyi](https://github.com/Dremorio)
- [Ivan Danyleiko](https://github.com/Ivan-Danyleiko)


## FOR DEVS:

HERE IS FRONTEND REPO: 

HERE IS FRONTEND RENDER: 

&#xa0;
