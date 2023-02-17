# Marvel Impossible Travel

This tool allows you to obtain information about Spectrum character and all other characters they've worked with in other comics, and save this information in a database.

## Prerequisites

- Docker

## Installation

1. Clone this repository
```
git clone https://github.com/your-username/marvel-characters.git
cd marvel-characters
```
2. Sign up for an API key from the Marvel Developer Portal
3. In the repository, create a file named `.env` and add your API key like this: 
```
API_KEY=<your_api_key>
PRIVATE_KEY=<your_api_key>
```
4. Build the Docker image: 
```docker build -t marvel_tool .```
5. Run the Docker container: 
```docker run --env-file .env -p 8000:8000 marvel_tool```


## Usage

The tool will automatically make requests to the Marvel API and save the information in a database. 

It will also provide endpoints to retrieve the information from the database.

You can also access the admin portal by acessing `http://localhost:8000/admin/` in your browser. The defaul user/password is `admin/password`.

## Limitations

The Marvel API has a limit of 3000 calls per day. Please be careful with your usage to avoid exceeding this limit.

## Tests

Run tests with the following command:
```./manage.py test character```

## Endpoints available

| Endpoint URL  | HTTP Method | Description | Parameters | 
|---------------| --- | --- | --- |
| /characters/ | GET | Retrieve a list of characters | None | 
| /characters/{id}   | GET | Retrieve details for a specific character | id (string) | 
