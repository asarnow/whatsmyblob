from __future__ import annotations
import glob
import json
import numpy as np
import os
import pandas as pd
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox, row, grid, column
from bokeh.models.widgets import Div
from bokeh.plotting import figure, Figure
from bokeh.resources import CDN
from bokeh.models import ColumnDataSource, Plot
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.models import Panel
from bokeh.models.widgets import Tabs
from bokeh.embed import file_html
from typing import Dict, List, Tuple
from whatsmyblob import constants


result_titles = {
    'corr_coef': 'Correlation coefficient',
    'CATH_domain': 'CATH domain',
    'neighbor_score': 'Neighbour score'
}


def make_dataframe(
        folder: str = 'test_folder',
        result_filename: str = 'result.json',
) -> pd.DataFrame:
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
) -> Tuple[DataTable, ColumnDataSource]:
    source = ColumnDataSource(data_frame)
    keys = result_titles.keys()
    columns = [
            TableColumn(field=key, title=result_titles[key])
            for key in keys
        ]
    data_table = DataTable(
        source=source,
        columns=columns,
        width=400,
        height=280
    )
    return data_table, source


def make_plot(
    source: ColumnDataSource
) -> Figure:
    p1 = figure(title="Correlation coefficients of assessed structures")
    p1.grid.grid_line_alpha=0.3
    p1.xaxis.axis_label = 'Structure'
    p1.yaxis.axis_label = 'Correlation coefficient'
    p1.circle(
        x='index', y='corr_coef',
        source=source,
        fill_color="red",
        size=8
    )
    return p1


# def render_mrc_pdb_overlays(
#     mrc_filename: str = None,
#     result_folder: str = 'test_folder'
# ) -> None:
#     if mrc_filename is None:
#         mrc_filename = glob.glob(
#             os.path.join(
#                 result_folder,
#                 '*.mrc'
#             )
#         )[0]
#     filename_density = os.path.join(
#         result_folder,
#         mrc_filename
#     )
#     pymol = pymol2.PyMOL()
#     pymol.start()
#     for pdb_filename in glob.glob(
#         os.path.join(
#             result_folder,
#             '*.pdb'
#         )
#     ):
#         root_file, _ = os.path.splitext(pdb_filename)
#         pymol.cmd.do('reinitialize')
#         pymol.cmd.do('bg_color white')
#         pymol.cmd.do('hide all')
#         pymol.cmd.do('show cartoon')
#         pymol.cmd.do('load %s' % filename_density)
#         pymol.cmd.do('load %s' % pdb_filename)
#         pymol.cmd.do('png %s' % root_file + ".png")


def get_rendered_png(
    selected_pdb_filename: str,
    folder: str = './test_folder',
) -> Div:
    root_filename, _ = os.path.splitext(selected_pdb_filename)
    filename_png = root_filename + '.png'
    file_url = os.path.join(
            folder,
            filename_png
        )
    file_url = os.path.abspath(file_url)
    div_image = Div(
        text="""<img src="%s" alt="div_image">""" % file_url,
        width=150, height=150
    )
    return div_image


def generate_html(
        jobid: int,
        title: str = ""
):
    folder = os.path.join(constants.TEMP_ROOT, str(jobid))
    df = make_dataframe(folder=folder)
    data_table, data_source = make_datatable(df)
    results_table = widgetbox(
                children=[
                    data_table
                ],
                sizing_mode='scale_width'
    )
    results_plot = make_plot(data_source)
    # render_mrc_pdb_overlays(
    #     result_folder=folder
    # )
    rendered_results = get_rendered_png(
        '1ubq_fit.pdb',
        folder=folder
    )
    # Create a row layout
    layout1 = row(results_table, results_plot)
    layout2 = row(rendered_results)

    # Make a tab with the layout
    tab1 = Panel(child=layout1, title='Results')
    tab2 = Panel(child=layout2, title='View')
    tabs = Tabs(tabs=[tab1, tab2])

    html = file_html(tabs, CDN, title=title)
    return html

