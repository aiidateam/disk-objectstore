import uuid


def hex_from_ints(int1, int2):
    # remove 0x, fill with zeros
    return (hex((int1 * 2**64) + int2)[2:]).zfill(32)


def ints_from_hex(hex_string):
    hex1, hex2 = hex_string[:16], hex_string[16:]
    return int(hex1, 16), int(hex2, 16)


#%timeit compute_uuids(1000)
#100 loops, best of 3: 4.42 ms per loop
def compute_uuids(N):
    for i in range(N):
        _ = uuid.uuid4().hex


#%timeit compute_conversion(1000, h)
#1000 loops, best of 3: 1.5 ms per loop
def compute_conversion(N, uuid_hex):
    for i in range(N):
        int1, int2 = ints_from_hex(uuid_hex)
        _ = hex_from_ints(int1, int2)
