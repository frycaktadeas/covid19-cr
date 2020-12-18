import os
import pickle
import pandas


class Data:
    FILE = None

    def __init__(self):
        self._data = {}

    # Internal methods
    @staticmethod
    def _read_excel(file):
        return pandas.read_excel(file)

    @staticmethod
    def _read_csv(file):
        return pandas.read_csv(file, sep=";")

    # Private methods
    def __get_name(self):
        return os.path.join("library", "cache", type(self).__name__.lower())

    # Visible methods
    def generate(self):
        self._data = self.generate_inner(self.FILE)
        self.dump()

    def data(self):
        if not self._data:
            raise ValueError("Generate data at first!")

        return self._data

    # Cache
    def load(self):
        try:
            return pickle.load(open(f"{self.__get_name()}.pck", "r+b"))

        except FileNotFoundError:
            return self

    def dump(self):
        pickle.dump(self, open(f"{self.__get_name()}.pck", "w+b"))

    # Methods to override
    def generate_inner(self, file):
        raise NotImplementedError


class Coordinates(Data):
    FILE = "data/coordinates/Obce_centroid.xls"

    VILLAGE_CODE = "KOD_OBEC_P"
    CENTROID_X = "INSIDE_X"
    CENTROID_Y = "INSIDE_Y"

    def generate_inner(self, file):
        excel_data = self._read_excel(file)
        current_data = {}

        for num, code in enumerate(excel_data[self.VILLAGE_CODE]):
            current_data[code] = [
                excel_data[self.CENTROID_X][num],
                excel_data[self.CENTROID_Y][num]
            ]

        return current_data


class Covid19(Data):
    FILES = ["data/covid19/obec_new.csv", "data/covid19/obec.csv", "data/covid19/obec_old.csv"]

    DATE = "datum"
    VILLAGE_CODE = "obec_kod"
    DISTRICT_CODE = "okres_kod"
    DAILY_CASES = "nove_pripady"
    ACTUAL_CASES = "aktualne_nemocnych"

    def data(self, compare=False):
        if not self._data:
            raise ValueError("Generate data at first!")

        if compare:
            return self._data

        else:
            return self._data[0]

    def generate(self):
        self._data = []

        for file in self.FILES:
            self._data.append(self.generate_inner(file))

        self.dump()

    def generate_inner(self, file):
        csv_data = self._read_csv(file)
        current_data = {}

        for date, village, district, daily, cases in zip(
                csv_data[self.DATE],
                csv_data[self.VILLAGE_CODE],
                csv_data[self.DISTRICT_CODE],
                csv_data[self.DAILY_CASES],
                csv_data[self.ACTUAL_CASES]):

            if str(village) != "nan":
                # if number not in current_data:
                #     current_data = {}

                if district != "CZ099Y" and village != 999999:
                    if district not in current_data:
                        current_data[district] = {}

                    if village not in current_data[district]:
                        current_data[district][village] = {}

                    # Save information to current village and to current date
                    current_data[district][village][date] = [daily, cases]

        return current_data


class Area(Data):
    FILE = "data/covid19/area_codes.csv"

    VILLAGE_CODE = "obec_kod"
    VILLAGE_NAME = "obec_nazev"
    DISTRICT_CODE = "okres_kod"
    DISTRICT_NAME = "okres_nazev"
    REGION_CODE = "kraj_kod"
    REGION_NAME = "kraj_nazev"

    def generate_inner(self, file):
        csv_data = self._read_csv(file)
        current_data = {}

        for village_code, village_name, district_code, district_name, region_code, region_name in zip(
                csv_data[self.VILLAGE_CODE],
                csv_data[self.VILLAGE_NAME],
                csv_data[self.DISTRICT_CODE],
                csv_data[self.DISTRICT_NAME],
                csv_data[self.REGION_CODE],
                csv_data[self.REGION_NAME]
        ):
            current_data[village_code] = [village_name, district_code, district_name, region_code, region_name]

        return current_data


class Population(Data):
    NAME = "population"
    DIR = "data/pohyb19"

    VILLAGE_CODE = "Číslo\nobce"
    YEAR = "Rok"
    POPULATION = "Stav 31.12."

    def generate(self):
        total_data = {}

        # For every Excel file in dir
        for num, file in enumerate(os.listdir(self.DIR)):
            # Validation, if file is really Excel file
            if file.endswith(".xlsx"):
                filename = os.path.splitext(file)[0]
                total_data[filename] = self.generate_inner(os.path.join(self.DIR, file))

        self._data = total_data
        self.dump()

    def generate_inner(self, file):
        # Load data and select columns
        excel_data = self._read_excel(file)

        # Define variables for current file
        current_data = {}

        # Refactor
        for year, code, population in zip(excel_data[self.YEAR],
                                          excel_data[self.VILLAGE_CODE],
                                          excel_data[self.POPULATION]):
            # If this year is newer than last year
            if year >= 2015:
                # If it is valid
                if population != "-":
                    current_data[code] = population

        return current_data
