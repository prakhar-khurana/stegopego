import argparse
import subprocess
import os
import zlib

def run_binwalk(file_path):
    print(f"Binwalking on {file_path}")
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

def decompress_data(data):
    try:
        decompressed_data = zlib.decompress(data)
        return decompressed_data.decode('utf-8')
    except zlib.error as e:
        print(f"Error decompressing data: {e}")
        return None

def write_to_output_file(data, output_file="output.txt"):
    try:
        with open(output_file, 'w') as f:
            f.write(data)
        print(f"Hidden message written to {output_file}")
    except Exception as e:
        print(f"Error writing to file: {e}")

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
        print("Steganography Results:")
        print(stego_results)
        hidden_message = stego_results.strip()
        write_to_output_file(hidden_message, "stegoveritas_output.txt")
        if "Found message" in stego_results or "Hidden message" in stego_results:
            try:
                start = stego_results.find("Found message:") + len("Found message:")
                end = stego_results.find("\n", start)
                raw_message = stego_results[start:end].strip()
                try:
                    decompressed_message = decompress_data(raw_message.encode())
                    if decompressed_message:
                        print("Decompressed steganography message:")
                        print(decompressed_message)
                        write_to_output_file(decompressed_message)
                    else:
                        print("No compressed data found or error decompressing. Saving original output.")
                        write_to_output_file(raw_message)
                except Exception as e:
                    print(f"Error during decompression: {e}. Saving original output.")
                    write_to_output_file(raw_message)
            except Exception as e:
                print(f"Error extracting hidden message: {e}. Saving original output.")
                write_to_output_file(hidden_message)
        else:
            print("No hidden message found in stego results.")
    else:
        print("No results from stegoveritas.")

if __name__ == "__main__":
    main()
