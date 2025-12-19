import math

# 检查一个数是否为素数
def is_prime(n):
    """检查一个数是否为素数"""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# 计算模反元素（扩展欧几里得算法）
def mod_inverse(e, phi):
    """计算模反元素"""
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

# 根据 p 和 q 生成公钥和私钥
def generate_keys(p, q, e):
    """根据两个素数 p 和 q 以及用户输入的 e 生成公钥 (e, n) 和私钥 (d, n)"""
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("输入的 p 和 q 必须是素数")
    if p == q:
        raise ValueError("p 和 q 不能相同")

    # 计算 n 和 φ(n)
    n = p * q
    phi = (p - 1) * (q - 1)

    # 验证 e 是否与 φ(n) 互质
    if math.gcd(e, phi) != 1 or e >= phi or e < 1:
        raise ValueError("e 必须与 φ(n) 互质，且 1 < e < φ(n)")

    # 计算私钥 d
    d = mod_inverse(e, phi)

    print(f"生成的公钥 (e, n): ({e}, {n})")
    print(f"生成的私钥 (d, n): ({d}, {n})")
    return (e, n), (d, n)

# 根据 e 和 n 尝试推导 p 和 q
def derive_p_q(e, n):
    """根据公钥 (e, n) 推导可能的 p 和 q（仅为学习用途）"""
    print(f"尝试从公钥 (e={e}, n={n}) 推导 p 和 q...")
    # 简单的因数分解（仅适用于小 n）
    for p in range(2, int(math.sqrt(n)) + 1):
        if n % p == 0:
            q = n // p
            if is_prime(p) and is_prime(q) and p != q:
                print(f"可能的 p 和 q: p={p}, q={q}")
                phi = (p - 1) * (q - 1)
                if math.gcd(e, phi) == 1:  # 验证 e 与 φ(n) 互质
                    print(f"验证通过：φ(n) = {phi}，e 与 φ(n) 互质")
                else:
                    print("警告：e 与 φ(n) 不互质，密钥可能无效")
                return p, q
    print("无法分解 n，可能是因数过大或输入错误")
    return None, None

# 主程序
def main():
    print("欢迎使用 RSA 密钥生成与推导工具！")
    print("请选择操作：")
    print("1. 根据 p 和 q 及输入的 e 生成公钥和私钥")
    print("2. 根据 e 和 n 推导 p 和 q")
    choice = input("请输入 1或2：")

    if choice == '1':
        # 根据 p 和 q 及输入的 e 生成密钥
        p = int(input("请输入第一个素数 p："))
        q = int(input("请输入第二个素数 q："))
        e = int(input("请输入公钥 e（与 (p-1)*(q-1) 互质）："))
        try:
            public_key, private_key = generate_keys(p, q, e)
        except ValueError as e:
            print(f"错误：{e}")

    elif choice == '2':
        # 根据 e 和 n 推导 p 和 q
        e = int(input("请输入公钥 e："))
        n = int(input("请输入模数 n："))
        try:
            p, q = derive_p_q(e, n)
            if p and q:
                print("推导成功！请验证 p 和 q 是否正确。")
        except ValueError as e:
            print(f"错误：{e}")

    else:
        print("无效选择，请输入 1、2 ！")

if __name__ == "__main__":
    main()