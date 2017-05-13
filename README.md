# Detective Conan API

Hello Detectives! This API will allow you to search raw data about *Detective
Conan* characters and cases, derived from the Detective Conan World wiki.
Why? Because nothing has existed like this before
and Detective Conan is an institution.

The data is stored in JSON files that are loaded into a database on the server,
accessible via a Weppy REST API, which you can self-host if you accept CoAi as 
your One True Pairing. Right now, that database is SQLite, but it will be 
changed to PostgreSQL when it would make sense to do so. Eventually, I'll set
up a demonstration box and write a Python wrapper for this API, but this project
is in early stages.

## Setup
1. Clone this repository. `git clone https://github.com/lethargilistic/dcapi.git`

2. Install Weppy. `pip install weppy`

3. Create `keys.py` and define `DB_PIPE_KEY` as a `str` for use as your database key.

4. Initialize the database. `weppy -a dcapi setup`

5. Run the Weppy development server. `weppy -a dcapi run`

6. Make the API calls. Weppy defaults to `127.0.0.1:8000`.

## Example Usage
Here is an example GET request for data on a character:

`GET [api_url]/v0/character/[character_id]`

You can also search a character by name, whether that's their name in Japanese or romanji, or their name from the Funimation English dub and manga.

`GET [api_url]/v0/character/Ai Haibara`

## Planned Topics
* Character data (characters major enough to have their own page on Detective Conan World only)
* Case data (manga and anime only)
* Crossreferencing characters in cases (See the cases where Conan and Ai both appear)

## Other TODO
* Migrate from SQLite to PostgreSQL.
* Create a command to set the database key? 770?
* Use search library for text search. Whoosh?
