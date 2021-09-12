import numpy as np
import os.path
from . import download

_folder_path = os.path.abspath("./TE_process/")

"""Setup names of data sets"""
_training_sets = []
_test_sets = []
for i in range(22):
    _training_sets.append("d" + str(i).zfill(2) + ".dat")
    _test_sets.append("d" + str(i).zfill(2) + "_te.dat")


def data_exists_check() -> None:
    missing = []
    choice = ''
    if os.path.isdir(_folder_path):
        for f in (_training_sets + _test_sets):
            if not os.path.isfile(os.path.join(_folder_path, f)):
                missing.append(f)
        if len(missing) > 0:
            choice = input(f"The following data sets are missing from the "
                           f"folder: {missing}, would you like to download "
                           f"the data sets again? [y/n] ").lower()
    else:
        choice = input(f"No data set folder at '{_folder_path}' was found, "
                       f"would you like to dowload the data sets and extract "
                       f"to this folder? [y, n] ").lower()
    if choice == 'y':
        download.main()


def set_folder_path(path: str) -> None:
    global _folder_path
    abs_path = os.path.abspath(path)
    if not os.path.isdir(abs_path):
        raise NotADirectoryError
    _folder_path = abs_path


def import_data_set(file_name: str) -> np.ndarray:
    file_path = os.path.join(_folder_path, file_name)
    data = np.loadtxt(file_path)
    if data.shape[0] > data.shape[1]:
        # Enfore column samples and row variables
        data = data.T
    return(data)


def import_sets(sets_to_import: tuple = range(22),
                check_data_exists: bool = True,
                skip_training: bool = False,
                skip_test: bool = False) -> list:
    """
    Takes a sequence of integers from 0-21 and returns a list of tuples
    of (set name, training set, test set)

    Parameters
    ----------
    sets_to_import: iterable or int
        An iterable object containing integers in the range [0, 21] or a single
        integer in that range that indicate the data sets to be imported
    check_data_exists: bool
        Checks that the data sets exist before attempting to import and prompt
        the user to download the data sets if they aren't found
    skip_training: bool
        If true, don't import the training sets
    skip_test: bool
        If true, don't import the test sets
    """

    if isinstance(sets_to_import, int):
        sets_to_import = (sets_to_import)
    if not hasattr(type(sets_to_import), '__iter__'):
        raise TypeError("Expected an iterable object")

    if check_data_exists:
        data_exists_check()

    names = []
    train = []
    test = []
    for val in sets_to_import:
        if not type(val) == int:
            raise TypeError("Expceted an integer value")
        if val > 21 or val < 0:
            raise ValueError("Expected an integer between 0 and 21")

        names.append(f"IDV({int(_training_sets[val][1:3])})")
        if not skip_training:
            train.append(import_data_set(_training_sets[val]))
        if not skip_test:
            test.append(import_data_set(_test_sets[val]))

    # Build return list
    if skip_training and skip_test:
        sets = [tuple([x]) for x in names]
    elif skip_test:
        sets = list(zip(names, train))
    elif skip_training:
        sets = list(zip(names, test))
    else:
        sets = list(zip(names, train, test))
    return(sets)


def import_tep_sets(lagged_samples: int = 2) -> tuple:
    """
    Imports the normal operation training set and 4 of the commonly used test
    sets [IDV(0), IDV(4), IDV(5), and IDV(10)] with only the first 22 measured
    variables and first 11 manipulated variables
    """
    normal_operation = import_sets(0)
    testing_sets = import_sets([4, 5, 10], skip_training=True)

    X = normal_operation[0][1]
    T0 = normal_operation[0][2]
    T4 = testing_sets[0][1]
    T5 = testing_sets[1][1]
    T10 = testing_sets[2][1]

    ignored_var = list(range(22, 41))
    X = np.delete(X, ignored_var, axis=0)
    T0 = np.delete(T0, ignored_var, axis=0)
    T4 = np.delete(T4, ignored_var, axis=0)
    T5 = np.delete(T5, ignored_var, axis=0)
    T10 = np.delete(T10, ignored_var, axis=0)

    # Add lagged samples
    X = add_lagged_samples(X, lagged_samples)
    T0 = add_lagged_samples(T0, lagged_samples)
    T4 = add_lagged_samples(T4, lagged_samples)
    T5 = add_lagged_samples(T5, lagged_samples)
    T10 = add_lagged_samples(T10, lagged_samples)

    return(X, T0, T4, T5, T10)


def add_lagged_samples(data: np.ndarray, lagged_samples: int) -> np.ndarray:
    """
    Takes a matrix X of [x(1), x(2), ..., x(n)] of n samples where each sample
    x(i) = [x_1(i), x_2(i), ..., x_m(n)]^T contains m variables and returns a
    new matrix X* = [x*(1), x*(2), ..., x*(n - d)] of n - d samples where each
    sample x*(i) = [x_1(i + d), x_2(i + d), ..., x_m(i + d), x_1(i + d - 1),
    ..., x_2(i + d - 2), ..., x_m(i)] contains m(d + 1) variables where d is
    the number of lagged samples.
    """
    data_dyn = np.copy(data)
    for i in range(1, lagged_samples + 1):
        rolled = np.roll(data, i, axis=1)
        data_dyn = np.append(data_dyn, rolled, axis=0)
    data = np.delete(data_dyn, range(lagged_samples), axis=1)
    return(data)


if __name__ == "__main__":
    print("This file cannot be run directly, import this module to obtain the",
          "datasets of the Tennessee Eastman process")
