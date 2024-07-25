import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
from archiver_plotter import ArchiverPlotter  # Replace with the correct import


class TestArchiverPlotter(unittest.TestCase):

    def setUp(self):
        self.plotter = ArchiverPlotter()

    def test_set_fonts(self):
        self.plotter.set_fonts('Arial', 'blue', 'red', 'green', 12, 14, 20, 16)
        self.assertEqual(self.plotter.font_x['family'], 'Arial')
        self.assertEqual(self.plotter.font_x['color'], 'blue')
        self.assertEqual(self.plotter.font_y['color'], 'red')
        self.assertEqual(self.plotter.font_title['color'], 'green')
        self.assertEqual(self.plotter.tick_x_size, 12)
        self.assertEqual(self.plotter.tick_y_size, 14)
        self.assertEqual(self.plotter.font_title['size'], 20)
        self.assertEqual(self.plotter.font_x['size'], 16)

    @patch('archiver_plotter.arch.get_values_over_time_range')
    def test_create_df(self, mock_get_values):
        mock_data = {
            'pv1': MagicMock(timestamps=[datetime(2024, 1, 1), datetime(2024, 1, 2)], values=[1, 2])
        }
        mock_get_values.return_value = mock_data

        df = self.plotter.create_df('pv1', '2024/01/01 00:00:00', '2024/01/02 00:00:00')
        self.assertTrue('timestamps' in df.columns)
        self.assertTrue('pv1' in df.columns)
        self.assertEqual(len(df), 2)
        self.assertEqual(df['pv1'].iloc[0], 1)

    def test_create_correlation_df(self):
        df_x = pd.DataFrame({'timestamps': ['2024/01/01 00:00:00', '2024/01/02 00:00:00'], 'pv1': [1, 2]})
        df_y = pd.DataFrame({'timestamps': ['2024/01/01 00:00:00', '2024/01/02 00:00:00'], 'pv2': [3, 4]})

        df_corr = self.plotter.create_correlation_df(df_x, df_y)
        self.assertTrue('pv1' in df_corr.columns)
        self.assertTrue('pv2' in df_corr.columns)
        self.assertEqual(len(df_corr), 2)

    @patch('matplotlib.pyplot.show')
    def test_plot_pv_over_time(self, mock_show):
        df = pd.DataFrame({'timestamps': ['2024/01/01 00:00:00', '2024/01/02 00:00:00'], 'pv1': [1, 2]})
        self.plotter.plot_pv_over_time([df], xlabel="Time", ylabel="PV Value")
        mock_show.assert_called_once()

    @patch('matplotlib.pyplot.show')
    def test_plot_correl(self, mock_show):
        df = pd.DataFrame({'pv1': [1, 2], 'pv2': [3, 4]})
        self.plotter.plot_correl(df, 'pv1', 'pv2')
        mock_show.assert_called_once()

    def test_set_fonts_invalid_inputs(self):
        with self.assertRaises(ValueError):
            self.plotter.set_fonts('Arial', 'invalid_color', 'red', 'green', 12, 14, 20, 16)

    @patch('archiver_plotter.arch.get_values_over_time_range')
    def test_create_df_invalid_date_format(self, mock_get_values):
        with self.assertRaises(ValueError):
            self.plotter.create_df('pv1', 'invalid_date', '2024/01/02 00:00:00')

    def test_create_correlation_df_mismatched_timestamps(self):
        df_x = pd.DataFrame({'timestamps': ['2024/01/01 00:00:00'], 'pv1': [1]})
        df_y = pd.DataFrame({'timestamps': ['2024/01/02 00:00:00'], 'pv2': [2]})

        df_corr = self.plotter.create_correlation_df(df_x, df_y)
        self.assertEqual(len(df_corr), 0)

    def test_plot_pv_over_time_empty_df_list(self):
        with self.assertRaises(ValueError):
            self.plotter.plot_pv_over_time([], xlabel="Time", ylabel="PV Value")

    def test_plot_correl_empty_df(self):
        df = pd.DataFrame()
        with self.assertRaises(ValueError):
            self.plotter.plot_correl(df, 'pv1', 'pv2')

    def test_plot_pv_over_time_different_lengths(self):
        df1 = pd.DataFrame({'timestamps': ['2024/01/01 00:00:00'], 'pv1': [1]})
        df2 = pd.DataFrame({'timestamps': ['2024/01/01 00:00:00', '2024/01/02 00:00:00'], 'pv2': [2, 3]})

        with self.assertRaises(ValueError):
            self.plotter.plot_pv_over_time([df1, df2], xlabel="Time", ylabel="PV Value")

    def test_plot_correl_different_lengths(self):
        df = pd.DataFrame({'pv1': [1], 'pv2': [2, 3]})

        with self.assertRaises(ValueError):
            self.plotter.plot_correl(df, 'pv1', 'pv2')

    def test_create_df_empty_pv_str(self):
        with self.assertRaises(ValueError):
            self.plotter.create_df('', '2024/01/01 00:00:00', '2024/01/02 00:00:00')

    def test_create_df_empty_date_str(self):
        with self.assertRaises(ValueError):
            self.plotter.create_df('pv1', '', '')

    def test_create_correlation_df_empty_df(self):
        df_x = pd.DataFrame()
        df_y = pd.DataFrame()

        df_corr = self.plotter.create_correlation_df(df_x, df_y)
        self.assertTrue(df_corr.empty)

    def test_get_formatted_timestamps_empty_df_list(self):
        formatted = self.plotter.get_formatted_timestamps([])
        self.assertEqual(formatted, [])

    @patch('matplotlib.pyplot.show')
    def test_plot_pv_over_time_no_labels(self, mock_show):
        df = pd.DataFrame({'timestamps': ['2024/01/01 00:00:00', '2024/01/02 00:00:00'], 'pv1': [1, 2]})
        self.plotter.plot_pv_over_time([df])
        mock_show.assert_called_once()

    @patch('matplotlib.pyplot.show')
    def test_plot_correl_no_labels(self, mock_show):
        df = pd.DataFrame({'pv1': [1, 2], 'pv2': [3, 4]})
        self.plotter.plot_correl(df, 'pv1', 'pv2')
        mock_show.assert_called_once()

    def test_set_fonts_partial_input(self):
        self.plotter.set_fonts('Arial', 'blue', 'red', 'green', 12, 14, 20, 16)
        self.plotter.set_fonts('Courier', 'black', 'yellow', 'orange', 10, 12, 18, 14)
        self.assertEqual(self.plotter.font_x['family'], 'Courier')

    def test_create_df_invalid_pv(self):
        with self.assertRaises(KeyError):
            self.plotter.create_df('invalid_pv', '2024/01/01 00:00:00', '2024/01/02 00:00:00')

    @patch('archiver_plotter.arch.get_values_over_time_range')
    def test_create_df_empty_response(self, mock_get_values):
        mock_get_values.return_value = {'pv1': MagicMock(timestamps=[], values=[])}

        df = self.plotter.create_df('pv1', '2024/01/01 00:00:00', '2024/01/02 00:00:00')
        self.assertTrue(df.empty)

    def test_plot_correl_single_point(self):
        df = pd.DataFrame({'pv1': [1], 'pv2': [2]})
        self.plotter.plot_correl(df, 'pv1', 'pv2')
        plt.close()

    def test_plot_pv_over_time_single_point(self):
        df = pd.DataFrame({'timestamps': ['2024/01/01 00:00:00'], 'pv1': [1]})
        self.plotter.plot_pv_over_time([df])
        plt.close()

    def test_set_fonts_large_values(self):
        self.plotter.set_fonts('Arial', 'blue', 'red', 'green', 50, 60, 100, 80)
        self.assertEqual(self.plotter.font_x['size'], 80)
        self.assertEqual(self.plotter.tick_x_size, 50)

    def test_create_df_large_date_range(self):
        with self.assertRaises(ValueError):
            self.plotter.create_df('pv1', '2024/01/01 00:00:00', '2030/01/01 00:00:00')

    def test_plot_pv_over_time_large_marker_size(self):
        df = pd.DataFrame({'timestamps': ['2024/01/01 00:00:00', '2024/01/02 00:00:00'], 'pv1': [1, 2]})
        self.plotter.plot_pv_over_time([df], is_marker=True, marker_size=100)
        plt.close()

    def test_plot_correl_large_marker_size(self):
        df = pd.DataFrame({'pv1': [1, 2], 'pv2': [3, 4]})
        self.plotter.plot_correl(df, 'pv1', 'pv2', is_marker=True, marker_size=100)
        plt.close()

    def test_get_formatted_timestamps_large_df(self):
        df_list = [pd.DataFrame({'timestamps': ['2024/01/01 00:00:00'] * 1000})]
        formatted = self.plotter.get_formatted_timestamps(df_list)
        self.assertEqual(len(formatted), 1000)

    @patch('archiver_plotter.arch.get_values_over_time_range')
    def test_create_df_special_characters(self, mock_get_values):
        mock_data = {
            'pv!@#$%^&*()': MagicMock(timestamps=[datetime(2024, 1, 1), datetime(2024, 1, 2)], values=[1, 2])
        }
        mock_get_values.return_value = mock_data

        df = self.plotter.create_df('pv!@#$%^&*()', '2024/01/01 00:00:00', '2024/01/02 00:00:00')
        self.assertTrue('timestamps' in df.columns)
        self.assertTrue('pv!@#$%^&*()' in df.columns)
        self.assertEqual(len(df), 2)

    @patch('matplotlib.pyplot.show')
    def test_plot_pv_over_time_special_characters(self, mock_show):
        df = pd.DataFrame({'timestamps': ['2024/01/01 00:00:00', '2024/01/02 00:00:00'], 'pv!@#$%^&*()': [1, 2]})
        self.plotter.plot_pv_over_time([df])
        mock_show.assert_called_once()

    @patch('matplotlib.pyplot.show')
    def test_plot_correl_special_characters(self, mock_show):
        df = pd.DataFrame({'pv!@#$%^&*()': [1, 2], 'pv2': [3, 4]})
        self.plotter.plot_correl(df, 'pv!@#$%^&*()', 'pv2')
        mock_show.assert_called_once()

    def test_set_fonts_empty_string(self):
        self.plotter.set_fonts('', '', '', '', 0, 0, 0, 0)
        self.assertEqual(self.plotter.font_x['family'], '')
        self.assertEqual(self.plotter.font_x['color'], '')
        self.assertEqual(self.plotter.font_y['color'], '')
        self.assertEqual(self.plotter.font_title['color'], '')
        self.assertEqual(self.plotter.tick_x_size, 0)
        self.assertEqual(self.plotter.tick_y_size, 0)
        self.assertEqual(self.plotter.font_title['size'], 0)
        self.assertEqual(self.plotter.font_x['size'], 0)


if __name__ == '__main__':
    unittest.main()
