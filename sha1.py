def chunks(str, n):
    return [str[i:i+n] for i in range(0, len(str), n)]


def rotl(n, b):
    # left roate a 32-bit integer x by n bits
        return ((n << b) | (n >> (32 - b))) & 0xffffffff


def preprocess(msg):
    bitstring = ''.join('{0:08b}'.format(ord(c), 'b') for c in msg)
    len_msg = len(bitstring)
    bitstring += '1'
    while len(bitstring)%512 != 448:
        bitstring += '0' 
    bitstring += '{0:064b}'.format(len_msg)
    blocks = chunks(bitstring, 512)
    for i in range(len(blocks)):
        blocks[i] = chunks(blocks[i], 32)
    return blocks

def getfk(t, x, y, z):
    if 0 <= t <= 19:
        f = (x & y) | ((~x) & z)
        k = 0x5a827999
    elif 20 <= t <= 39:
        f = x ^ y ^ z
        k = 0x6ed9eba1 
    elif 40 <= t <= 59:
        f = (x & y) | (x & z) | (y & z)
        k = 0x8f1bbcdc 
    elif 60 <= t <= 79:
        f = x ^ y ^ z
        k = 0xca62c1d6
    return f, k

def hexprint(lst):
    for x in lst:
        print(hex(x))


def hash_computation(blocks):
    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    for block in blocks:
        w = [None] * 80
        for i in range(16):
            w[i] = int(block[i], 2)
        for j in range(16, 80):
            w[j] = rotl((w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16]), 1)
        hexprint(w)
        print("-------------------")
        a = h[0]
        b = h[1]
        c = h[2]
        d = h[3]
        e = h[4]
        for t in range(80):
            f, k = getfk(t, b, c, d)
            T = rotl(a, 5) + f + e + k + w[t] & 0xffffffff
            e = d
            d = c
            c = rotl(b, 30)
            b = a
            a = T
            print(hex(a), hex(b), hex(c), hex(d), hex(e))
        h[0] = h[0] + a & 0xffffffff
        h[1] = h[1] + b & 0xffffffff
        h[2] = h[2] + c & 0xffffffff
        h[3] = h[3] + d & 0xffffffff
        h[4] = h[4] + e & 0xffffffff
    return h[0] << 32*4 | h[1]<<32*3 | h[2]<<32*2 | h[3]<<32 | h[4]



def sha1(msg):
    blocks = preprocess(msg)
    digest = hash_computation(blocks)
    return digest
        
digest = sha1('abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq')
print(hex(digest))