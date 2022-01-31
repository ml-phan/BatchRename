import time
import multiprocessing
import concurrent.futures

start = time.perf_counter()


def do_something(second):
    print(f"Sleeping for {second} seconds")
    time.sleep(second)
    return f"Done Sleeping {second} seconds"


if __name__ == '__main__':
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        seconds = list(range(1, 11))
        # results = [executor.submit(do_something, sec) for sec in seconds]
        results = executor.map(do_something, seconds)
        for f in results:
            print(f)
    # processes = []
    # for _ in range(4):
    #     p = multiprocessing.Process(target=do_something, args=[1.5])
    #     p.start()
    #     processes.append(p)
    # for process in processes:
    #     process.join()

    finish = time.perf_counter()
    print(finish - start)
