import time
from multiprocessing import Pool

THREADS = 8
poolQueue = [[12], [22], [32], [42],
             [52], [62], [72], [82]]

for x in range(THREADS):
    for y in range(16):
        poolQueue[x].append(10*x+2+y)

# print(poolQueue)

def threadExec(ls):
    r = []
    for l in ls:
        r.append(exec(l))
    return r

def exec(x):
    time.sleep(0.5)
    return x

if __name__ == '__main__':
    start_time = time.time()

    with Pool(THREADS) as p:
        print(p.map(threadExec, poolQueue))

    elapsed_time = time.time() - start_time
    print("Time elapsed: ", elapsed_time)