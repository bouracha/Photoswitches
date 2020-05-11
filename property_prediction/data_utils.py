"""
Script for loading data
"""

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def load_thermal_data(path):
    """
    Load the SMILES as x-values and the rate of thermal isomerisation as the y-values.

    :param path: path to dataset
    :return: SMILES, rate of thermal isomerisation values
    """

    df = pd.read_csv(path)
    smiles_list = df['SMILES'].to_list()
    thermal_vals = df['rate of thermal isomerisation from Z-E in s-1'].to_numpy()

    # Remove molecules for which the value of thermal isomerisation rate is infinity or not available

    smiles_list = smiles_list[:65]
    thermal_vals = thermal_vals[:65]

    return smiles_list, thermal_vals


def load_e_iso_pi_data(path):
    """
    Load the SMILES as x-values and the E isomer pi-pi* wavelength in nm as the y-values.
    97 molecules with valid experimental values as of 9 May 2020.

    :param path: path to dataset
    :return: SMILES, property
    """

    df = pd.read_csv(path)
    smiles_list = df['SMILES'].to_list()
    smiles_list.remove('C12=CC=CC=C1CCC3=CC=CC=C3/N=N\\2')
    e_iso_pi_vals = df['E isomer pi-pi* wavelength in nm'].to_numpy()
    e_iso_pi_vals = np.delete(e_iso_pi_vals, 31)

    return smiles_list, e_iso_pi_vals


def load_e_iso_n_data(path):
    """
    Load the SMILES as x-values and the E isomer n-pi* wavelength in nm as the y-values.
    96 valid molecules for this property as of 9 May 2020.

    :param path: path to dataset
    :return: SMILES, property
    """

    df = pd.read_csv(path)
    smiles_list = df['SMILES'].to_list()
    smiles_list = smiles_list[0:14] + smiles_list[15:38] + smiles_list[39:]
    e_iso_n_vals = df['E isomer n-pi* wavelength in nm'].to_numpy()
    e_iso_n_vals = np.delete(e_iso_n_vals, np.array([14, 38]))

    return smiles_list, e_iso_n_vals


def load_z_iso_pi_data(path):
    """
    Load the SMILES as x-values and the Z isomer pi-pi* wavelength in nm as the y-values.
    84 valid molecules for this property as of 9 May 2020.

    :param path: path to dataset
    :return: SMILES, property
    """

    df = pd.read_csv(path)
    smiles_list = df['SMILES'].to_list()

    # Remove NaN indices
    smiles_list = smiles_list[0:12] + smiles_list[15:25] + [smiles_list[26]] + smiles_list[28:31] + [smiles_list[33]] + [smiles_list[37]] + smiles_list[42:]
    z_iso_pi_vals = df['Z isomer pi-pi* wavelength in nm'].to_numpy()
    selection = np.concatenate((np.arange(34, 37, 1), np.arange(38, 42, 1)))
    selection = np.concatenate((np.arange(31, 33, 1), selection))
    selection = np.concatenate((np.array([27]), selection))
    selection = np.concatenate((np.array([25]), selection))
    selection = np.concatenate((np.arange(12, 15, 1), selection))
    z_iso_pi_vals = np.delete(z_iso_pi_vals, selection)

    return smiles_list, z_iso_pi_vals


def load_z_iso_n_data(path):
    """
    Load the SMILES as x-values and the Z isomer n-pi* wavelength in nm as the y-values.
    93 valid molecules with this property as of 9 May 2020

    :param path: path to dataset
    :return: SMILES, property
    """

    df = pd.read_csv(path)
    smiles_list = df['SMILES'].to_list()
    smiles_list = smiles_list[0:12] + smiles_list[15:32] + smiles_list[33:41] + smiles_list[42:]
    z_iso_n_vals = df['Z isomer n-pi* wavelength in nm'].to_numpy()
    z_iso_n_vals = np.delete(z_iso_n_vals, np.array([12, 13, 14, 32, 41]))

    return smiles_list, z_iso_n_vals


def transform_data(X_train, y_train, X_test, y_test, n_components=None, use_pca=False):
    """
    Apply feature scaling, dimensionality reduction to the data. Return the standardised and low-dimensional train and
    test sets together with the scaler object for the target values.

    :param X_train: input train data
    :param y_train: train labels
    :param X_test: input test data
    :param y_test: test labels
    :param n_components: number of principal components to keep when use_pca = True
    :param use_pca: Whether or not to use PCA
    :return: X_train_scaled, y_train_scaled, X_test_scaled, y_test_scaled, y_scaler
    """

    x_scaler = StandardScaler()
    X_train_scaled = x_scaler.fit_transform(X_train)
    X_test_scaled = x_scaler.transform(X_test)
    y_scaler = StandardScaler()
    y_train_scaled = y_scaler.fit_transform(y_train.reshape(-1, 1))
    y_test_scaled = y_scaler.transform(y_test.reshape(-1, 1))

    if use_pca:
        pca = PCA(n_components)
        X_train_scaled = pca.fit_transform(X_train_scaled)
        print('Fraction of variance retained is: ' + str(sum(pca.explained_variance_ratio_)))
        X_test_scaled = pca.transform(X_test_scaled)

    return X_train_scaled, y_train_scaled, X_test_scaled, y_test_scaled, y_scaler
