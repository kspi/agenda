import os
import sys
import time

CACHE_PATH = os.path.join(os.path.dirname(__file__), 'cache')

def get(name, max_age, update_fn):
    filename = os.path.join(CACHE_PATH, name)
    value = None

    def update_value():
        nonlocal value
        try:
            value = update_fn()
            with open(filename, 'wb') as f:
                f.write(value.encode('utf-8'))
        except Exception as e:
            #sys.stderr.write("warning: cache update {} failed: {}\n".format(name, e))
            pass

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
