~~~
~$ pip install geopy
Defaulting to user installation because normal site-packages is not writeable
Collecting geopy
  Downloading geopy-2.3.0-py3-none-any.whl (119 kB)
     |████████████████████████████████| 119 kB 1.3 MB/s
Collecting geographiclib<3,>=1.52
  Downloading geographiclib-2.0-py3-none-any.whl (40 kB)
     |████████████████████████████████| 40 kB 5.0 MB/s
Installing collected packages: geographiclib, geopy
Successfully installed geographiclib-2.0 geopy-2.3.0

~$ python
Python 3.10.10 (main, Feb  8 2023, 00:00:00) [GCC 12.2.1 20221121 (Red Hat 12.2.1-4)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import geopy
>>> from geopy.geocoders import Nominatim
>>> loc = Nominatim(user_agent="GetLoc")
>>> gl = loc.geocode("Boston")
>>> print(gl.address)
Boston, Suffolk County, Massachusetts, United States
>>> gl.latituted
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Location' object has no attribute 'latituted'. Did you mean: 'latitude'?
>>> gl.latitude
42.3554334
>>> gl.longitude
-71.060511
>>> gl = loc.geocode("Littleton, New Hampshire")
>>> gl
Location(Littleton, Grafton County, New Hampshire, 03561, United States, (44.3063899, -71.7710705, 0.0))
>>> gl = loc.geocode("sao paolo, brazil")
>>> gl
Location(São Paulo, Região Imediata de São Paulo, Região Metropolitana de São Paulo, Região Geográfica Intermediária de São Paulo, São Paulo, Região Sudeste, Brasil, (-23.5506507, -46.6333824, 0.0))
~~~
