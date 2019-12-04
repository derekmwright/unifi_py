[![Maintainability](https://api.codeclimate.com/v1/badges/a7e2c4672e2443b053f9/maintainability)](https://codeclimate.com/github/derekmwright/unifi_py/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a7e2c4672e2443b053f9/test_coverage)](https://codeclimate.com/github/derekmwright/unifi_py/test_coverage)
[![Build Status](https://travis-ci.com/derekmwright/unifi_py.svg?branch=master)](https://travis-ci.com/derekmwright/unifi_py)

# Under Development
Code is under development and not suitable for inclusion in other projects. If you'd like to contribute, fork and submit a PR with your changes. If there is a feature you'd like to see, open a feature request in the issues section.

# Example usage

```python
import unifi

client = unifi.Client('username', 'password', 'unifi_controller_ip')

# Get Sites
print(client.get_sites())

# Get Networks
print(client.get_networks())

# Get sysinfo for all sites
print(list(map(lambda site: client.get_system(site), client.get_sites())))

# Get sysinfo for a single site
site = client.get_site('default')
print(client.get_system(site))
```
