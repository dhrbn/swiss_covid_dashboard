import json
import urllib.request
import pandas as pd
from datetime import datetime

import figures
import compute


cases_file = "https://www.covid19.admin.ch/api/data/20220302-fq7zytwk/sources/COVID19CasesRawData_AKL10_d.csv"
hosps_file = "https://www.covid19.admin.ch/api/data/20220302-fq7zytwk/sources/COVID19EpiRawData_d.csv"
vacc_file = "https://www.covid19.admin.ch/api/data/20220302-fq7zytwk/sources/COVID19VaccPersons_vaccine.csv"


def get_swiss_df():
    swiss_df_url = "https://raw.githubusercontent.com/empet/Datasets/master/Swiss-synthetic-data.csv"
    return pd.read_csv(swiss_df_url).drop(columns=['2018', '2019'])


def get_jdata():
    swiss_url = 'https://raw.githubusercontent.com/empet/Datasets/master/swiss-cantons.geojson'
    with urllib.request.urlopen(swiss_url) as url:
        jdata = json.loads(url.read().decode())
    return jdata


def convert_date(date_string):
    return datetime.fromisoformat(date_string)


class Controller:
    def __init__(self):
        self.cases_df = pd.read_csv(cases_file)
        self.cases_df['date'] = self.cases_df['date'].apply(convert_date)

        # Adding the total case per day and per region (aggregating the ageRange column)

        df = self.cases_df.groupby(['date', 'geoRegion']).sum()
        df['date'] = [i[0] for i in df.index]
        df['geoRegion'] = [i[1] for i in df.index]
        df['ageRange'] = 'Total'
        self.cases_df = pd.concat([self.cases_df, df], ignore_index=True)
        self.cases_df.sort_values(by=['date'], inplace=True)

        self.hosps_df = pd.read_csv(hosps_file)
        self.hosps_df['date'] = self.hosps_df['date'].apply(convert_date)
        self.hosps_df.sort_values(by=['date'], inplace=True)

        self.vacc_df = pd.read_csv(vacc_file)
        self.vacc_df['date'] = self.vacc_df['date'].apply(convert_date)
        self.vacc_df.sort_values(by=['date'], inplace=True)

        self.regions = list(sorted(set(
            self.cases_df.geoRegion.unique().tolist() +
            self.hosps_df.geoRegion.unique().tolist() +
            self.vacc_df.geoRegion.unique().tolist()
        )))

        self._map_df = get_swiss_df()
        self._jdata = get_jdata()

        self._current_region = 'CH'

    def get_regions(self):
        return ['CH'] + [gr for gr in sorted(self.cases_df.geoRegion.unique()) if gr != 'CH']

    def get_swiss_map_figure(self):
        return figures.get_swiss_map_figure(self._map_df, self._jdata, self._current_region)

    def get_cases_evolution_figure(self):
        return figures.get_cases_evolution_figure(self.cases_df, self._current_region)

    def get_hosps_evolution_figure(self):
        return figures.get_hosps_evolution_figure(self.hosps_df, self._current_region)

    def get_vaccine_evolution_figure(self):
        return figures.get_vaccine_evolution_figure(self.vacc_df, self._current_region)

    def get_vaccination_coverage_figure(self):
        return figures.get_vaccination_coverage_figure(self.vacc_df, self._current_region)

    def get_vaccines_figure(self):
        return figures.get_vaccines_figure(self.vacc_df, self._current_region)

    def get_age_repartition_figure(self):
        return figures.get_age_repartition_figure(self.cases_df, self._current_region)

    def get_total_count_figure(self):
        return figures.get_total_count_figure(self.hosps_df, self._current_region)

    def get_total_number_of_cases(self):
        return compute.get_total_number_of_cases(self.hosps_df, self._current_region)

    def get_total_number_of_deaths(self):
        return compute.get_total_number_of_deaths(self.hosps_df, self._current_region)

    def get_total_number_of_hospitalizations(self):
        return compute.get_total_number_of_hospitalizations(self.hosps_df, self._current_region)

    def get_deaths_cases_ratio(self):
        return compute.get_deaths_cases_ratio(self.hosps_df, self._current_region)

    def get_deaths_hospitalizations_ratio(self):
        return compute.get_deaths_hospitalizations_ratio(self.hosps_df, self._current_region)

    def set_current_region(self, region):
        self._current_region = region

    def get_current_region(self):
        return self._current_region
