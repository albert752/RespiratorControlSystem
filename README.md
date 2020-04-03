# Respirator Monitor System 
Respirator Monitor System (RMS) is a software aimed to the RPM and pressure
parameters of a respirator. It offers a web interface as well as a REST API in
order to receive the information of the device.

## Introduction
The RMS will be connected to a magnetic switch on the respirators arm to monitor
its movement as well as report the RPMs. The RMS is equiped with an alarm to
alert the user.

The following events will trigger the alarm (by order of priority):
    1. If in a time difference of MAX_DIFF_SAMPLES no new interruptions are
       triggered. It means that the motor has stopped.
    2. If the motor module reports an rpm value of -2. This value represents an
       internal error.
    3. If the RPM value is not in the range of [MIN_RPM_MOTOR, MAX_RPM_MOTOR]
    4. Any other error with the reading of the RPM value 

## Features
- [x] Motor monitor
- [ ] Pressure sensor monito

## Config file reference
This is an example of the config file:

```
[Respirator]
ID = 123
LOC = SF45
POLL_FREQ = 1

[Motor]
STARTUP_TIME = 60
MIN_RPM_MOTOR = 10
MAX_RPM_MOTOR = 40
MAX_DIFF_SAMPLES = 6
```

* **ID:** Indicates the identification number of the respirator.
* **LOC:** Indicates the localization of the respirator.
* **POLL_FREQ:** Respirators control poll frequency.
* **STARTUP_TIME:** Minimum time to gather samples before monitoring.
* **MIN_RPM_MOTOR:** Minimum operating RPM.
* **MAX_RPM_MOTOR:** Maximum operating RPM.
* **MAX_DIFF_SAMPLES:** Maximum time difference between two consecutive samples.
    It is adviced to use the MIN_RPM_MOTOR cicle time to take into account the
    worst case scenario.


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
  "rpm": 40,
  "status": "on"
}
```

* **id:** Identification number of the respirator.
* **loc:** Localization of the respirator.
* **pressure:** Pressure of the respirator.
* **rpm:** RPMs of the respirator.
* **status:** Status of the respirator. Can be `off` when setting up, `on` when
  functioning correctly or `fail` in case of faliure.

## Authors
* **Albert Azemar i Rovira** - *Initial work* - [albert752](https://github.com/albert752)

## License
This project is licensed under the GNU General Public License v3.0 - see the 
[LICENSE.md](./LICENSE.md) file for details.
