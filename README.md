# Project Title

Query, store, and display the top starred repos on GitHub.

## Summary
This is a Flask based project locally backed by an SQLite database. Model validation are performed via Marshmallow and database integration via SQLAlchemy. The project is also deployed to Google Cloud where it is backed by a MySQL. [That can be found here.](https://starry-hearth-324007.ue.r.appspot.com/) 

## Getting Started

### Dependencies

* Python 3.6 or higher
* SQLite3

### Executing program

* Running the program is as simple as:
```
./local_deploy
```
* If you wish to change the number of repos pulled from GitHub you can modify the `PER_PAGE` variable and hit the refresh endpoint


## Notes

Given the simplicity of this project it was determined that creating blueprints, controllers, and static files were unnecessary and have been omitted
