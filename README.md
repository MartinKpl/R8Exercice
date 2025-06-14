# R8Exercice
This is the Python developer recruitment exercise for R8Technologies
## Run the script
For startes running the code in a python enviroment is recommended, you can do this by running:
```
python -m venv venv

.\venv\Scripts\activate #on Windows

source /venv/bin/activate #on Linux
```
To run the script, first install the needed packages by running:
```
pip install -r requirements.txt
```
Once all the packages are installed you can run the script like so:
```
python main.py {CityName1 CityName2 ...}
```
If you want to run the unit tests you can by running:
```
python -m unittest .\UnitTests.py
```
## Possible enhancments

* Add a persistent caching system.
* Add a GUI with a library like PyQt or Tkinter
* Update it live and make it dynamic so cities can be removed or added without needing to execute the script everytime.