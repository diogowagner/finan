import string
import random
from random import SystemRandom

from django.utils.text import slugify


def random_letters(k=5):
    return ''.join(SystemRandom().choices(
        string.ascii_lowercase + string.digits,
        k=k
    ))

def slugify_new(text, k=5):
    return slugify(text) + '-' + random_letters(k)

def random_color():
    color = '#' + "%06x" % random.randint(0, 0xFFFFFF)
    return color

