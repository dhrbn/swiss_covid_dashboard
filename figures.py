
import plotly.graph_objs as go

from display_utils import COLORS


def get_cases_evolution_figure(df, region):

    if 'geoRegion' in df.columns:
        df = df[df.geoRegion == region]

    gos = []
    for idx, age_range in enumerate(sorted(df.ageRange.unique())):
        df_age = df[df.ageRange == age_range]
        evo_go = go.Scatter(
            x=df_age.date,
            y=df_age.entries,
            name=f"{age_range}",
            text=f"Cases evolution, region {region}, age range {age_range}",
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
        xaxis=dict(
            title='Time',
        ),
        yaxis=dict(
            title=f"Cases",
        ),
        title=dict(
            text=f'Covid cases evolution for region {region}',
        )
        # font=dict(
        #     family='century gothic',
        # ),
    )

    return go.Figure(data=gos, layout=layout)


def get_hosps_evolution_figure(df, region):

    if 'geoRegion' in df.columns:
        df = df[df.geoRegion == region]

    gos = []
    for idx, column in enumerate(['hosps', 'deaths']):
        evo_go = go.Scatter(
            x=df.date,
            y=df[column],
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
        xaxis=dict(
            title='Time',
        ),
        yaxis=dict(
            title=f"Count",
        ),
        title=dict(
            text=f'Deaths and hospitalizations evolution for region {region}',
        )
        # font=dict(
        #     family='century gothic',
        # ),
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
            y=df_type.sumTotal,
            name=f"{vaccine_type}",
            text=f"Cases evolution, region {region}, vaccine type {vaccine_type}",
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
        xaxis=dict(
            title='Time',
        ),
        yaxis=dict(
            title=f"Cases",
        ),
        title=dict(
            text=f'Vaccination evolution for region {region}',
        )
        # font=dict(
        #     family='century gothic',
        # ),
    )

    return go.Figure(data=gos, layout=layout)
