fsem-scheduler
==============

# Development

Fork the repository. Then, to work with it locally:

Clone your repository

git clone https://github.com/USERNAME/fsem-scheduler.git
cd into the folder created, and use virtualenv to create an isolated python environment. Ensure that the path to the folder that you hold the files in does not contain any spaces.

virtualenv venv
(venv is the suggested foldername, as it is excluded in the .gitignore)

Activate the virtual environment

Ubuntu:
    source venv/bin/activate

Windows:
    venv/Scripts/activate

Then install project dependencies using

pip install -r requirements.txt
