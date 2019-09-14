[![Maintainability](https://api.codeclimate.com/v1/badges/a7e2c4672e2443b053f9/maintainability)](https://codeclimate.com/github/derekmwright/unifi_py/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a7e2c4672e2443b053f9/test_coverage)](https://codeclimate.com/github/derekmwright/unifi_py/test_coverage)

# Under Development
Code is under development and not suitable for inclusion is other projects. If you'd like to contribute, fork and submit a PR with your changes. If there is a feature you'd like to see, open a feature request in the issues section.

# Example usage

```python
import unifi

client = unifi.Client('username', 'password', 'unifi_controller_ip')

# Get Sites
print(client.get_sites())

# Get Networks
print(client.get_networks())
```
