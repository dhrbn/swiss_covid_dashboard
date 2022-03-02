
import plotly.graph_objs as go

from display_utils import COLORS


def get_cases_evolution_figure(df, region):

    if 'geoRegion' in df.columns:
        df = df[df.geoRegion == region]

    # if age_range.upper() == 'ALL':
    #     df = df.groupby(['date', 'geoRegion']).sum()
    #     df['date'] = [i[0] for i in df.index]
    #     df['geoRegion'] = [i[1] for i in df.index]
    #     df['ageRange'] = 'All'
    # else:
    #     df = df[df.ageRange == age_range]

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