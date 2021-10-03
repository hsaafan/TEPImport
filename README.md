# TEPImport

Utility for quickly downloading and loading the Tennessee Eastman Process data set.

## Small Data Set

The data set is downloaded from the University of Illinois Large Scale Systems Research Laboratory. A copy of the license is included in the zip package downloaded from the site in the file `readme.txt`.

## Large Data Set

The data set is downloaded from the Harvard Dataverse site. By downloading this data, you are agreeing to the terms set out in the Harvard Dataverse site.

The terms can be found in the following link.
https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/6C3JR1

## Quickstart

Install the package using pip.

    pip3 install tepimport

Import the data sets into your code

    import tepimport
    tep = tepimport.import_sets()

Output the data sets

    for name, train, test in tep:
        print(name)
        print(train)
        print(test)

## Downloading the Data

You will be automatically prompted to download the data when trying to import the files into your code. Alternatively, you can run the download module with the following command.

    python3 download.py [-h] [--url URL] [--path PATH] [--target TARGET] [--name NAME] [--use-local] [--cleanup] [--no-extract]

    optional arguments:
    -h, --help       show this help message and exit
    --url URL        custom url to download the data from
    --path PATH      the path to download the zip file to
    --target TARGET  the target path to extract the zip file to
    --name NAME      the name of the zip file
    --use-local      extract a local copy of the zip file
    --cleanup        delete the zip file after extracting it
    --no-extract     download the zip without extracting it

## Module Functions

The `tepimport.py` file provides the utilities for import the data sets into your code.

`data_exists_check() -> None`

        Check that the data set is present in the defined folder path and prompt the user to download the data set if it can't be found.

`set_folder_path(path: str) -> None`

        Change the path of where to look for the data sets

`import_data_set(file_name: str) -> np.ndarray`

        Import a data set file as a numpy array

`import_sets(sets_to_import: tuple, check_data_exists: bool, skip_training: bool, skip_test: bool) -> list`

    Takes a sequence of integers from 0-21 and returns a list of tuples
    of (set name, training set, test set)

    Parameters
    ----------
    sets_to_import: iterable or int
        An iterable object containing integers in the range [0, 21] or a single integer in that range that indicate the data sets to be imported. By default all data sets will be imported.

    check_data_exists: bool
        Checks that the data sets exist before attempting to import and prompt the user to download the data sets if they aren't found. Set to True by default.

    skip_training: bool
        If true, don't import the training sets. Set to False by default.

    skip_test: bool
        If true, don't import the test sets. Set to False by default.

`import_tep_sets(lagged_samples: int) -> tuple`

    Imports the normal operation training set and 4 of the commonly used test sets [IDV(0), IDV(4), IDV(5), and IDV(10)] with only the first 22 measured variables and first 11 manipulated variables. By default, 2 lagged copies are added to the data sets.

`add_lagged_samples(data: np.ndarray, lagged_samples: int) -> np.ndarray`

    Takes a matrix X of [x(1), x(2), ..., x(n)] of n samples where each sample x(i) = [x_1(i), x_2(i), ..., x_m(n)]^T contains m variables and returns a new matrix X* = [x*(1), x*(2), ..., x*(n - d)] of n - d samples where each sample x*(i) = [x_1(i + d), x_2(i + d), ..., x_m(i + d), x_1(i + d - 1), ..., x_2(i + d - 2), ..., x_m(i)] contains m(d + 1) variables where d is the number of lagged samples.
