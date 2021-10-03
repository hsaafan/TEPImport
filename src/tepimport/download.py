import os
import os.path
import urllib.request
import zipfile
import argparse


ZIP_URL = "http://web.mit.edu/braatzgroup/TE_process.zip"
R_ZIP_URL = "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/6C3JR1"


def download_r_data(path: str = ".",
                    file_name: str = "TE_process.zip") -> None:
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from webdriver_manager.firefox import GeckoDriverManager
    import time

    abspath = os.path.abspath(path)
    options = Options()
    options.headless = True

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", abspath)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                           "application/zip")

    driver = webdriver.Firefox(options=options,
                               firefox_profile=profile,
                               executable_path=GeckoDriverManager().install())
    driver.get(R_ZIP_URL)

    time.sleep(3)
    dropdown_btn_cls = "btn.btn-primary.btn-access-dataset.dropdown-toggle"
    dropdown_btn = driver.find_element_by_class_name(dropdown_btn_cls)
    dropdown_btn.click()

    time.sleep(3)
    download_btn = driver.find_element_by_id("datasetForm:j_idt257")
    download_btn.click()

    time.sleep(3)
    accept_btn = driver.find_element_by_id("datasetForm:j_idt2106")
    accept_btn.click()

    time.sleep(3)
    while os.path.isfile(os.path.join(abspath, 'dataverse_files.zip.part')):
        time.sleep(10)
    os.rename('dataverse_files.zip', file_name)


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


def convert_r_to_numpy(path: str = "."):
    import gc
    import pyreadr
    import numpy as np
    folder_name = "TE_process/"
    ff_train_name = 'TEP_FaultFree_Training.RData'
    ff_test_name = 'TEP_FaultFree_Testing.RData'
    f_train_name = 'TEP_Faulty_Training.RData'
    f_test_name = 'TEP_Faulty_Testing.RData'

    abs_path = os.path.abspath(path)
    os.makedirs(folder_name)

    def convert(file_path):
        file = pyreadr.read_r(file_path)
        first_key = list(file.keys())[0]  # Title of data
        data = np.asarray(file[first_key])
        d = {i: data[data[:, 0] == i][:, 3:] for i in np.unique(data[:, 0])}
        return(d)

    # Fault free data
    ff_train = convert(ff_train_name)
    np.savetxt(folder_name + 'd00.dat', ff_train[0], delimiter='   ')
    del ff_train
    gc.collect()
    os.remove(os.path.join(abs_path, ff_train_name))

    ff_test = convert(ff_test_name)
    np.savetxt(folder_name + 'd00_te.dat', ff_test[0], delimiter='   ')
    del ff_test
    gc.collect()
    os.remove(os.path.join(abs_path, ff_test_name))

    # Faulty data
    f_train = convert(f_train_name)
    for i in range(20):
        np.savetxt(folder_name + f'd{i + 1:02}.dat',
                   f_train[i + 1], delimiter='   ')
    del f_train
    gc.collect()
    os.remove(os.path.join(abs_path, f_train_name))


    f_test = convert(f_test_name)
    for i in range(20):
        np.savetxt(folder_name + f'd{i + 1:02}_te.dat',
                   f_test[i + 1], delimiter='   ')
    del f_test
    gc.collect()
    os.remove(os.path.join(abs_path, f_test_name))


def main(url: str = ZIP_URL,
         path: str = ".",
         file_name: str = "TE_process.zip",
         target_path: str = ".",
         use_local: bool = False,
         no_extract: bool = False,
         cleanup: bool = False,
         large_dataset: bool = False,
         verbose: bool = False) -> None:
    if not use_local:
        if verbose: print("Downloading data")
        if large_dataset:
            if verbose: print("The dataset is 1.4GB, it might take a few "
                              "minutes to download")
            download_r_data(path=path, file_name=file_name)
        else:
            download_data(url=url, path=path, file_name=file_name)
    if not no_extract:
        if verbose: print("Extracting files")
        extract_data(path=path, file_name=file_name, target_path=target_path)
        if large_dataset:
            if verbose: print("Converting .RData files to .dat\n"
                              "This will take a few minutes")
            convert_r_to_numpy(path=target_path)
    if cleanup:
        if verbose: print("Removing zip file")
        cleanup_zip(path=path, file_name=file_name)
    if verbose: print("Done!")


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
    parser.add_argument('--large-dataset',
                        help='download the larger dataset files',
                        action='store_true')
    parser.add_argument('-v', '--verbose',
                        help='output progress messages',
                        action='store_true')
    args = parser.parse_args()

    main(url=args.url, path=args.path, file_name=args.name,
         target_path=args.target, use_local=args.use_local,
         no_extract=args.no_extract, cleanup=args.cleanup,
         large_dataset=args.large_dataset, verbose=args.verbose)
