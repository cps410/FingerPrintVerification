#!/bin/bash
source `which virtualenvwrapper.sh`

PROJ_NAME="auth_server"
PROJ_DIR_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

ENVS_HOME_DIR="$HOME/envs/"
ENV_NAME="FingerPrintVerification"

cd "$PROJ_DIR_PATH/$PROJ_NAME"
rm settings.py
rm settings.pyc
ln -s settings_development.py settings.py

cd $PROJ_DIR_PATH
chmod +x manage.py

deactivate
rmvirtualenv $ENV_NAME
mkvirtualenv $ENV_NAME
workon $ENV_NAME
pip install -r requirements.txt

./manage.py migrate
