

def get_total_number_of_cases(df, region=None):
    return get_total_number(df, region, 'cases')


def get_total_number_of_deaths(df, region=None):
    return get_total_number(df, region, 'deaths')


def get_total_number_of_hospitalizations(df, region=None):
    return get_total_number(df, region, 'hosps')


def get_deaths_cases_ratio(df, region=None):
    return int(get_total_number_of_cases(df, region) / get_total_number_of_deaths(df, region))


def get_deaths_hospitalizations_ratio(df, region=None):
    return int(get_total_number_of_hospitalizations(df, region) / get_total_number_of_deaths(df, region))


def get_total_number(df, region=None, column=''):

    if 'geoRegion' in df.columns and region is not None:
        df = df[df.geoRegion == region]

    return df[column].sum()
