import pickle
from phe import paillier

file_path_private = 'paillier_private_key.pkl'
with open(file_path_private, 'rb') as file:
    private_key = pickle.load(file)

file_path = 'result.pkl'
with open(file_path, 'rb') as file:
    message = pickle.load(file)

result = private_key.decrypt(message)

print("候选人1：", result % (1<<10))
print("候选人2：", (result >> 10) % (1<<10) )
print("候选人3：", (result >> 20) % (1<<10) )
