# Respirator Monitor System 
Respirator Monitor System (RMS) is a software aimed to the RPM and pressure
parameters of a respirator. It offers a web interface as well as a REST API in
order to receive the information of the device.

## Introduction
The RMS will be connected to a magnetic switch on the respirator's arm 
in order to monitor
its movement as well as report the RPMs. The RMS is equiped with an alarm to
alert the user.

The following events will trigger the alarm (by order of priority):
    1. If in a time difference of MAX_DIFF_SAMPLES no sensor new interruptions are
       triggered. This means that the motor has stopped. It is important to set up
        the MAX_DIFF_SAMPLES value  taking into account the worst case scenario which corresponds to the
        cicle duration in MIN_RPM_MOTOR.
    2. If the motor module reports an rpm value of -2. This code represents an
       internal error.
    3. If the RPM value is not in the range of [MIN_RPM_MOTOR, MAX_RPM_MOTOR]
    4. Any other error with the reading of the RPM value 

## Features
- [x] Motor monitor
- [ ] Pressure sensor monitor

## Installation
1. Grab the image file from [here](https://mega.nz/file/vXwgXIQb)
2. Flash the image to an SD card with Raspberry's utility
3. Plug the SD card to the Raspberry and connect the alarm button to pin 13 and
   the motor sensor to pin 13. **Both of this components must be low level
   active**.
4. The current version does **not** have a configured WiFi network. In order
   to enable wireless connection, first of all access to the terminal via `ssh`
   with a wired connection or directly with the terminal. Run `sudo nano
   /etc/wpa_supplicant/wpa_supplicant.conf` and field the `ssid` and `psk` fields.
   Do not forget to include the surrounding "".
5. Reboot the Raspberry and enjoy!

## Config reference
This is an example of the config, it is changed at `__init__.py`:

```
config = {  
            "Respirator": {
                "ID": hex(getnode())[2:].upper()
                "LOC": "Not set",
                "POLL_FREQ": 1
            },
            "Motor": {
                "STARTUP_TIME": 60,
                "MIN_RPM_MOTOR": 12,
                "MAX_RPM_MOTOR": 35,
                "MAX_DIFF_SAMPLES": 6
            }
        }
```

* **ID:** Indicates the identification number of the respirator.
* **LOC:** Indicates the localization of the respirator.
* **POLL_FREQ:** Respirators control poll frequency.
* **STARTUP_TIME:** Minimum time to gather samples before monitoring.
* **MIN_RPM_MOTOR:** Minimum operating RPM.
* **MAX_RPM_MOTOR:** Maximum operating RPM.
* **MAX_DIFF_SAMPLES:** Maximum time difference between two consecutive samples.
    It is adviced to use the MIN_RPM_MOTOR cicle duration to take into account the
    worst case scenario.


## API Reference
### GET /api/status
In order to retrieve the information of the respirator the api link is the
following:

```
http://example.com/api/status
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
* **status:** Status of the respirator. Can be `off` when nothing has been received,
  , `cal` when it receives the first sample and suring the set up interval, `on` when
  functioning correctly or `fail` in case of faliure.
### POST /api/loc
In order to change the location parameter, a `POST` request is needed. The body
of it must be:

```
{"loc": "new_loc"}
```

It will return the same information as with the `GET /api/status` if the
parameter was correctly change or `{"error": "Location not changed"}` if it
fails to do so. 

## Authors
* **Albert Azemar i Rovira** - *Initial work* - [albert752](https://github.com/albert752)

## License
This project is licensed under the GNU General Public License v3.0 - see the 
[LICENSE.md](./LICENSE.md) file for details.
