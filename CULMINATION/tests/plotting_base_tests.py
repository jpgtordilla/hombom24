import unittest
from pydantic import ValidationError
import pandas as pd
import numpy as np


# TODO: reformat code, test if functional, re-write tests

# Assuming FontBase, LabelBase, and PlottingBase are imported from your module

class TestPlottingBase(unittest.TestCase):

    # Test 1: FontBase Initialization
    def test_fontbase_initialization(self):
        font = FontBase(family="Arial", color="blue", size=12)
        self.assertEqual(font.family, "Arial")
        self.assertEqual(font.color, "blue")
        self.assertEqual(font.size, 12)

    # Test 2: FontBase Validation
    def test_fontbase_validation(self):
        with self.assertRaises(ValidationError):
            FontBase(family="Arial", color="blue", size=-5)

    # Test 3: LabelBase Initialization
    def test_labelbase_initialization(self):
        label = LabelBase(x_axis="Time", y_axis="Value")
        self.assertEqual(label.x_axis, "Time")
        self.assertEqual(label.y_axis, "Value")

    # Test 4: PlottingBase Initialization
    def test_plottingbase_initialization(self):
        df = pd.DataFrame({
            "Timestamp": pd.date_range(start="2023-01-01", periods=5, freq="D"),
            "PV1": np.random.random(5)
        })
        plot = PlottingBase(pv_dataframes=[df])
        self.assertEqual(plot.figure_width, 10)
        self.assertEqual(plot.figure_height, 7)

    # Test 5: PlottingBase Validation
    def test_plottingbase_validation(self):
        with self.assertRaises(ValidationError):
            PlottingBase(pv_dataframes=[], figure_width=-10)

    # Test 6: Plot PVs Over Time
    def test_plot_pv_over_time(self):
        df = pd.DataFrame({
            "Timestamp": pd.date_range(start="2023-01-01", periods=5, freq="D"),
            "PV1": np.random.random(5)
        })
        plot = PlottingBase(pv_dataframes=[df])
        plot.plot_pv_over_time()  # Should run without errors

    # Test 7: Plot PVs Correlation
    def test_plot_pvs_correlation(self):
        df = pd.DataFrame({
            "PVX": np.random.random(5),
            "PVY": np.random.random(5)
        })
        plot = PlottingBase(pv_dataframes=[], df_correlation=df, pv_x="PVX", pv_y="PVY")
        plot.plot_pvs_correlation()  # Should run without errors

    # Test 8: Empty DataFrame for PVs Over Time
    def test_empty_pv_over_time(self):
        with self.assertRaises(AssertionError):
            plot = PlottingBase(pv_dataframes=[])
            plot.plot_pv_over_time()

    # Test 9: Empty DataFrame for Correlation Plot
    def test_empty_pv_correlation(self):
        with self.assertRaises(AssertionError):
            plot = PlottingBase(pv_dataframes=[], df_correlation=pd.DataFrame())
            plot.plot_pvs_correlation()

    # Test 10: Incorrect PV Columns for Correlation
    def test_incorrect_pv_columns_correlation(self):
        df = pd.DataFrame({
            "PVX": np.random.random(5),
            "PVY": np.random.random(5)
        })
        with self.assertRaises(AssertionError):
            plot = PlottingBase(pv_dataframes=[], df_correlation=df, pv_x="PV1", pv_y="PV2")
            plot.plot_pvs_correlation()

    # Test 11: FontBase with Non-string Family
    def test_fontbase_non_string_family(self):
        with self.assertRaises(ValidationError):
            FontBase(family=123, color="blue", size=12)

    # Test 12: Invalid Color for FontBase
    def test_fontbase_invalid_color(self):
        with self.assertRaises(ValidationError):
            FontBase(family="Arial", color=123, size=12)

    # Test 13: Plot PVs with Line and Marker
    def test_plot_pv_with_line_and_marker(self):
        df = pd.DataFrame({
            "Timestamp": pd.date_range(start="2023-01-01", periods=5, freq="D"),
            "PV1": np.random.random(5)
        })
        plot = PlottingBase(pv_dataframes=[df], is_line_and_marker_plot=True)
        plot.plot_pv_over_time()  # Should run without errors

    # Test 14: Plot Scatter Plot
    def test_plot_scatter_plot(self):
        df = pd.DataFrame({
            "Timestamp": pd.date_range(start="2023-01-01", periods=5, freq="D"),
            "PV1": np.random.random(5)
        })
        plot = PlottingBase(pv_dataframes=[df], is_scatter_plot=True)
        plot.plot_pv_over_time()  # Should run without errors

    # Test 15: Plot Correlation with Fit Line
    def test_plot_correlation_with_fit_line(self):
        df = pd.DataFrame({
            "PVX": np.random.random(5),
            "PVY": np.random.random(5)
        })
        plot = PlottingBase(pv_dataframes=[], df_correlation=df, pv_x="PVX", pv_y="PVY", has_fit_line=True)
        plot.plot_pvs_correlation()  # Should run without errors

    # Test 16: Plot with Custom Axis Labels
    def test_plot_with_custom_axis_labels(self):
        df = pd.DataFrame({
            "Timestamp": pd.date_range(start="2023-01-01", periods=5, freq="D"),
            "PV1": np.random.random(5)
        })
        plot = PlottingBase(pv_dataframes=[df], x_axis_label="Custom X", y_axis_label="Custom Y")
        plot.plot_pv_over_time()  # Should run without errors

    # Test 17: Plot with Custom Title
    def test_plot_with_custom_title(self):
        df = pd.DataFrame({
            "Timestamp": pd.date_range(start="2023-01-01", periods=5, freq="D"),
            "PV1": np.random.random(5)
        })
        plot = PlottingBase(pv_dataframes=[df], figure_title="Custom Title")
        plot.plot_pv_over_time()  # Should run without errors

    # Test 18: Plot with Custom Colors
    def test_plot_with_custom_colors(self):
        df = pd.DataFrame({
            "Timestamp": pd.date_range(start="2023-01-01", periods=5, freq="D"),
            "PV1": np.random.random(5)
        })
        plot = PlottingBase(pv_dataframes=[df], pv_colors=("red", "green"))
        plot.plot_pv_over_time()  # Should run without errors

    # Test 19: Plot with Smart Timestamps
    def test_plot_with_smart_timestamps(self):
        df = pd.DataFrame({
            "Timestamp": pd.date_range(start="2023-01-01", periods=5, freq="D"),
            "PV1": np.random.random(5)
        })
        plot = PlottingBase(pv_dataframes=[df], has_smart_timestamps=True)
        plot.plot_pv_over_time()  # Should run without errors

    # Test 20: Plot Correlation with Colormap
    def test_plot_correlation_with_colormap(self):
        df = pd.DataFrame({
            "PVX": np.random.random(50),
            "PVY": np.random.random(50)
        })
        plot = PlottingBase(pv_dataframes=[], df_correlation=df, pv_x="PVX", pv_y="PVY", is_scatter_plot=True,
                            is_cmap=True)
        plot.plot_pvs_correlation()  # Should run without errors


if __name__ == "__main__":
    unittest.main()
