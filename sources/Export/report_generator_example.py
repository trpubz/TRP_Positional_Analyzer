import pandas as pd

import sources.Export.report_util as report_util
import numpy as np
import matplotlib.pyplot as plt


def generate_report(pos: str, dataset: pd.DataFrame) -> report_util.Report:
    report = report_util.Report("TRP Positional Analyzer")

    section = report.add_section(f"Position Group: {pos}")

    paragraph = section.add_paragraph()

    paragraph.append(f"The {pos} player group has {len(dataset)} players. ")
    paragraph.append(f"The dataset holds valuable player data to include wRAA and xwOBA. ")
    paragraph.append(f"Weighted Runs Above Average (wRAA) measures the number of offensive runs a player contributes "
                     f"to their team compared to the average player. ")
    paragraph.append(f"Expected Weighted On-base Average (xwOBA) is formulated using exit velocity, launch angle and, "
                     f"on certain types of batted balls, Sprint Speed. The formation of said player's xwOBA isolates "
                     f"the quality of contact, instead of focusing on the real outcomes which carry too much noise. ")
    paragraph_2 = section.add_paragraph()
    ##########################################################################
    # The following code demonstrates creating a figure directly with the matplotlib API
    ##########################################################################
    figure1 = section.add_figure()

    plot_builder(pos=pos, data=dataset, ruFig=figure1)
    figure1.matplotlib_figure.tight_layout()

    paragraph_2.append_cross_reference(figure1)
    paragraph_2.append("Figure shows a scatter plot with On-Base Percentage on the x-axis and Slugging Percentage on "
                       "the y-axis. The volume of the shape is directly correlated to the player's wRAA. The names "
                       "only appear next to the plot point for those players that are "
                       "Free Agents in my Fantasy League. ")
    ##########################################################################

    ##########################################################################
    # The following code demonstrates creating a table
    ##########################################################################
    tbl_1 = section.add_table()
    tbl_1.caption = "Dataset Listing"

    tbl_1.set_header(list(dataset.columns.values))
    tbl_1.set_data(dataset.values)

    paragraph_2.append(f"\n TRP - Truncated Runs Produced projection dataset. ")

    ##########################################################################
    # The following code demonstrates creating another section to the report
    ##########################################################################
    section_2 = report.add_section("Positional Heat Map")
    paragraph_3 = section_2.add_paragraph()

    ##########################################################################
    # The following code demonstrates creating a figure directly with the matplotlib API
    ##########################################################################
    figure_2 = section_2.add_figure()

    stats = ["wOBA", "xwOBA", "Performance"]  # x-axis labels
    trimmedData = dataset.loc[:, ("wOBA", "xwOBA")]  # get the 2 columns I want
    trimmedData["Performance"] = dataset.xwOBA - dataset.wOBA  # add computed column
    npData = trimmedData.to_numpy()  # convert to numpy

    # The following starts the plot creation using data generated above
    # notice in the next line we access matplotlib's figure object directly
    ax = figure_2.matplotlib_figure.add_subplot()
    ax.imshow(npData)  # heatmap
    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(stats)), labels=stats)
    ax.set_yticks(np.arange(len(dataset["_name"])), labels=dataset["_name"].to_numpy())

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    # Loop over data dimensions and create text annotations.
    for i in range(len(dataset["_name"].to_numpy())):
        for j in range(len(stats)):
            text = ax.text(j, i, npData[i, j],
                           ha="center", va="center", color="w")

    ax.set_title("Player Performance Deltas")
    figure_2.matplotlib_figure.tight_layout()

    ##########################################################################

    paragraph_3.append_cross_reference(figure_2)
    paragraph_3.append(" shows a heatmap of player performance.")

    return report


def plot_builder(pos: str, data: pd.DataFrame, ruFig: report_util.Figure):
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
    plt.style.use('fivethirtyeight')
    ax = ruFig.matplotlib_figure.add_subplot()

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
    plt.show()


if __name__ == "__main__":
    # np.random.seed(19680801)
    dataset = np.random.randn(50)
    report = generate_report(dataset)

    html_generator = report_util.HTMLReportContext("")
    html_generator.generate(report, "example")
