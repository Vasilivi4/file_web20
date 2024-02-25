import os
import time
from threading import Thread
from multiprocessing import Pool, cpu_count
import shutil


def normalize(input_str):
    translit_table = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "h",
        "д": "d",
        "е": "e",
        "є": "ie",
        "ж": "zh",
        "з": "z",
        "и": "y",
        "і": "i",
        "ї": "i",
        "й": "i",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "kh",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ь": "",
        "ю": "iu",
        "я": "ia",
    }

    normalized_str = ""
    for char in input_str:
        if char.isalnum() or char in [".", " "]:
            if char in translit_table:
                normalized_str += translit_table[char]
            else:
                normalized_str += char
        else:
            normalized_str += "_"

    return normalized_str


def process_file(args, known_extensions):
    root, filename, folder_path, extensions = args

    file_extension = filename.split(".")[-1].upper()

    if file_extension in extensions["images"]:
        category = "images"
    elif file_extension in extensions["video"]:
        category = "video"
    elif file_extension in extensions["documents"]:
        category = "documents"
    elif file_extension in extensions["audio"]:
        category = "audio"
    elif file_extension in extensions["archives"]:
        category = "archives"
        archive_path = os.path.join(root, filename)
        extract_folder = os.path.join(folder_path, "archives", normalize(filename))
        shutil.unpack_archive(archive_path, extract_folder)
        return
    else:
        category = "unknown"

    known_extensions.add(file_extension)

    src_file_path = os.path.join(root, filename)
    dest_folder = os.path.join(folder_path, category)
    dest_file_path = os.path.join(dest_folder, normalize(filename))

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    shutil.move(src_file_path, dest_file_path)


def sort_folder(folder_path):
    extensions = {
        "images": ("JPEG", "PNG", "JPG", "SVG"),
        "video": ("AVI", "MP4", "MOV", "MKV"),
        "documents": ("DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX"),
        "audio": ("MP3", "OGG", "WAV", "AMR"),
        "archives": ("ZIP", "GZ", "TAR"),
    }

    known_extensions = set()
    args_list = []

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            args_list.append(
                (root, filename, folder_path, extensions, known_extensions)
            )

    with Pool(cpu_count()) as pool:
        pool.starmap(process_file, args_list)

    return known_extensions


def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Processing file: {file_path}")


def factorize(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors


def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_directory, "Хлам")
    num_threads = 4

    threads = []
    for _ in range(num_threads):
        thread = Thread(target=process_folder, args=(folder_path,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    numbers = [128, 256, 512, 1024, 2048]

    start_time = time.time()
    for num in numbers:
        result = factorize(num)
        print(f"Factors of {num}: {result}")
    sync_time = time.time() - start_time
    print(f"Synchronous execution time: {sync_time} seconds")

    start_time = time.time()
    with Pool(cpu_count()) as pool:
        results = pool.map(factorize, numbers)
    parallel_time = time.time() - start_time

    for num, result in zip(numbers, results):
        print(f"Factors of {num}: {result}")
    print(f"Parallel execution time: {parallel_time} seconds")


if __name__ == "__main__":
    main()
