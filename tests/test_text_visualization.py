import os
import re
import shutil
import unittest
from pathlib import Path
from dianna.visualization.text import highlight_text


class TextExample:
    """Text and explanation for running visualizing tests."""
    original_text = 'Doloremque aliquam totam ut. Aspernatur repellendus autem quia deleniti. Natus accusamus ' \
                    'doloribus et in quam officiis veniam et. '
    explanation = [('ut', 25, -0.06405025896517044),
                   ('in', 102, -0.05127647027074053),
                   ('et', 99, 0.02254588506724936),
                   ('quia', 58, -0.0008216335740370412),
                   ('aliquam', 11, -0.0006268298968242725),
                   ('Natus', 73, -0.0005556223616156406),
                   ('totam', 19, -0.0005126140261410219),
                   ('veniam', 119, -0.0005058379023790869),
                   ('quam', 105, -0.0004573258796550468),
                   ('repellendus', 40, -0.0003253862469633824)]


class TextExampleWithExpectedHtml:
    """Short text and explanation and its expected html output after visualizing."""
    expected_html = '<html><body><span style="background:rgba(255, 0, 0, 0.08)">such</span> ' \
                    '<span style="background:rgba(255, 0, 0, 0.01)">a</span> <span style="background:rgba(0, 0, 255, 0.800000)">' \
                    'bad</span> <span style="background:rgba(0, 0, 255, 0.059287)">movie</span>.</body></html>\n'
    original_text = 'Such a bad movie.'
    explanation = [('bad', 7, -0.4922624307995777),
                   ('such', 0, 0.04637815000309109),
                   ('movie', 11, -0.03648111256069627),
                   ('a', 5, 0.008377155657765745)]


class TextVisualizationTestCase(unittest.TestCase):
    """Suite of tests for visualizing text given text and explanation data."""
    temp_folder = 'temp_text_visualization_test'
    html_file_path = str(Path(temp_folder) / 'output.html')

    def test_text_visualization_html_output_exists(self):
        """Test if any output is generated at all."""
        highlight_text(TextExample.explanation, original_text=TextExample.original_text,
                       output_html_filename=self.html_file_path)

        assert Path(self.html_file_path).exists()

    def test_text_visualization_html_output_contains_text(self):
        """Test if all words in the input are present in the output html."""
        highlight_text(TextExample.explanation, original_text=TextExample.original_text,
                       output_html_filename=self.html_file_path)

        assert Path(self.html_file_path).exists()
        with open(self.html_file_path, encoding='utf-8') as result_file:
            result = result_file.read()
        for word in _split_text_into_words(TextExample.original_text):
            assert word in result

    def test_text_visualization_html_output_is_correct(self):
        """Test if exact html output of visualization is correct."""
        highlight_text(TextExampleWithExpectedHtml.explanation, original_text=TextExampleWithExpectedHtml.original_text,
                       output_html_filename=self.html_file_path)

        assert Path(self.html_file_path).exists()

        with open(self.html_file_path, encoding='utf-8') as result_file:
            result = result_file.read()
        assert result == TextExampleWithExpectedHtml.expected_html

    def test_text_visualization_show_plot(self):
        """Test if it runs while showing the plot."""
        highlight_text(TextExample.explanation, original_text=TextExample.original_text,
                       show_plot=True)

    def setUp(self) -> None:
        os.mkdir(self.temp_folder)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_folder, ignore_errors=True)


def _split_text_into_words(text):
    # regex taken from
    # https://stackoverflow.com/questions/12683201/python-re-split-to-split-by-spaces-commas-and-periods-but-not-in-cases-like
    # explanation: split by \s (whitespace), and only split by commas and
    # periods if they are not followed (?!\d) or preceded (?<!\d) by a digit.
    regex = r'\s|(?<!\d)[,.](?!\d)'
    return re.split(regex, text)
