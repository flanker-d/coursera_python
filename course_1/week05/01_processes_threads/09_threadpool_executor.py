from concurrent.futures import ThreadPoolExecutor, as_completed

def f(a):
    return a * a

with ThreadPoolExecutor(max_workers=3) as pool:
    results = [pool.submit(f, i) for i in range(10)]
    #submit creates concurrent.futures.future

    for future in as_completed(results): #wait asap (as_completed)
        print(future.result())