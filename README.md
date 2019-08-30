# Example usage

    import unifi

    client = unifi.Client('username', 'password', 'unifi_controller_ip')

    print(client)
    print(list(client.get_sites()))
    nets = client.get_networks()
    print(list(nets))

