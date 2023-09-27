from src.permutation import triads


for interval in triads(0b101010110101):
    print(bin(interval))