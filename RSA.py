import math

# RSA 加密解密算法实现
def is_prime(n):
    """检查一个数是否为素数"""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def mod_inverse(e, phi):
    """计算模反元素（扩展欧几里得算法）"""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("互质条件不满足，模反元素不存在")
    return x % phi

def generate_keys(p, q, e):
    """生成公钥 (e, n) 和私钥 (d, n)"""
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("输入的 p 和 q 必须是素数")
    if p == q:
        raise ValueError("p 和 q 不能相同")

    # 计算 n 和 φ(n)
    n = p * q
    phi = (p - 1) * (q - 1)

    # 确保 e 和 φ(n) 互质
    if math.gcd(e, phi) != 1:
        raise ValueError("e 和 φ(n) 必须互质")

    # 计算私钥 d
    d = mod_inverse(e, phi)

    print(f"公钥 (e, n): ({e}, {n})")
    print(f"私钥 (d, n): ({d}, {n})")
    return (e, n), (d, n)

def encrypt(plaintext, e, n):
    """使用公钥 (e, n) 加密明文"""
    # 将明文转换为整数（简单起见，假设输入是数字）
    m = int(plaintext)
    if m >= n:
        raise ValueError("明文必须小于模数 n")
    # 加密：c = m^e mod n
    ciphertext = pow(m, e, n)
    print(f"加密结果（密文）：{ciphertext}")
    return ciphertext

def decrypt(ciphertext, d, n):
    """使用私钥 (d, n) 解密密文"""
    # 解密：m = c^d mod n
    plaintext = pow(ciphertext, d, n)
    print(f"解密结果（明文）：{plaintext}")
    return plaintext

# 主程序
def main():
    print("欢迎使用 RSA 算法演示！")
    print("请选择操作：")
    print("1. 加密")
    print("2. 解密")
    choice = input("请输入 1 或 2：")

    if choice == '1':
        # 加密模式
        plaintext = input("请输入明文（数字）：")
        p = int(input("请输入第一个素数 p："))
        q = int(input("请输入第二个素数 q："))
        e = int(input("请输入公钥 e（与 (p-1)*(q-1) 互质）："))

        try:
            public_key, private_key = generate_keys(p, q, e)
            ciphertext = encrypt(plaintext, public_key[0], public_key[1])
        except ValueError as e:
            print(f"错误：{e}")

    elif choice == '2':
        # 解密模式
        ciphertext = int(input("请输入密文（数字）："))
        d = int(input("请输入私钥 d："))
        n = int(input("请输入模数 n："))

        try:
            decrypt(ciphertext, d, n)
        except ValueError as e:
            print(f"错误：{e}")

    else:
        print("无效选择，请输入 1 或 2！")

if __name__ == "__main__":
    main()