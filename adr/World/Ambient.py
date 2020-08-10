from adr.World import air_gas_constant


class Ambient:
    def __init__(self, temperature=273.15, pressure=101325, humidity=0):
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity

    @property
    def air_density(self):
        cond1 = self.temperature > 0
        cond2 = self.pressure > 0
        cond3 = self.humidity >= 0 and self.humidity <= 100

        if cond1 and cond2 and cond3:
            return self.pressure / (air_gas_constant * self.temperature)
        else:
            raise ValueError(
                f'Absolute temperature and absolute pressure should be greater than zero. \
                Humidity should be between 0 and 100. \
                Found temp={self.temperature}, pressure={self.pressure} and humidity={self.humidity}')
