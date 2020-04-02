# Respirator Monitor System 
Respirator Monitor System (BCS) is a software aimed to the RPM and pressure
parameters of a respirator. It offers a web interface as well as a REST API in
order to receive the information of the device.

## Config file reference
This is an example of the config file:

```
[Respirator]
ID = 123
LOC = SF45
POLL_FREQ = 1

[Motor]
STARTUP_TIME = 60
MIN_RPM_MOTOR = 35
MAX_RPM_MOTOR = 45

[Preasure]
MIN_PRESSURE = 45
MAX_PRESSURE = 55
```

* **ID:** Indicates the identification number of the respirator.
* **LOC:** Indicates the localization of the respirator.
* **POLL_FREQ:** Respirators control poll frequency.
* **STARTUP_TIME:** Minimum time to gather samples before monitoring.
* **MIN_RPM_MOTOR:** Minimum operating RPM.
* **MAX_RPM_MOTOR:** Maximum operating RPM.
* **MIN_PRESSURE:** Minimum operating pressure.
* **MAX_PRESSURE:** Maximim operating pressure.


## API Reference
In order to retrieve the information of the respirator the api link is the
following:

```
http://example.com/api/info
```

Here there is an example of the output:

```
{
  "id": "123",
  "loc": "SF34",
  "pressure": 55,
  "rpm": 40,
  "status": "on"

}
```

* **id:** Identification number of the respirator.
* **loc:** Localization of the respirator.
* **pressure:** Pressure of the respirator.
* **rpm:** RPMs of the respirator.
* **status:** Status of the respirator.

## Authors
* **Albert Azemar i Rovira** - *Initial work* - [albert752](https://github.com/albert752)

## License
This project is licensed under the GNU General Public License v3.0 - see the 
[LICENSE.md](./LICENSE.md) file for details.
