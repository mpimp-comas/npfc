"""
Module save
================
"""


class Saver:
    """A class for saving DataFrames with molecules to different file types."""

    def __init__(self,
                 shuffle: bool = False,
                 random_seed: int = None,
                 chunk_size: int = None,
                 encode_mols: bool = True,
                 col_mol: str = 'mol'):
        """Create a Saver object with following parameters:

        :param shuffle: randomize records
        :param random_seed: a number for reproducing the shuffling
        :param chunk_size: the maximum number of records per chunk. If this value is unset, no chunking is performed, otherwise each chunk filename gets appended with a suffix: file_XXX.ext.
        :param encode_mols: convert rdkit.Chem.Mol objects to base64 string representation. For HDF format, pandas stops complaining about PerformanceWarning, for csv molecules do not need to parsed again.
        :param col_mol: if molecules need to be encoded, then the encoding is perfomed on this column.
        """
        self._shuffle = shuffle
        self._random_seed = random_seed
        self._chunk_size = chunk_size
        self._encode_mols = encode_mols
        self._col_mol = col_mol

    @property
    def shuffle(self):
        return self._shuffle

    @shuffle.setter
    def shuffle(self, value: bool):
        self._shuffle = value

    @property
    def random_seed(self):
        return self._random_seed

    @random_seed.setter
    def random_seed(self, value: int = None):
        if type(value) is not None and value < 1:
            raise ValueError(f"Error! A positive value was expected for setting random_seed, but got '{value}'")
        self._random_seed = value

    @property
    def chunk_size(self):
        return self._chunk_size

    @chunk_size.setter
    def chunk_size(self, value: int = None):
        if type(value) is not None and value < 1:
            raise ValueError(f"Error! A positive value was expected for setting chunk_size, but got '{value}'")
        self._random_seed = value

    @property
    def encode_mols(self):
        return self._encode_mols

    @encode_mols.setter
    def encode_mols(self, value):
        self._encode_mols = value

    @property
    def col_mol(self):
        return self._col_mol

    @col_mol.setter
    def col_mol(self, value: str):
        self._col_mol = str(value)
