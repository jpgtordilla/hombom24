from pydantic import BaseModel, PositiveInt, ValidationError
from typing import Annotated, Dict, List, Literal, Tuple
import pandas as pd


class PlottingBase(BaseModel):
    pv_dataframes: list[pd.DataFrame]
    pv_labels: list[str] = None
    figure_width: PositiveInt = 10
    figure_height: PositiveInt = 7
    figure_title: str = None
    figure_title_font_size: PositiveInt = 25
    is_smart_title: bool = False
    figure_title_color: str = "black"
    x_axis_label: str = "Timestamp"
    y_axis_label: str = "PV"
    x_axis_label_color: str = "black"
    y_axis_label_color: str = "black"
    all_label_font_family: str = "Helvetica"
    axis_label_font_size: PositiveInt = 16
    num_axis_ticks: PositiveInt = 7
    x_axis_tick_font_size: PositiveInt = 10
    y_axis_tick_font_size: PositiveInt = 10
    smart_timestamps: bool = True
    is_scatter_plot: bool = False
    is_line_and_marker_plot: bool = False
    marker_size: PositiveInt = 5
    pv_colors: tuple[str] = ("tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple")
    line_types: tuple[Literal["solid", "dashed", "dashdot", "dotted"]] = ("solid", "dashed", "dashdot", "dotted")
    # TODO: ADD LITERALS
    marker_types: tuple[str] = ("x", ".", "^", "s", "p", "*")

