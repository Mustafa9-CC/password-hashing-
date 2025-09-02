# -*- coding: utf-8 -*-
import argparse
import hashlib

# parsing
parser = argparse.ArgumentParser(description='Hashing given password(s)')
parser.add_argument('password', nargs='?', help='Input password you want to hash')
parser.add_argument(
    '-t', '--type',
    choices=['sha256', 'sha512', 'md5'],
    help='Type of hashing algorithm (default: sha256)'
)
parser.add_argument(
    '-f', '--file',
    help='File containing passwords (one per line) to hash'
)
parser.add_argument(
    '-o', '--output',
    default='hashed_output.txt',
    help='Output file to save hashed results (default: hashed_output.txt)'
)
args = parser.parse_args()

# ask for hash type if not provided
if not args.type:
    choice = input("Do you want to use default (sha256)? (y/n): ").strip().lower()
    if choice == "y":
        hashtype = "sha256"
    else:
        print("Choose hash type:")
        print("1) sha256 (default)")
        print("2) sha512")
        print("3) md5")
        opt = input("Enter choice (1/2/3): ").strip()
        if opt == "2":
            hashtype = "sha512"
        elif opt == "3":
            hashtype = "md5"
        else:
            hashtype = "sha256"
else:
    hashtype = args.type

hash_func = getattr(hashlib, hashtype)

def hash_password(pwd: str) -> str:
    m = hash_func()
    m.update(pwd.encode())
    return m.hexdigest()

results = []

# Case 1: file input
if args.file:
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            for line in f:
                pwd = line.strip()
                if pwd:  # skip empty lines
                    hashed = hash_password(pwd)
                    result_line = f"{pwd:<20} | < hash-type: {hashtype} > {hashed}"
                    print(result_line)
                    results.append(result_line)
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found")
        exit(1)

# Case 2: single password
else:
    if not args.password:
        args.password = input("Enter password: ")
    pwd = args.password
    hashed = hash_password(pwd)
    result_line = f"< hash-type : {hashtype} > {hashed}"
    print(result_line)
    results.append(result_line)

# Save results to output file
with open(args.output, "w", encoding="utf-8") as out:
    out.write("\n".join(results))

print(f"\n✅ Results saved to {args.output}")
