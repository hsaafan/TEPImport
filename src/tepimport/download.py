import os
import os.path
import urllib.request
import zipfile
import argparse


ZIP_URL = "http://web.mit.edu/braatzgroup/TE_process.zip"


def download_data(url: str = ZIP_URL,
                  path: str = ".",
                  file_name: str = "TE_process.zip") -> None:
    abs_path = os.path.abspath(path)
    file_name = os.path.join(abs_path, file_name)
    urllib.request.urlretrieve(url, file_name)


def extract_data(path: str = ".",
                 file_name: str = "TE_process.zip",
                 target_path: str = ".") -> None:
    abs_path = os.path.abspath(path)
    file_name = os.path.join(abs_path, file_name)

    target_abs_path = os.path.abspath(target_path)
    with zipfile.ZipFile(file_name,"r") as zip:
        zip.extractall(path=target_abs_path)


def cleanup_zip(path: str = ".",
            file_name: str = "TE_process.zip") -> None:
    abs_path = os.path.abspath(path)
    file_name = os.path.join(abs_path, file_name)
    os.remove(file_name)


def main(url: str = ZIP_URL,
         path: str = ".",
         file_name: str = "TE_process.zip",
         target_path: str = ".",
         use_local: bool = False,
         no_extract: bool = False,
         cleanup: bool = False) -> None:
    if not use_local:
        download_data(url=url, path=path, file_name=file_name)
    if not no_extract:
        extract_data(path=path, file_name=file_name, target_path=target_path)
    if cleanup:
        cleanup_zip(path=path, file_name=file_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Parser arguments
    parser.add_argument('--url',
                        help='custom url to download the data from',
                        type=str,
                        default=ZIP_URL
                        )
    parser.add_argument('--path',
                        help='the path to download the zip file to',
                        type=str,
                        default="."
                        )
    parser.add_argument('--target',
                        help='the target path to extract the zip file to',
                        type=str,
                        default="."
                        )
    parser.add_argument('--name',
                        help='the name of the zip file',
                        type=str,
                        default="TE_process.zip")

    parser.add_argument('--use-local',
                        help="extract a local copy of the zip file",
                        action='store_true')
    parser.add_argument('--cleanup',
                        help='delete the zip file after extracting it',
                        action='store_true')
    parser.add_argument('--no-extract',
                        help='download the zip without extracting it',
                        action='store_true')
    args = parser.parse_args()

    main(url=args.url, path=args.path, file_name=args.name,
         target_path=args.target, use_local=args.use_local,
         no_extract=args.no_extract, cleanup=args.cleanup)
