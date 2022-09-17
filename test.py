import os

res = os.listdir('media/img')

for i in res:
    os.remove(os.path.join('./media/img/', i))

