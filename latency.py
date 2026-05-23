import time

def measure_latency(function, *args):

    start = time.time()

    result = function(*args)

    end = time.time()

    latency = end - start

    return result, latency