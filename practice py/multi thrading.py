# threading_example.py
import threading
import time

def worker(name, count):
    for i in range(count):
        print(f"[{name}] working {i+1}/{count}")
        time.sleep(0.5)  # simulate I/O or work

if __name__ == "__main__":
    t1 = threading.Thread(target=worker, args=("Thread-A", 4))
    t2 = threading.Thread(target=worker, args=("Thread-B", 3))

    # Start threads
    t1.start()
    t2.start()

    # Wait for threads to finish
    t1.join()
    t2.join()

    print("Both threads finished.")