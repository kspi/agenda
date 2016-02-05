import os
import sys
import time
from xdg.BaseDirectory import save_cache_path

def get(name, max_age, update_fn):
    filename = os.path.join(save_cache_path('agenda'), name)
    value = None

    def update_value():
        nonlocal value
        value = update_fn()
        if value is not None:
            with open(filename, 'wb') as f:
                f.write(value.encode('utf-8'))

    def read_cached():
        nonlocal value
        with open(filename, 'rb') as f:
            value = f.read().decode('utf-8')

    if not os.path.exists(filename):
        update_value()
    else:
        age = time.time() - os.path.getmtime(filename)
        if age > max_age:
            update_value()
            if not value:
                read_cached()
        else:
            read_cached()

    return value
