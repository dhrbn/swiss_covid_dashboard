

def get_total_number_of_cases(df, region):
    return get_total_number(df, region, 'cases')


def get_total_number_of_deaths(df, region):
    return get_total_number(df, region, 'deaths')


def get_total_number_of_hospitalizations(df, region):
    return get_total_number(df, region, 'hosps')


def get_deaths_cases_ratio(df, region):
    return get_total_number_of_deaths(df, region) / get_total_number_of_cases(df, region)


def get_deaths_hospitalizations_ratio(df, region):
    return get_total_number_of_deaths(df, region) / get_total_number_of_hospitalizations(df, region)


def get_total_number(df, region, column):

    if 'geoRegion' in df.columns:
        df = df[df.geoRegion == region]

    return df[column].sum()
