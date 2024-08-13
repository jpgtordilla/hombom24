from pydantic import BaseModel, PositiveInt, ValidationError
from typing import Annotated, Dict, List, Literal, Tuple
import pandas as pd


class PlottingBase(BaseModel):
    pv_dataframes: list[pd.DataFrame]
    pv_x: str
    pv_y: str
    pv_x_label: str = None
    pv_y_label: str = None
    pv_labels: list[str] = None
    figure_width: PositiveInt = 10
    figure_height: PositiveInt = 7
    figure_title: str = None
    figure_title_font_size: PositiveInt = 25
    is_smart_title: bool = False
    is_smart_axis_labels: bool = False
    figure_title_color: str = "black"
    x_axis_label: str = "Timestamp"
    y_axis_label: str = "PV"
    x_axis_label_color: str = "black"
    y_axis_label_color: str = "black"
    all_label_font_family: str = "DejaVu Sans"
    axis_label_font_size: PositiveInt = 16
    num_axis_ticks: PositiveInt = 7
    x_axis_tick_font_size: PositiveInt = 10
    y_axis_tick_font_size: PositiveInt = 10
    smart_timestamps: bool = True
    is_scatter_plot: bool = False
    is_cmap: bool = False
    is_line_and_marker_plot: bool = False
    has_fit_line: bool = False
    marker_size: PositiveInt = 5
    pv_colors: tuple[str] = ("tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple")
    line_types: tuple[Literal["solid", "dashed", "dashdot", "dotted"]] = ("solid", "dashed", "dashdot", "dotted")
    marker_types: tuple[Literal[".", ",", "o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "P", "*", "h",
                                "H", "+", "x", "X", "D", "d", "|", "_", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, "none",
                                "None", " ", "", "$...$"]] = ("x", ".", "^", "s", "p", "*")

