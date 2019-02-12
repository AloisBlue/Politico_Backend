[![Coverage Status](https://coveralls.io/repos/github/AloisBlue/Politico_Backend/badge.svg?branch=ch-intergrations-fix-163768112)](https://coveralls.io/github/AloisBlue/Politico_Backend?branch=ch-intergrations-fix-163768112)
[![codecov](https://codecov.io/gh/AloisBlue/Politico_Backend/branch/ft-get-specific-office-163720410/graph/badge.svg)](https://codecov.io/gh/AloisBlue/Politico_Backend)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b52fa8718b0c4538b6c4f2511190131a)](https://www.codacy.com/app/AloisBlue/Politico_Backend?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=AloisBlue/Politico_Backend&amp;utm_campaign=Badge_Grade)
<<<<<<< HEAD
[![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/codeclimate/codeclimate/maintainability)
=======
[![Maintainability](https://api.codeclimate.com/v1/badges/a1a46a3438e3f150b0e4/maintainability)](https://codeclimate.com/github/AloisBlue/Politico_Backend/maintainability)
>>>>>>> 4f24b25b3cf3f58dd60283630c7ebe1eb1aba9f5
[![Build Status](https://travis-ci.com/AloisBlue/Politico_Backend.svg?branch=ft-get-specific-office-163720410)](https://travis-ci.com/AloisBlue/Politico_Backend)

#### Name of the backend
Politico_Backend
#### Description
The backend is designed to be consumed by a front end that conducts election
#### Language used
Python
#### Framework
Flask restful
#### Pivotal tracker dashboard
https://www.pivotaltracker.com/n/projects/2244219
#### How to run this backend app
- Clone the repo to your computer via ***git clone https://github.com/AloisBlue/Politico_Backend.git***
- Go to app directory ***cd Politico_Backend***
- Make a virtual environment ***python3 -m venv venv***
- Activate the above venv ***source venv/bin/activate***
- Export environment variable i.e. ***export FLASK_CONFIG=development && export FLASK_APP=run.py***
- Run the app ***flask run***

#### Routes
|ACTION   |ROUTE   |DESCRIPTION   |
|---|---|---|
|GET  | /api/v1/parties  |Get all parties in the data structure   |
|GET | /api/v1/offices  |Get all offices in the data structure   |
|GET  |/api/v1/parties/1   |Get a particular party by id   |
|GET   |/api/v1/offices/1   |Get a particular office by id   |
|POST   |/api/v1/parties   |Create a new non existent party   |
|POST   |/api/v1/offices   |Create a new non existent office   |
|PUT   |/api/v1/parties/1   |Edit an existing office with new details   |
|DELETE   |/api/v1/parties   |Delete an existing office out of the data structure   |

#### Deployment
Heroku
#### Heroku link
https://politico-backend-api.herokuapp.com

**NB:** *Use above heroku link with the routes provided above*

