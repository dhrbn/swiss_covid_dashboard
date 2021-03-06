
import plotly.graph_objs as go

import compute
from display_utils import COLORS, MAIN_COLOR, MIDDLE_GRAY, BLACK


def apply_moving_average(serie, size=7):
    return serie.rolling(window=size).mean()


def get_swiss_map_figure(map_df, jdata, current_region):

    colorscale = [
        [0, MAIN_COLOR],
        [0.5, MAIN_COLOR],
        [1, MIDDLE_GRAY]
    ]

    if current_region in ['CH', 'CHFL']:
        map_df['mask'] = 0.5
    else:
        map_df['mask'] = [0 if row['canton-id'] == current_region else 1 for i, row in map_df.iterrows()]

    gos = []
    map_go = go.Choroplethmapbox(
        geojson=jdata,
        locations=map_df['canton-id'],
        z=map_df['mask'],
        featureidkey='properties.id',
        colorscale=colorscale,
        showscale=False,
        marker=dict(opacity=0.75)
    )
    gos.append(map_go)

    layout = dict(
        mapbox=dict(
            style="white-bg",
            zoom=6.1,
            center=dict(lat=46.8181877, lon=8.2275124),
        ),
        xaxis=dict(
            fixedrange=True,
        ),
        yaxis=dict(
            fixedrange=True,
        ),
        dragmode=False,
        margin=dict(l=10, r=10, t=10, b=10),
    )

    return go.Figure(data=gos, layout=layout)


def get_cases_evolution_figure(df, region):

    if 'geoRegion' in df.columns:
        df = df[df.geoRegion == region]

    iter_list = ['Total'] + [l for l in sorted(df.ageRange.unique()) if l != 'Total']

    gos = []
    step = 0  # step is used to apply COLORS[2] to "Total" age range, to be coherent with the total count figure
    for idx, age_range in enumerate(iter_list):
        if idx == 1:
            step -= 1
        elif idx == 3:
            step += 1
        df_age = df[df.ageRange == age_range]
        evo_go = go.Scatter(
            x=df_age.date,
            y=apply_moving_average(df_age.entries),
            name=f"{age_range}",
            text=f"Cases evolution, region {region}, age range {age_range}",
            xaxis='x',
            yaxis='y',
            line=dict(
                # width=2,
                color=COLORS[idx + step] if age_range != 'Total' else COLORS[2],
            ),
            hoverlabel=dict(
                namelength=-1,
            )
        )
        gos.append(evo_go)

    layout = dict(
        template="plotly_white",
        annotations=[],
        showlegend=True,
        yaxis=dict(
            title=f"Cases",
        ),
        margin=dict(l=10, r=10, t=10, b=10),
    )

    return go.Figure(data=gos, layout=layout)


def get_hosps_evolution_figure(df, region):

    if 'geoRegion' in df.columns:
        df = df[df.geoRegion == region]

    gos = []
    for idx, column in enumerate(['hosps', 'deaths']):
        evo_go = go.Scatter(
            x=df.date,
            y=apply_moving_average(df[column]),
            name=f"{'Hospitalizations' if column.upper() == 'HOSPS' else 'Deaths'}",
            text=f"{'Hospitalizations' if column.upper() == 'HOSPS' else 'Deaths'} evolution, region {region}",
            xaxis='x',
            yaxis='y',
            line=dict(
                # width=2,
                color=COLORS[idx],
            ),
            hoverlabel=dict(
                namelength=-1,
            )
        )
        gos.append(evo_go)

    layout = dict(
        template="plotly_white",
        annotations=[],
        showlegend=True,
        yaxis=dict(
            title=f"Count",
        ),
        margin=dict(l=10, r=10, t=10, b=10),
    )

    return go.Figure(data=gos, layout=layout)


def get_vaccine_evolution_figure(df, region):
    if 'geoRegion' in df.columns:
        df = df[df.geoRegion == region]

    all_vaccine_df = df.groupby(['date', 'geoRegion', 'type']).sum()
    all_vaccine_df['date'] = [i[0] for i in all_vaccine_df.index]
    all_vaccine_df['geoRegion'] = [i[1] for i in all_vaccine_df.index]
    all_vaccine_df['type'] = [i[2] for i in all_vaccine_df.index]

    gos = []
    for idx, vaccine_type in enumerate(sorted(all_vaccine_df.type.unique())):
        df_type = all_vaccine_df[all_vaccine_df.type == vaccine_type]
        evo_go = go.Scatter(
            x=df_type.date,
            y=apply_moving_average(df_type.sumTotal),
            name=f"{vaccine_type}",
            text=f"Cases evolution, region {region}, vaccine type {vaccine_type}",
            xaxis='x',
            yaxis='y',
            line=dict(
                color=COLORS[idx],
            ),
            hoverlabel=dict(
                namelength=-1,
            )
        )
        gos.append(evo_go)

    layout = dict(
        template="plotly_white",
        annotations=[],
        showlegend=True,
        yaxis=dict(
            title=f"Count",
        ),
        margin=dict(l=10, r=10, t=20, b=20),
    )

    return go.Figure(data=gos, layout=layout)


def get_vaccination_coverage_figure(df, region):
    if 'geoRegion' in df.columns:
        df = df[df.geoRegion == region]

    total_pop = df.iloc[-1]['pop']
    df = df[df.type == 'COVID19FullyVaccPersons']

    all_vaccine_df = df.groupby(['date', 'geoRegion', 'type']).sum()
    all_vaccine_df['date'] = [i[0] for i in all_vaccine_df.index]
    all_vaccine_df['geoRegion'] = [i[1] for i in all_vaccine_df.index]
    all_vaccine_df['type'] = [i[2] for i in all_vaccine_df.index]

    total_vaccines = all_vaccine_df.iloc[-1]['sumTotal']

    labels = ['Vaccinated', 'Non-vaccinated']
    values = [100 * total_vaccines / total_pop, 100 * (1 - total_vaccines / total_pop)]
    colors = [MAIN_COLOR, MIDDLE_GRAY]

    gos = []
    pie_go = go.Pie(labels=labels, values=values, hole=.5, marker=dict(colors=colors), textinfo='label')
    gos.append(pie_go)
    layout = dict(
        template="plotly_white",
        annotations=[],
        showlegend=False,
        margin=dict(l=10, r=10, t=20, b=20),
    )

    return go.Figure(data=gos, layout=layout)


def get_vaccines_figure(df, region):
    if 'geoRegion' in df.columns:
        df = df[df.geoRegion == region]

    df = df[df.type == 'COVID19FullyVaccPersons']

    all_vaccine_df = df.groupby(['date', 'geoRegion', 'type']).sum()
    all_vaccine_df['date'] = [i[0] for i in all_vaccine_df.index]
    all_vaccine_df['geoRegion'] = [i[1] for i in all_vaccine_df.index]
    all_vaccine_df['type'] = [i[2] for i in all_vaccine_df.index]

    total_vaccines = all_vaccine_df.iloc[-1]['sumTotal']

    labels = []
    values = []
    colors = []
    for idx, vaccine in enumerate(sorted(df.vaccine.unique())):
        df_vaccine = df[df.vaccine == vaccine]
        labels.append(vaccine)
        values.append(100 * df_vaccine.iloc[-1]['sumTotal'] / total_vaccines)
        colors.append(COLORS[idx])

    gos = []
    pie_go = go.Pie(labels=labels, values=values, hole=.5, marker=dict(colors=colors), textinfo='label')
    gos.append(pie_go)
    layout = dict(
        template="plotly_white",
        annotations=[],
        showlegend=False,
        margin=dict(l=10, r=10, t=20, b=20),
    )

    return go.Figure(data=gos, layout=layout)


def get_age_repartition_figure(df, region):
    if 'geoRegion' in df.columns:
        df = df[df.geoRegion == region]

    max_date = df.date.max()
    df = df[(df.date == max_date) & (df.ageRange != 'Total')]

    total_cases = df.entries.sum()

    labels = []
    values = []
    colors = []
    for idx, age_range in enumerate(sorted(df.ageRange.unique())):
        df_age = df[df.ageRange == age_range]
        labels.append(age_range)
        values.append(100 * df_age.iloc[0]['entries'] / total_cases)
        colors.append(COLORS[idx])

    gos = []
    pie_go = go.Pie(labels=labels, values=values, hole=.5, marker=dict(colors=colors), textinfo='label')
    gos.append(pie_go)
    layout = dict(
        template="plotly_white",
        annotations=[],
        showlegend=False,
        margin=dict(l=10, r=10, t=20, b=20),
    )

    return go.Figure(data=gos, layout=layout)


def get_total_count_figure(df, region):
    if 'geoRegion' in df.columns:
        df = df[df.geoRegion == region]

    dic = dict(
        cases=dict(
            value=compute.get_total_number_of_cases(df),
            color=COLORS[2],
            name='Cases',
        ),
        hosps=dict(
            value=compute.get_total_number_of_hospitalizations(df),
            color=COLORS[0],
            name='Hospitalizations',
        ),
        deaths=dict(
            value=compute.get_total_number_of_deaths(df),
            color=COLORS[1],
            name='Deaths',
        ),
    )

    gos = []
    annotations = []
    for v in dic.values():
        bar_go = go.Bar(
            x=[v['name']],
            y=[v['value']],
            name=v['name'],
            marker_color=v['color'],
        )
        gos.append(bar_go)

        annotation = dict(
            x=v['name'],
            y=v['value'],
            text=f"<b>{v['value']}</b>",
            # xref='paper',
            # yref='paper',
            align='center',
            xanchor="center",
            yanchor="bottom",
            showarrow=False,
            font=dict(
                # family='century gothic',
                size=14,
                color=v['color'],
            )
        )
        annotations.append(annotation)

    layout = dict(
        template="plotly_white",
        annotations=annotations,
        showlegend=False,
        margin=dict(l=10, r=10, t=20, b=20),
    )

    return go.Figure(data=gos, layout=layout)
