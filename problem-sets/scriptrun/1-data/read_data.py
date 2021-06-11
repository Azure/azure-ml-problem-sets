import argparse
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", "-d", default=".", help="Directory containing text file.")
    parser.add_argument("--filename", "-f", help="File to read.")
    args = parser.parse_args()

    fpath = os.path.join(args.data_dir, args.filename)
    print(f"Reading lines in {fpath}")
    
    with open(fpath) as f:
        for line in f.readlines():
            print(line)
