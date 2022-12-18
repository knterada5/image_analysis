import time
for i in range(100):
    time.sleep(0.2)
    print(f'\r{i}',end="")
print('')
print('end')