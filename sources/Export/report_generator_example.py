import pandas as pd

import sources.Export.report_util as report_util
import numpy as np
import matplotlib.pyplot as plt


def generate_report(pos: str, dataset: pd.DataFrame) -> report_util.Report:
    report = report_util.Report("TRP Positional Analyzer")

    section = report.add_section(f"Position Group: {pos}")

    paragraph = section.add_paragraph()

    paragraph.append(f"The {pos} player group has {len(dataset)} players. ")
    paragraph.append(f"The dataset is sorted on wRAA - weightedRunsAboveAverage. ")

    paragraph_2 = section.add_paragraph()
    ##########################################################################
    # The following code demonstrates creating a figure directly with the matplotlib API
    ##########################################################################
    figure1 = section.add_figure()

    paragraph_2.append_cross_reference(figure1)
    paragraph_2.append(f" shows the histogram distribution of the numbers in the dataset. ")
    ##########################################################################

    ##########################################################################
    # The following code demonstrates creating a table
    ##########################################################################
    tbl_1 = section.add_table()
    tbl_1.caption = "Dataset Listing"

    tbl_1.set_header(list(dataset.columns.values))
    tbl_1.set_data(dataset.values.tolist())

    paragraph_2.append_cross_reference(report_part=plot_builder(pos, dataset))
    paragraph_2.append(f" TRP - Truncated Runs Produced projection dataset. ")

    ##########################################################################
    # The following code demonstrates creating another section to the report
    ##########################################################################
    section_2 = report.add_section("More Random Data")
    paragraph_3 = section_2.add_paragraph()

    ##########################################################################
    # The following code demonstrates creating a figure directly with the matplotlib API
    ##########################################################################
    figure_2 = section_2.add_figure()

    # Generate some more example data for figure
    dt = 0.01
    t = np.arange(0, 30, dt)
    nse1 = np.random.randn(len(t))  # white noise 1
    nse2 = np.random.randn(len(t))  # white noise 2
    s1 = np.sin(2 * np.pi * 10 * t) + nse1
    s2 = np.sin(2 * np.pi * 10 * t) + nse2

    # The following starts the plot creation using data generated above
    # notice in the next line we access matplotlib's figure object directly
    axs = [figure_2.matplotlib_figure.add_subplot(2, 1, 1), figure_2.matplotlib_figure.add_subplot(2, 1, 2)]
    axs[0].plot(t, s1, t, s2)
    axs[0].set_xlim(0, 2)
    axs[0].set_xlabel('time')
    axs[0].set_ylabel('s1 and s2')
    axs[0].grid(True)

    cxy, f = axs[1].cohere(s1, s2, 256, 1. / dt)
    axs[1].set_ylabel('coherence')
    figure_2.matplotlib_figure.tight_layout()
    ##########################################################################

    paragraph_3.append_cross_reference(figure_2)
    paragraph_3.append(" shows a plot of more random numbers.")
    n_mean = sum(nse1) / len(nse1)
    if n_mean > 1:
        paragraph_3.append("This dataset has a larger mean compared to the baseline dataset. ")
    else:
        paragraph_3.append("This dataset has a smaller mean compared to the baseline dataset. ")
    paragraph_3.append(f"The mean is {n_mean}. ")

    return report


def plot_builder(pos: str, data: pd.DataFrame, ruFig: report_util.Figure) -> plt.Figure:
    xCat: str
    yCat: str
    sCat: str  # size category
    if pos.__contains__("P"):
        xCat = "WHIP"
        yCat = "ERA"
        sCat = "xERA"
    else:
        xCat = "OBP"
        yCat = "SLG"
        sCat = "wRAA"

    # extract the data
    x = data[xCat].to_numpy()
    y = data[yCat].to_numpy()
    # size and color based on wRAA:
    sizes = data[sCat].apply(lambda r: r * 10)
    colors = data[sCat].apply(lambda r: r * 10)

    # plot
    fig, ax = plt.subplots()

    ax.scatter(x, y, s=sizes, c=colors, vmin=0, vmax=100, alpha=0.5)
    # We only want to place the scatter plot labels only for those players that are Free Agents
    for name in data["_name"]:
        if data.fantasyTeam[data["_name"] == name].values[0] == "FA":  # 1st index value holds the string rep
            plt.text(x=data[xCat][data["_name"] == name], y=data[yCat][data["_name"] == name], s=name)
    ax.set_xlabel(xCat)
    ax.set_ylabel(yCat)
    ax.set_title(f'POS: {pos}')
    vline = data[xCat].mean()
    plt.axvline(vline, c='black', ls='-')
    plt.axhline(data[yCat].mean(), c='black', ls='-')
    plt.grid()
    return fig
    plt.show()


if __name__ == "__main__":
    # np.random.seed(19680801)
    dataset = np.random.randn(50)
    report = generate_report(dataset)

    html_generator = report_util.HTMLReportContext("")
    html_generator.generate(report, "example")
