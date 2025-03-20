## How to use local environments

**Create the local .venv environment**  
python -m venv .venv

**Activate the .venv environment**  
execute .venv/sctipts/Activate.ps1  
or .venv/sctipts/activate.bat

**Deactivate the .venv environment**  
type: deactivate  
or execute .venv/sctipts/deactivate.bat

**Check which local environment is active (on Windows)**  
where python

**Generate the `requirements.txt` file**  
pip freeze > requirements.txt

**Install dependencies from the `requirements.txt` file**  
pip install -r requirements.txt
