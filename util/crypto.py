import hashlib
import base64
import struct
import random
import math
import json

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

from . import string

G79_KEYS = [
    b"\x1C\x8D\x9C\xAD\x81\x1F\x2F\x1E\x3F\x7B\x3B\x5D\x20\x8D\xBE\x83",
    b"\x96\x27\x1E\xAE\x01\x7F\x44\x4B\x34\x2E\xB8\xC5\x3A\xE1\x06\xBA",
    b"\x6B\x5F\xF1\x29\x2C\x60\x23\x7E\x77\x69\x23\xCF\x4C\x49\xED\x9A",
    b"\xF0\x20\x96\x9C\x88\x3F\x9C\x7A\xDC\x2C\x5A\x13\x0F\xD1\xA9\xCC",
    b"\x60\x7E\xB2\x5E\x87\x5E\x8C\x9B\x5C\x1C\x5D\x08\x64\x8F\x2D\x8F",
    b"\xE6\x7D\x0B\x43\x97\xCC\xB3\x9C\x97\xA7\x8F\x03\x31\x5F\xBE\x03",
    b"\x3F\x8F\x5F\x7C\xC3\x59\x50\xBF\x5C\x9E\x2B\x56\xB2\x0A\x1F\x1b",
    b"\x7B\x8D\x1D\x7D\x67\x4D\x7D\x8D\x91\x7F\x7D\x0F\x2A\x4D\x9B\x48",
    b"\x78\x28\x9B\x0C\x06\x23\x4B\x2A\x2A\x7D\x9D\x7C\x3C\x1C\x1C\xD3",
    b"\x18\x09\x28\xC6\xAF\x6C\x70\x3F\xBD\x1A\x1C\x8C\x7E\xB0\x6C\x8F",
    b"\x9D\x2B\x5D\x4D\x0C\x84\x3E\x44\x5C\x4E\x2A\x3E\x19\xCC\xCC\x3F",
    b"\xED\x33\xB9\xEF\x6D\xCC\x3D\x2D\x45\x42\x8A\xF5\x16\xF8\x0A\x4A",
    b"\x7B\x6C\xBC\x5C\x21\x5E\x3E\x4B\x7E\x2F\x5F\x5A\x20\x68\x23\xDD",
    b"\x79\x32\x13\x7D\x6A\x2E\x1B\x7E\x20\x4D\x6D\x89\x1E\xD5\x5D\x95",
    b"\x0E\x51\x6B\xF5\x9B\xEE\x9E\xB6\x71\x2F\x5E\x5D\x63\xAC\x89\xD2",
    b"\xED\x8B\xBB\x2D\x80\x8A\x0D\x8F\x35\x3F\x3F\x7B\x0E\x48\x6B\xE5",
]

X19_KEYS = [
    b"MK6mipwmOUedplb6", b"OtEylfId6dyhrfdn", b"VNbhn5mvUaQaeOo9", b"bIEoQGQYjKd02U0J",
    b"fuaJrPwaH2cfXXLP", b"LEkdyiroouKQ4XN1", b"jM1h27H4UROu427W", b"DhReQada7gZybTDk",
    b"ZGXfpSTYUvcdKqdY", b"AZwKf7MWZrJpGR5W", b"amuvbcHw38TcSyPU", b"SI4QotspbjhyFdT0",
    b"VP4dhjKnDGlSJtbB", b"UXDZx4KhZywQ2tcn", b"NIK73ZNvNqzva4kd", b"WeiW7qU766Q1YQZI",
]

KEY_MAP = {
    "g79": G79_KEYS,
    "x19": X19_KEYS,
}

def pick_key(query: int, key_type: str) -> bytes:
    if key_type not in KEY_MAP:
        raise ValueError(f"Unknown key type: {key_type}")
    index = (query >> 4) & 0x0F
    return KEY_MAP[key_type][index]

def g79_http_decrypt(body: bytes) -> bytes:
    if len(body) < 33:
        raise ValueError("Input body too short")

    iv = body[:16]
    key_query = body[-1]
    encrypted_data = body[16:-1]

    raw_key = pick_key(key_query, "g79")
    
    aes_key = bytearray(b ^ 0x7C for b in raw_key)
    cipher = AES.new(bytes(aes_key), AES.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(encrypted_data)

    try:
        decrypted = unpad(decrypted_padded, 16)
    except ValueError:
        decrypted = decrypted_padded
        
    try:
        decrypted_str = decrypted.decode(encoding='utf-8', errors='ignore')
        
        start_idx = -1
        for i, char in enumerate(decrypted_str):
            if char in '{[':
                start_idx = i
                break
        
        if start_idx != -1:
            decoder = json.JSONDecoder()
            _, end_idx = decoder.raw_decode(decrypted_str[start_idx:])
            
            pure_json_str = decrypted_str[start_idx : start_idx + end_idx]
            return pure_json_str.encode('utf-8')
            
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
        pass
    
    return decrypted

def g79_http_encrypt(json_body: bytes, session_key1: bytes = None) -> bytes:
    if session_key1:
        key1 = session_key1
    else:
        key1 = string.rand_string_runes(16).encode('utf-8')
    
    payload = json_body + key1
    
    key2_iv = string.rand_string_runes(16).encode('utf-8')
    key_index = (random.randint(0, 15) << 4) | 0x0C
    raw_server_key = pick_key(key_index, "g79")
    aes_key = bytearray(b ^ 0x7C for b in raw_server_key)
    
    cipher = AES.new(bytes(aes_key), AES.MODE_CBC, key2_iv)
    padded_payload = pad(payload, 16)
    ciphertext = cipher.encrypt(padded_payload)
    
    final_packet = key2_iv + ciphertext + bytes([key_index])
    
    return final_packet

def x19_http_encrypt(body_in: bytes) -> bytes:
    target_len = math.ceil((len(body_in) + 16) / 16) * 16
    body = bytearray(target_len)
    body[:len(body_in)] = body_in
    
    rand_fill = string.rand_string_runes(16).encode('utf-8')
    body[len(body_in):len(body_in)+16] = rand_fill
    
    key_query = (random.randint(0, 15) << 4) | 2
    key = pick_key(key_query, "x19")
    iv = string.rand_string_runes(16).encode('utf-8')
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(bytes(body))
    
    result = bytearray()
    result.extend(iv)
    result.extend(encrypted)
    result.append(key_query)
    
    return bytes(result)

def x19_http_decrypt(body: bytes) -> bytes:
    # remove HTTP Chunked Transfer Encoding
    if len(body) > 5:
        first_line_idx = body.find(b"\r\n")
        if 0 < first_line_idx < 10:
            header = body[:first_line_idx]
            if all(c in b"0123456789abcdefABCDEF" for c in header):
                body = body[first_line_idx+2:]
                if body.endswith(b"\r\n0\r\n\r\n"):
                    body = body[:-7]
                elif body.endswith(b"\r\n"):
                    body = body.rstrip(b"\r\n")

    if len(body) < 33:  # 16(IV) + 16(Scissor) + 1(KeyQuery)
        raise ValueError("Input body too short")
    
    iv = body[:16]
    key_query = body[-1]
    encrypted_data = body[16:-1]
    key = pick_key(key_query, "x19")
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted_data)
    
    # remove padding
    decrypted = decrypted.rstrip(b"\x00")
    
    # remove fixed 16-byte Scissor
    if len(decrypted) < 16:
        raise ValueError("Invalid decrypted data length")
        
    return decrypted[:-16]

def compute_dynamic_token(path: str, body: bytes, token: str) -> str:
    token_md5 = hashlib.md5(token.encode('utf-8')).hexdigest()
    payload = token_md5.encode('utf-8') + body + b"0eGsBkhl" + path.encode('utf-8')
    sum_hex = hashlib.md5(payload).hexdigest()
    sum_bytes = sum_hex.encode('utf-8')
    
    binary_str = ""
    for b in sum_bytes:
        binary_str += bin(b)[2:].zfill(8)

    rotated_binary = binary_str[6:] + binary_str[:6]
    
    final_sum = bytearray(sum_bytes)
    for i in range(len(final_sum)):
        section = rotated_binary[i*8 : i*8+8]
        b_val = 0
        for j in range(8):
            if section[7-j] == '1':
                b_val |= (1 << j)
        final_sum[i] ^= b_val
        
    b64 = base64.b64encode(final_sum).decode('utf-8').replace('=', '')
    result = b64.replace('+', 'm').replace('/', 'o')
    
    return result[:16] + "1"

def pe_auth_sign_old(v: str, sp: int, tr: int) -> str:
    # 常量表 b
    b = bytes([
        0x62, 0x25, 0x1e, 0xf6, 0x40, 0xb3, 0x40, 0xc0, 0x51, 0x5a, 0x5e, 0x26, 0xaa, 0xc7, 0xb6, 0xe9,
        0x44, 0xea, 0xbe, 0xa4, 0xa9, 0xcf, 0xde, 0x4b, 0x60, 0x4b, 0xbb, 0xf6, 0x70, 0xbc, 0xbf, 0xbe,
        0xc3, 0x59, 0x5b, 0x65, 0x92, 0xcc, 0x0c, 0x8f, 0x7d, 0xf4, 0xef, 0xff, 0xd1, 0x5d, 0x84, 0x85,
        0xc6, 0x7e, 0x9b, 0x28, 0xfa, 0x27, 0xa1, 0xea, 0x85, 0x30, 0xef, 0xd4, 0x05, 0x1d, 0x88, 0x04,
        0xe6, 0xcd, 0xe1, 0x21, 0xd6, 0x07, 0x37, 0xc3, 0x87, 0x0d, 0xd5, 0xf4, 0xed, 0x14, 0x5a, 0x45,
    ])
    
    # 位移表 qTable
    q_table = bytes([
        0x01, 0x06, 0x0a, 0x0d, 0x02, 0x05, 0x09, 0x0e, 0x04, 0x07, 0x0b, 0x03, 0x03, 0x08, 0x0b, 0x05,
        0x01, 0x07, 0x0b, 0x0e,
    ])

    if sp < 0 or tr <= 0:
        raise ValueError("invalid sp/tr parameters")
    if 16 * sp + 16 > len(b):
        raise ValueError(f"sp={sp} out of range for constant table")
    if 4 * sp + 4 > len(q_table):
        raise ValueError(f"sp={sp} out of range for shift table")

    # 1. 补齐字符串到 4 字节边界
    rem = len(v) % 4
    if rem != 0:
        v += "0" * (4 - rem)

    # 2. 将字符串转换为大端序 uint32 数组 (p)
    a = v.encode('latin-1')
    p = []
    for i in range(0, len(a), 4):
        # Go 逻辑: uint32(a[i])<<24 | uint32(a[i+1])<<16 | uint32(a[i+2])<<8 | uint32(a[i+3])
        val = struct.unpack('>I', a[i:i+4])[0]
        p.append(val)

    # 3. 补齐 p 到 64 的倍数
    rem_p = len(p) % 64
    if rem_p != 0:
        p.extend([0xabcde987] * (64 - rem_p))

    # 4. 初始化上下文常量 c (小端序)
    c = []
    for i in range(4):
        offset = 16 * sp + i * 4
        c.append(struct.unpack('<I', b[offset:offset+4])[0])

    # 5. 获取位移量 q
    q = list(q_table[4*sp : 4*sp+4])

    # 6. 核心哈希逻辑
    r, u, x, z = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476

    MASK = 0xffffffff

    for t in range(tr):
        for j in range(0, len(p), 4):
            # 第一轮: r
            a1 = (r + ((u & x) | (~u & z))) & MASK
            val1 = (a1 + p[j] + c[0]) & MASK
            shift1 = (val1 << q[0]) & MASK
            r = (u + shift1) & MASK

            # 第二轮: u
            a2 = (r + ((u & z) | (~z & x))) & MASK
            val2 = (a2 + p[j] + c[1]) & MASK
            shift2 = (val2 << q[1]) & MASK
            u = (u + shift2) & MASK

            # 第三轮: x
            a3 = (r + (u ^ x ^ z)) & MASK
            val3 = (a3 + p[j] + c[2]) & MASK
            shift3 = (val3 << q[2]) & MASK
            x = (u + shift3) & MASK

            # 第四轮: z
            term = (x ^ (u | z)) & MASK
            a4 = (r + term) & MASK
            val4 = (a4 + p[j] + c[3]) & MASK
            shift4 = (val4 << q[3]) & MASK
            z = (u + shift4) & MASK

    # 7. 输出转换为字节序列 (小端序) 并进行 Base64 编码
    out = struct.pack('<IIII', r, u, x, z)
    return base64.b64encode(out).decode('utf-8')

def pe_auth_sign(data: str) -> str:
    un_encrypted = data
    while len(un_encrypted) % 4 != 0:
        un_encrypted += "0"

    if len(un_encrypted) > 256:
        raise ValueError("data too big")

    crypto_table = [0xABCDE987] * 64
    
    data_bytes = un_encrypted.encode('ascii')
    groups = len(data_bytes) // 4
    for i in range(groups):
        chunk = data_bytes[i*4 : i*4 + 4]
        crypto_table[i] = struct.unpack(">I", chunk)[0]

    L1 = [0x289B7EC6, 0xEAA127FA, 0xD4EF3085, 0x04881D05]
    L2 = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]
    L3 = [0, 0, 0, 0]
    L4 = [0, 0, 0, 0]

    mask = 0xFFFFFFFF
    
    def offs(p1, p2, bits):
        mask = 0xFFFFFFFF
        # p1 = (p2 >> (32 - bits)) | ((p1 & (mask >> bits)) << bits)
        new_p1 = ((p2 >> (32 - bits)) | (p1 << bits)) & mask
        new_p2 = (p2 << bits) & mask
        return new_p1, new_p2

    for i in range(9):
        for j in range(16):
            L4[3] = crypto_table[j * 4]

            # L4[0] = L1[0] + L2[0] + L4[3] + (~L2[1] & L2[3] | L2[2] & L2[1])
            f1 = ((~L2[1] & L2[3]) | (L2[2] & L2[1])) & mask
            L4[0] = (L1[0] + L2[0] + L4[3] + f1) & mask
            
            # L4[1] = (L4[1] | L3[1] & L3[0]) + L3[3]
            L4[1] = ((L4[1] | (L3[1] & L3[0])) + L3[3]) & mask
            
            L4[1], L4[0] = offs(L4[1], L4[0], 3)

            L2[0] = (L4[0] + L2[1]) & mask
            L3[3] = (L4[1] + L3[0]) & mask
            
            # L4[1] = (~L3[2] & L3[1]) | (L4[0] & L3[0])
            L4[1] = ((~L3[2] & L3[1]) | (L4[0] & L3[0])) & mask
            
            # L4[2] = (~L2[3] & L2[2] | L2[3] & L2[1]) + L1[1] + L4[3] + L2[0]
            f2 = ((~L2[3] & L2[2]) | (L2[3] & L2[1])) & mask
            L4[2] = (f2 + L1[1] + L4[3] + L2[0]) & mask
            
            L4[0] = L4[2]
            L4[1] = (L4[1] + L3[3]) & mask
            
            L4[1], L4[0] = offs(L4[1], L4[0], 8)

            L2[1] = (L4[0] + L2[1]) & mask
            
            # L4[1] = (L3[1] ^ L3[2] ^ (L3[0] + L4[1])) + L3[3]
            L4[1] = ((L3[1] ^ L3[2] ^ ((L3[0] + L4[1]) & mask)) + L3[3]) & mask
            
            # L4[0] = (L2[1] ^ L2[2] ^ L2[3]) + L1[2] + L2[0] + L4[3]
            f3 = (L2[1] ^ L2[2] ^ L2[3]) & mask
            L4[0] = (f3 + L1[2] + L2[0] + L4[3]) & mask
            
            L3[0] = L4[2]
            
            L4[1], L4[0] = offs(L4[1], L4[0], 11)

            L3[1] = (L4[1] + L3[0]) & mask
            L2[2] = (L4[0] + L2[1]) & mask
            
            # L4[1] = ((L3[0] | L3[2]) ^ L3[1]) + L4[2] + L3[3]
            f4 = ((L3[0] | L3[2]) ^ L3[1]) & mask
            L4[1] = (f4 + L4[2] + L3[3]) & mask
            
            # L4[0] = ((L2[3] | L2[1]) ^ L2[2]) + L1[3] + L4[3] + L2[0]
            f5 = ((L2[3] | L2[1]) ^ L2[2]) & mask
            L4[0] = (f5 + L1[3] + L4[3] + L2[0]) & mask
            
            L4[1], L4[0] = offs(L4[1], L4[0], 5)

            L2[3] = (L4[0] + L2[1]) & mask
            L3[2] = (L4[1] + L3[0]) & mask

    result_bytes = struct.pack("<IIII", *L2)
    return base64.b64encode(result_bytes).decode('utf-8')

def get_decrypt_key(user_id: str, content_key: bytes, device_id: str = "123456") -> str:
    if not content_key:
        return content_key
    if not device_id:
        device_id = "123456"
    key = ("TG8hVJD3Lt1r86Cv" + user_id + device_id).encode()

    data_len = len(content_key)
    key_len = len(key)
    
    buffer = bytearray(content_key)
    
    for i in range(key_len - 1, -1, -1):
        target_idx = i % data_len
        buffer[target_idx] ^= key[i]
        
    return bytes(buffer).decode()