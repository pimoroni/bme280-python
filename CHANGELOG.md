2.0.0
-----

* Enhancement: Repackage to the uv/hatchling method, with PyPI trusted publishing
* Enhancement: Version is derived from the git tag, __version__ from package metadata
* Bugfix: Humidity sign correction was applied incorrectly
* Bugfix: Forced mode could wait forever for a measurement that never completes
* Bugfix: get_altitude took two measurements instead of one
* Python 3.9 or later, 3.7 and 3.8 support dropped

1.0.0
-----

* Repackage to hatch/pyproject.toml
* Require i2cdevice>=1.0.0 (smbus2)
* Fix: dig_h4/dig_h5 sign correction shifted instead of subtracting
* Fix: forced mode could wait forever for a measurement that never completes
* Fix: first reading in normal mode was taken before the first conversion finished
* Fix: get_altitude took two measurements instead of one

0.1.1
-----

* Fix so package is included in .whl releases

0.1.0
-----

* Switch to setup.cfg
* Match humidity compensation to BOSCH formula

0.0.2
-----

* Update to i2cdevice>=0.0.6 set/get API

0.0.1
-----

* Initial Release
