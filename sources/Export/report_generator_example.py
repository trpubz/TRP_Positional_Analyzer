import report_util
import numpy as np


def generate_report(dataset):
    report = report_util.Report("Random Number Dataset Report")

    section = report.add_section("Dataset Stats")

    paragraph = section.add_paragraph()
    mean = sum(dataset) / len(dataset)
    standard_deviation = dataset.std()

    paragraph.append(f"The dataset has {len(dataset)} numbers. ")
    paragraph.append(f"The largest number in the dataset is {max(dataset)}. ")
    paragraph.append(f"The smallest number in the dataset is {min(dataset)}. ")
    paragraph.append(f"The dataset average value is {mean} with a standard deviation of {standard_deviation}. ")

    paragraph_2 = section.add_paragraph()
    ##########################################################################
    # The following code demonstrates creating a figure directly with the matplotlib API
    ##########################################################################
    figure_1 = section.add_figure()
    figure_1.caption = "Dataset Histogram"
    # notice in the next line we access matplotlib's figure object directly
    ax = figure_1.matplotlib_figure.add_subplot(1, 1, 1)
    ax.hist(dataset)
    ax.set_xlabel("Number Values")
    ax.set_ylabel("Count")
    figure_1.matplotlib_figure.tight_layout()

    paragraph_2.append_cross_reference(figure_1)
    paragraph_2.append(f" shows the histogram distribution of the numbers in the dataset. ")
    ##########################################################################

    ##########################################################################
    # The following code demonstrates creating a table
    ##########################################################################
    tbl_1 = section.add_table()
    tbl_1.caption = "Dataset Listing"

    tbl_1.set_header(["Value", "Less Than 0.3", "Has digit '3'"])
    tbl_1.set_data(zip(dataset, [x < 0.3 for x in dataset], [str(x).find('3') > -1 for x in dataset]))

    paragraph_2.append_cross_reference(tbl_1)
    paragraph_2.append(f" shows the numbers in the dataset with some other properties of these numbers. ")

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
    if n_mean > mean:
        paragraph_3.append("This dataset has a larger mean compared to the baseline dataset. ")
    else:
        paragraph_3.append("This dataset has a smaller mean compared to the baseline dataset. ")
    paragraph_3.append(f"The mean is {n_mean}. ")

    return report


if __name__ == "__main__":
    # np.random.seed(19680801)
    dataset = np.random.randn(50)
    report = generate_report(dataset)

    html_generator = report_util.HTMLReportContext("")
    html_generator.generate(report, "example")
