import socket


def resolve_ip(address):
    try:
        socket.inet_aton(address)
        return address
    except socket.error:
        try:
            socket.gethostbyname(address)
            ip_address = socket.gethostbyname(address)
            return ip_address
        except socket.error:
            raise ValueError(f"{address} in not neither IP nor Domain")


def resolve_ip_list(address_list):
    resolved_list = []
    for address in address_list:
        try:
            socket.inet_aton(address)
            resolved_list.append(address)
        except socket.error:
            try:
                socket.gethostbyname(address)
                ip_address = socket.gethostbyname(address)
                resolved_list.append(ip_address)
            except socket.error:
                raise ValueError(f"{address} in not neither IP nor Domain")
    return resolved_list