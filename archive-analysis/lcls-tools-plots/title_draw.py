import matplotlib.pyplot as plt


class TitleDraw:
    """
    A class that creates a plot window with centered text. Used as a transition in-between plots.

    Attributes
    ----------
    title_text: str
        The title of the group of plots that will be centered.
    background_color: str
        The background color of the image.
    """

    def __init__(self, title_text, background_color):
        """Plots the text, sets the background color, and hides the axes."""
        self.title_text = title_text
        self.background_color = background_color
        fig, ax = plt.subplots()
        fig.patch.set_facecolor(self.background_color)
        ax.set_facecolor(self.background_color)
        ax.set_axis_off()
        ax.text(0.5, 0.5, self.title_text, fontweight="bold", va="center", ha="center", fontsize=20)
        plt.show()

