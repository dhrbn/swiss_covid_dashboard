import figures
from datetime import datetime
import pandas as pd


cases_file = "https://www.covid19.admin.ch/api/data/20220302-fq7zytwk/sources/COVID19CasesRawData_AKL10_d.csv"
hosps_file = "https://www.covid19.admin.ch/api/data/20220302-fq7zytwk/sources/COVID19EpiRawData_d.csv"
vacc_file = "https://www.covid19.admin.ch/api/data/20220302-fq7zytwk/sources/COVID19VaccPersons_vaccine.csv"


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
        self.cases_df = self.cases_df.append(df, ignore_index=True)


        # for date in self.cases_df.date.unique():
        #     df_date = self.cases_df[self.cases_df.date == date]
        #     for region in self.cases_df.geoRegion.unique():
        #         print(date, region)
        #         df_region = df_date[df_date.geoRegion == region]
        #         total_cases = df_region.entries.sum()
        #         dic = dict(
        #             date=date,
        #             geoRegion=region,
        #             ageRange='all',
        #             entries=total_cases,
        #         )
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

        self._current_region = 'CH'

    def get_regions(self):
        return ['CH'] + [gr for gr in sorted(self.cases_df.geoRegion.unique()) if gr != 'CH']

    def get_cases_evolution_figure(self):
        return figures.get_cases_evolution_figure(self.cases_df, self._current_region)

    def set_current_region(self, region):
        self._current_region = region
