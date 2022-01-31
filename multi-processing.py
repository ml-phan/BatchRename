import time
import multiprocessing
import concurrent.futures

start = time.perf_counter()


def do_something(second):
    print(f"Sleeping for {second} second")
    time.sleep(second)
    print("Done Sleeping")


if __name__ == '__main__':
    start = time.perf_counter()
    processes = []
    for _ in range(4):
        p = multiprocessing.Process(target=do_something, args=[1.5])
        p.start()
        processes.append(p)
    for process in processes:
        process.join()
    finish = time.perf_counter()
    print(finish - start)
