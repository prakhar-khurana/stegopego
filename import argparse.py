import argparse
import subprocess
import os
import zlib

def run_binwalk(file_path):
    print(f"binwalking on {file_path}")
    try:
        command = ["binwalk", "-e", file_path]
        result = subprocess.run(command, capture_output=True, text=True)
        return result
    except Exception as e:
        print(f"Error running binwalk: {e}")
        return None

def check(file_path):
    print(f"Checking steganography on {file_path}")
    try:
        stego_result = subprocess.run(['stegoveritas', file_path, '-meta', '-image'], capture_output=True, text=True)
        return stego_result.stdout
    except Exception as e:
        print(f"Error checking steganography: {e}")
        return None

def decompress_data(file_path):
    try:
        with open(file_path, 'rb') as f:
            compressed_stuff = f.read()
            decompressed_data = zlib.decompress(compressed_stuff)
            return decompressed_data.decode('utf-8')
    except Exception as e:
        print(f"Error decompressing data: {e}")
        return None

def parse_arguments():
    parser = argparse.ArgumentParser(description="CLI tool to identify hidden files using steganography or binwalk")
    parser.add_argument('file', type=str, help="The file to analyze")
    return parser.parse_args()

def main():
    args = parse_arguments()
    file_path = args.file

    if not os.path.isfile(file_path):
        print(f"The file {file_path} does not exist.")
        return

    binwalk_results = run_binwalk(file_path)
    if binwalk_results and binwalk_results.stdout:
        print("Binwalk Results:")
        print(binwalk_results.stdout)

    stego_results = check(file_path)
    if stego_results:
        print("Steganography Results")
        print(stego_results)
        readable_message = decompress_data(stego_results)
        if readable_message:
            print("Decompressed steganography message")
            print(readable_message)

if __name__ == "__main__":
    main()
