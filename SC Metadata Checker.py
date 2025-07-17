import sys
import struct

def get_file_info(filepath):
    with open(filepath, "rb") as f:
        data = f.read()

    if len(data) < 6:
        raise ValueError("File too short to contain valid SC header.")

    magic = data[:2]
    if magic != b"SC":
        raise ValueError("Invalid file format (magic != 'SC').")

    raw_version = data[2:6]

    big_endian_version = struct.unpack(">I", raw_version)[0]
    little_endian_version = struct.unpack("<I", raw_version)[0]

    if big_endian_version >= 5:
        used_version = little_endian_version
        version_type = "Little Endian"
    else:
        used_version = big_endian_version
        version_type = "Big Endian"
    
    is_sc2 = used_version >= 5
    is_sc1 = 1 <= used_version < 5
    is_sc0_5 = 1 <= used_version < 3

    return {
        "Magic": magic.decode('ascii'),
        "Raw Version Bytes": raw_version.hex(),
        "Big Endian Version": big_endian_version,
        "Little Endian Version": little_endian_version,
        "Used Version": used_version,
        "Version Format": version_type,
        "File Size": f"{len(data)} bytes",
        "is_sc2": is_sc2,
        "is_sc1": is_sc1,
        "is_sc0.5": is_sc0_5
    }

if __name__ == "__main__":
    for file_path in sys.argv[1:]:
        print(f"\n=== {file_path} ===")
        try:
            info = get_file_info(file_path)
            for key, value in info.items():
                print(f"{key}: {value}")
        except Exception as e:
            print(f"Error: {e}")

    input()
