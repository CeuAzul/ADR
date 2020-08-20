# Ambient

This class will give you the ambient parameters, such as Temperature, Pressure and humidity, it will also return to you the Air Density property.

By default the instantiation values will be: Temperature = 273.15, Pressure = 101325 and Humidity = 0

You can change these values in the instatiation of the class.

## Air density property

This property returns the air density for the given ambient.

```python

from adr.World import Ambient

ambient = Ambient(temperature = 300, pressure = 101325, humidity = 10)

print(ambient.air_density)
>>> 1.1764
```

Note that if you enter unvalid ambient instantiaon values, it will return an error.

```python

from adr.World import Ambient

ambient = Ambient(temperature = 300, pressure = 101325, humidity = -30)

print(ambient.air_density)
>>> raise ValueError(
                f"Absolute temperature and absolute pressure should be greater than zero. \
                Humidity should be between 0 and 100. \
                Found temp = 300, pressure = 101325 and humidity = -30"
            )
```
