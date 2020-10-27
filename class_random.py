from random import choice
from glob import glob

# рандомный стикер из папки
def random_sticker(path):
    lists = glob(path)
    way = choice(lists)
    sticker = open(way, 'rb')
    return sticker
