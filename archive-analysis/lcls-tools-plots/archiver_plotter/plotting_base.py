from pydantic import BaseModel, PositiveInt, ValidationError
from typing import Annotated, Dict, List, Literal, Tuple
import pandas as pd
import archiver_data_process as data_processor
import matplotlib.pyplot as plt


class FontBase(BaseModel):
    family: str
    color: str
    size: PositiveInt


class LabelBase(BaseModel):
    x_axis: str
    y_axis: str


class PlottingBase(BaseModel):
    # TODO: add docstrings
    pv_dataframes: list[pd.DataFrame]
    df_correlation: pd.DataFrame = None
    pv_x: str = None
    pv_y: str = None
    pv_x_label: str = None
    pv_y_label: str = None
    pv_labels: list[str] = None
    figure_width: PositiveInt = 10
    figure_height: PositiveInt = 7
    figure_title: str = None
    figure_title_font_size: PositiveInt = 28
    is_smart_title: bool = False
    is_smart_axis_labels: bool = False
    figure_title_color: str = "black"
    x_axis_label: str = "Timestamp"
    y_axis_label: str = "PV"
    x_axis_label_color: str = "black"
    y_axis_label_color: str = "black"
    all_label_font_family: str = "DejaVu Sans"
    axis_label_font_size: PositiveInt = 23
    num_axis_ticks: PositiveInt = 4
    x_axis_tick_font_size: PositiveInt = 18
    y_axis_tick_font_size: PositiveInt = 18
    has_smart_timestamps: bool = True
    is_scatter_plot: bool = False
    is_cmap: bool = False
    is_line_and_marker_plot: bool = False
    has_fit_line: bool = False
    marker_size: PositiveInt = 5
    pv_colors: tuple[str] = ("tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple")
    correlation_color: str = "tab:blue"
    line_types: tuple[Literal["solid", "dashed", "dashdot", "dotted"]] = ("solid", "dashed", "dashdot", "dotted")
    correlation_line_type: Literal["solid", "dashed", "dashdot", "dotted"] = "solid"
    marker_types: tuple[Literal[".", ",", "o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "P", "*", "h",
                                "H", "+", "x", "X", "D", "d", "|", "_", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, "none",
                                "None", " ", "", "$...$"]] = ("x", ".", "^", "s", "p", "*")
    correlation_marker_type: Literal[".", ",", "o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "P", "*", "h",
                                     "H", "+", "x", "X", "D", "d", "|", "_", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, "none",
                                     "None", " ", "", "$...$"] = "o"

    class Config:
        """Allow pandas DataFrame as a type."""
        arbitrary_types_allowed = True

    def plot_pv_over_time(self):
        """Plots a nonempty list of PVs over time."""

        assert len(self.pv_dataframes) > 0, "Empty DataFrame given"
        fig, ax = plt.subplots(figsize=(self.figure_width, self.figure_height), layout="constrained")
        # LEGEND LABELS
        if self.pv_labels is not None:
            # rename columns to label names
            for i in range(len(self.pv_dataframes)):
                df_curr = self.pv_dataframes[i]
                df_curr.rename(columns={df_curr.columns[1]: self.pv_labels[i]}, inplace=True)

        # PLOTTING
        for i in range(len(self.pv_dataframes)):  # plot each DataFrame in df_list
            df_curr = self.pv_dataframes[i]  # current DataFrame plotted
            col = df_curr.columns[1]  # y-axis Series for each of the DataFrames
            if not self.is_scatter_plot:  # line plot
                # choose a line type and plot accordingly
                curr_line_type = self.line_types[i % len(self.line_types)]  # cycle through the list
                # marker plot
                if self.is_line_and_marker_plot:
                    ax.plot(df_curr["Timestamp"], df_curr[col], color=self.pv_colors[i % len(self.pv_colors)],
                            linestyle=curr_line_type, label=col,
                            marker=self.marker_types[i % len(self.marker_types)], markersize=self.marker_size)
                # line plot
                else:
                    ax.plot(df_curr["Timestamp"], df_curr[col], color=self.pv_colors[i % len(self.pv_colors)],
                            linestyle=curr_line_type, label=col)
            # scatter plot
            else:
                ax.scatter(df_curr["Timestamp"], df_curr[col], label=col, s=self.marker_size)

        font_x = FontBase(family=self.all_label_font_family, color=self.x_axis_label_color,
                          size=self.axis_label_font_size)
        font_y = FontBase(family=self.all_label_font_family, color=self.y_axis_label_color,
                          size=self.axis_label_font_size)
        font_title = FontBase(family=self.all_label_font_family, color=self.figure_title_color,
                              size=self.figure_title_font_size)

        # LABELS
        ax.legend()
        plt.xlabel(self.x_axis_label, fontdict=font_x.model_dump())
        plt.ylabel(self.y_axis_label, fontdict=font_y.model_dump())
        ax.tick_params(axis="x", labelsize=self.x_axis_tick_font_size)
        ax.tick_params(axis="y", labelsize=self.y_axis_tick_font_size)
        ax.ticklabel_format(axis="y", style='sci', scilimits=(-3, 3))  # scientific notation outside range 10^-3 to 10^3

        # TICKS
        if self.has_smart_timestamps:
            # remove redundant timestamp labels
            xticklabels = data_processor.get_formatted_timestamps(self.pv_dataframes)
            ax.set_xticks(range(len(xticklabels)))  # set a fixed number of ticks to avoid warnings
            ax.set_xticklabels(xticklabels)
        ax.xaxis.set_major_locator(plt.MaxNLocator(self.num_axis_ticks))  # reduce the amount of ticks for both axes
        ax.yaxis.set_major_locator(plt.MaxNLocator(self.num_axis_ticks))

        # TITLE
        if not self.is_smart_title:
            plt.title("PVs vs. Time", fontdict=font_title.model_dump())
        else:
            # create a title using the PV names
            pv_list = [df_curr.columns[1] for df_curr in self.pv_dataframes]
            plt.title(f"{", ".join(pv_list)} vs. Time", fontdict=font_title.model_dump())

        plt.show()

    def plot_pvs_correlation(self):
        assert self.df_correlation is not None, "Empty DataFrame given"
        assert self.pv_x in df_correlation.columns and self.pv_y in df_correlation.columns, \
            "PVs not found in the given DataFrame."

        fig, ax = plt.subplots(figsize=(self.figure_width, self.figure_height), layout="constrained")

        # LEGEND LABELS
        if self.pv_x_label is not None and self.pv_y_label is not None:
            df.rename(columns={pv_x: self.pv_x_label, pv_y: self.pv_y_label}, inplace=True)
        else:
            self.pv_x_label = pv_x
            self.pv_y_label = pv_y

        # PLOTTING
        if not self.is_scatter_plot:  # line plot
            # with marker
            if self.is_line_and_marker_plot:
                ax.plot(df_correlation[self.pv_x_label], df_correlation[self.pv_y_label],
                        color=self.correlation_color, linestyle=self.correlation_line_type,
                        marker=self.correlation_marker_type, markersize=self.marker_size)
            # without marker
            # TODO: fix method with correct parameters
            else:
                ax.plot(df_correlation[pv_xlabel], df_correlation[pv_ylabel], color=correl_color, linestyle=line_type)
        # scatter plot
        else:
            if not is_cmap:
                ax.scatter(df_correlation[pv_xlabel], df_correlation[pv_ylabel], color=correl_color, s=marker_size)
            # colormap plot
            else:
                xy = np.vstack([df_correlation[pv_xlabel], df_correlation[pv_ylabel]])
                z = gaussian_kde(xy)(xy)
                ax.scatter(df_correlation[pv_xlabel], df_correlation[pv_ylabel], c=z, cmap="viridis")
            if is_fit:
                # create a line of best fit
                slope, intercept = np.polyfit(df_correlation[pv_xlabel], df_correlation[pv_ylabel], deg=1)
                ax.axline(xy1=(0, intercept), slope=slope, label=f"y = {slope:.3f}x + {intercept:.3f}", color="red")

        # LABELS
        if smart_labels and pv_xlabel is not None and pv_ylabel is not None:
            self.label_settings["y_axis"] = pv_ylabel
            self.label_settings["x_axis"] = pv_xlabel

        self.set_fonts(label_font, xlabel_color, ylabel_color, title_color, tick_size_x, tick_size_y, title_size,
                       label_size)

        if plot_title is not None:
            plt.title(f"{self.label_settings["y_axis"]} vs. {self.label_settings["x_axis"]}", fontdict=self.font_title)
        else:
            plt.title(f"{plot_title}", fontdict=self.font_title)

        plt.xlabel(self.label_settings["x_axis"], fontdict=self.font_x)
        plt.ylabel(self.label_settings["y_axis"], fontdict=self.font_y)
        ax.tick_params(axis="x", labelsize=self.tick_x_size)
        ax.tick_params(axis="y", labelsize=self.tick_y_size)
        ax.ticklabel_format(axis="y", style='sci', scilimits=(-3, 3))  # scientific notation outside range 10^-3 to 10^3
        ax.xaxis.set_major_locator(plt.MaxNLocator(num_ticks))
        ax.yaxis.set_major_locator(plt.MaxNLocator(num_ticks))

        plt.show()


if __name__ == "__main__":
    toro_pv = data_processor.pv("TORO:GUNB:360:CHRG", "2024/07/01 00:00:00", "2024/07/01 01:00:00")
    df = data_processor.create_df(toro_pv)
    plotter = PlottingBase(pv_dataframes=[df])
    plotter.plot_pv_over_time()
    # changing starting point and re-plotting
    toro_pv.start = "2024/06/30 00:00:00"
    df_new = data_processor.create_df(toro_pv)
    plotter_new = PlottingBase(pv_dataframes=[df_new])
    plotter_new.plot_pv_over_time()

