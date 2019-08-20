## auto bookshelf organizing

### Create virtual environment

Each project is self contained and has requires specific in a `requirements.txt`
To make things isolated, for each project you will create a separate
python virtual environment. This allows us to separate our dependancies and track them.

You will need to have python 3.6 in your path.

If it is your first time in a project:
```
python -m venv .venv
source .venv/bin/activate
cd bookshelf
pip install -r requirements.txt
```
## WARNING that this line should only be run when a completely new virual environment is created:
```
python -m venv .venv
```
## Recreate virtual environment with the same name will wipe out all previous installed packages.
After virtual venv is created, we only need to run the following line to enter the virtual venv to use it:
```
source .venv/bin/activate
```
If there a requirements.txt need to be created or updated:
```
pip freeze > requirements.txt
```
Or when you add a new dependency to your project you can manually add it to the
`requirements.txt` file.

To exit virtual environment in terminal
```
deactivate
```

