import pickle
from phe import paillier
# 生成Paillier密钥对
public_key, private_key = paillier.generate_paillier_keypair()

with open('result.pkl', 'wb') as file:
    pickle.dump(public_key.encrypt(0), file)

# 保存公钥到文件
file_path_public = 'paillier_public_key.pkl'
with open(file_path_public, 'wb') as file:
    pickle.dump(public_key, file)
print(f"Public key saved to {file_path_public}")

# 保存私钥到文件
file_path_private = 'paillier_private_key.pkl'
with open(file_path_private, 'wb') as file:
    pickle.dump(private_key, file)
print(f"Private key saved to {file_path_private}")