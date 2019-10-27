from __future__ import annotations
import glob
import json
import os
import pandas as pd
from typing import Tuple
try:
    import pymol2
except ImportError:
    pymol2 = None

import bokeh.layouts
import bokeh.models
import bokeh.plotting
import bokeh.models.widgets
import bokeh.resources
import bokeh.embed
from whatsmyblob import constants


result_titles = {
    'corr_coef': 'Correlation coefficient',
    'CATH_domain': 'CATH domain',
    'neighbor_score': 'Neighbour score'
}


def make_dataframe(
        jobid: int,
        result_filename: str = 'result.json',
        folder: str = None
) -> pd.DataFrame:
    if folder is None:
        folder = os.path.join(constants.TEMP_ROOT, str(jobid))
    df = pd.DataFrame()
    filename = os.path.join(
        folder,
        result_filename
    )
    with open(filename, mode='r') as fp:
        d = json.load(fp)
        n_results = len(d)
        keys = d[0].keys()
        for key in keys:
            df[key] = [d[i][key] for i in range(n_results)]
    return df


def make_datatable(
        data_frame: pd.DataFrame
) -> Tuple[
    bokeh.models.widgets.DataTable,
    bokeh.models.ColumnDataSource
]:
    source = bokeh.models.ColumnDataSource(data_frame)
    keys = result_titles.keys()
    columns = [
            bokeh.models.widgets.TableColumn(
                field=key,
                title=result_titles[key],
            )
            for key in keys
        ]
    cath_formater = bokeh.models.widgets.tables.HTMLTemplateFormatter(
        template='<a href="http://beta.cathdb.info/version/v4_2_0/domain/<%= value %>" '
                 'target="_blank"><%= value %></a>'
    )
    columns.append(
        bokeh.models.widgets.TableColumn(
            field='CATH_domain',
            title='CATH link',
            formatter=cath_formater
        )
    )
    data_table = bokeh.models.widgets.DataTable(
        source=source,
        columns=columns,
        width=400,
        height=280
    )
    return data_table, source


def make_plot(
    source: bokeh.models.ColumnDataSource
) -> bokeh.plotting.Figure:
    p1 = bokeh.plotting.figure(
        title="Correlation coefficients of assessed structures"
    )
    p1.grid.grid_line_alpha = 0.3
    p1.xaxis.axis_label = 'Structure'
    p1.yaxis.axis_label = 'Correlation coefficient'
    p1.circle(
        x='index', y='corr_coef',
        source=source,
        fill_color="red",
        size=8
    )
    return p1


def render_mrc_pdb_overlays(
    mrc_filename: str = None,
    result_folder: str = 'test_folder'
) -> None:
    if mrc_filename is None:
        mrc_filename = glob.glob(
            os.path.join(
                result_folder,
                '*.mrc'
            )
        )[0]
    filename_density = os.path.join(
        result_folder,
        mrc_filename
    )
    pymol = pymol2.PyMOL()
    pymol.start()
    for pdb_filename in glob.glob(
        os.path.join(
            result_folder,
            '*.pdb'
        )
    ):
        root_file, _ = os.path.splitext(pdb_filename)
        pymol.cmd.do('reinitialize')
        pymol.cmd.do('bg_color white')
        pymol.cmd.do('hide all')
        pymol.cmd.do('show cartoon')
        pymol.cmd.do('load %s' % filename_density)
        pymol.cmd.do('load %s' % pdb_filename)
        pymol.cmd.do("matrix_copy %s, %s" % (pdb_filename, filename_density))
        pymol.cmd.do('png %s' % root_file + ".png")


def get_rendered_png(
    selected_pdb_filename: str,
    folder: str = './test_folder',
) -> bokeh.models.widgets.Div:
    root_filename, _ = os.path.splitext(selected_pdb_filename)
    filename_png = root_filename + '.png'
    file_url = os.path.join(
            folder,
            filename_png
        )
    file_url = os.path.abspath(file_url)
    div_image = bokeh.models.Div(
        text="""<img src="%s" alt="div_image">""" % file_url,
        width=300, height=300
    )
    return div_image


def generate_html(
        jobid: int,
        title: str = "",
        folder: str = None
):
    if folder is None:
        folder = os.path.join(constants.TEMP_ROOT, str(jobid))
    df = make_dataframe(
        jobid=jobid,
        folder=folder
    )
    data_table, data_source = make_datatable(df)
    results_table = bokeh.layouts.widgetbox(
                children=[
                    data_table
                ],
                sizing_mode='scale_width'
    )
    results_plot = make_plot(data_source)
    if pymol2 is not None:
        render_mrc_pdb_overlays(
            result_folder=folder
        )
    rendered_results = get_rendered_png(
        '1ubq_fit.pdb',
        folder=folder
    )
    # Create a row layout
    layout1 = bokeh.layouts.row(results_table, results_plot)
    layout2 = bokeh.layouts.row(rendered_results)

    # Make a tab with the layout
    tab1 = bokeh.models.Panel(child=layout1, title='Results')
    tab2 = bokeh.models.Panel(child=layout2, title='View')
    tabs = bokeh.models.widgets.Tabs(tabs=[tab1, tab2])

    html = bokeh.embed.file_html(
        models=tabs,
        resources=bokeh.resources.CDN,
        title=title,
        template=os.path.join(
            os.path.dirname(__file__),
            'result_page/template.html'
        )
    )
    return html


if __name__ == "__main__":
    with open('test.html', 'w') as fp:
        fp.write(
            generate_html(
                jobid=1,
                title='Test',
                folder='./test/data/results/'
            )
        )
