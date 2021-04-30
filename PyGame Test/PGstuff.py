from tqdm import tqdm
loop = tqdm(total = 500000, position=0, leave = False)
for k in range(500000):
    loop.set_description('Loading...'.format(k))
    loop.update(1)
loop.close()

from tqdm.auto import tqdm
for i in tqdm(range(100001)):
    print('', end = '\r')