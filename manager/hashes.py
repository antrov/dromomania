import hashlib
from io import BytesIO

import requests
from imagehash import ImageHash, hex_to_hash, phash
from PIL import Image


def get_local_img_hash(file: str) -> ImageHash:
    img = Image.open(file)
    return phash(img)


def get_remote_img_hash(url: str) -> ImageHash:
    response = requests.get(url)
    response.raise_for_status()
    img = Image.open(BytesIO(response.content))
    return phash(img)


def get_url_hash(url: str) -> str:
    return hashlib.md5(url.encode('utf-8')).hexdigest()


def get_min_diff(current_hash: str | ImageHash,
                 other_hashes: [str],
                 max_diff: int) -> str | None:
    if isinstance(current_hash, str):
        current_hash = hex_to_hash(current_hash)
    nearest_hash = None
    min_diff = max_diff + 1
    for hex_hash in other_hashes:
        other_hash = hex_to_hash(hex_hash)
        diff = abs(current_hash - other_hash)
        if (diff <= max_diff and diff < min_diff):
            nearest_hash = other_hash
            min_diff = diff
    return nearest_hash


if __name__ == '__main__':
    hash_a = get_remote_img_hash(
        'https://ireland.apollo.olxcdn.com/v1/files/927invi64y9v1-PL/image;s=600x0;q=50')
    hash_b = get_remote_img_hash(
        'https://i.st-nieruchomosci-online.pl/ht8vrvc/dzialka-budowlana-aleksandrowek.jpg')
    print(abs(hash_a - hash_b))
