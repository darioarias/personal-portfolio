# !/bash/bash

export FLASK_APP=run.py
export FLASK_CONFIG=testing
flask --help 2> /dev/null > /dev/null
if [[ "$?" != "0" ]]; then
  echo "activating virtual enviroment"
  source venv/bin/activate
fi

flask test