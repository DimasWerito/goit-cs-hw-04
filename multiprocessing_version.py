import os
import time
import multiprocessing
from multiprocessing import Queue, Manager

KEYWORDS = ["keyword1", "keyword2", "keyword3"]

def search_in_file(file_path, keywords, results):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        for keyword in keywords:
            if keyword in content:
                results[keyword].append(file_path)

def worker(file_list, keywords, results):
    for file_path in file_list:
        search_in_file(file_path, keywords, results)

def main():
    directory = "./text_files"
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".txt")]
    
    num_processes = 4  
    chunk_size = len(files) // num_processes
    file_chunks = [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

    with Manager() as manager:
        results = manager.dict({keyword: manager.list() for keyword in KEYWORDS})

        start_time = time.time()

        processes = []
        for chunk in file_chunks:
            process = multiprocessing.Process(target=worker, args=(chunk, KEYWORDS, results))
            process.start()
            processes.append(process)

        for process in processes:
            process.join()

        end_time = time.time()

        final_results = {keyword: list(files) for keyword, files in results.items()}

        print("Results:", final_results)
        print("Execution Time:", end_time - start_time, "seconds")

if __name__ == "__main__":
    main()
