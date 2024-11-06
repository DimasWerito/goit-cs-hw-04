import os
import threading
import time
from queue import Queue

KEYWORDS = ["keyword1", "keyword2", "keyword3"]

def search_in_file(file_path, keywords, results):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        for keyword in keywords:
            if keyword in content:
                results[keyword].append(file_path)

def worker(file_queue, keywords, results):
    while not file_queue.empty():
        file_path = file_queue.get()
        search_in_file(file_path, keywords, results)
        file_queue.task_done()

def main():
    directory = "./text_files"
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".txt")]
    
    file_queue = Queue()
    results = {keyword: [] for keyword in KEYWORDS}

    for file in files:
        file_queue.put(file)

    start_time = time.time()

    threads = []
    for _ in range(4):  
        thread = threading.Thread(target=worker, args=(file_queue, KEYWORDS, results))
        thread.start()
        threads.append(thread)

    file_queue.join()
    for thread in threads:
        thread.join()

    end_time = time.time()
    
    print("Results:", results)
    print("Execution Time:", end_time - start_time, "seconds")

if __name__ == "__main__":
    main()
