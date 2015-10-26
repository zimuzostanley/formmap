# Formmap
View form submissions on Formstack on a geographical map.

Usage
-------
[Formmap](http://formmap.herokuapp.com) is a webapp built ontop of [Formstack](http://formstack.com) and Google maps and hosted on heroku. 
It helps form creators visualize where, geographically, their form submissions are coming from.
There are only 3 requirements to using this app:
1. Have an account on Formstack. Because that is your login credentials on Formmap.
2. Create forms on Formstack and enable *Prompt for location*.
3. It visualizes the geographical spread over answers from only *radio boxes* and *select boxes*.

Dev
--------

1. You need a working Python environment with [pip](https://pypi.python.org/pypi/pip) installed.
2. ``cd` into the root directory and run `pip install -r requirements.txt` to install the dependencies. (On Linux).
3. Visit the local app on `http://localhost:5000`
4. The map would not display because the API key in `./templates/map.html` is restricted to only the formmap domain.





