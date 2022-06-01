import typing
import matplotlib.pyplot as plt
import os
import numpy as np
import enum
import html

class ReportPartType(enum.Enum):
    Paragraph = 0
    Section = 1
    Figure = 2
    Table = 3
    All = 4

class TextPartType(enum.Enum):
    CrossReference = 0
    #TODO implement inline equations

class TextOutputStream: # Python 3.8 you can specify (typing.Protocol) as the parent class
    def write(self,text:str) -> typing.Any:
        ...

class ReportPart:

    def __init__(self):
        self.part_number : int = 0
        self.part_type_number : int = 0

    def get_type(self) -> ReportPartType:
        raise NotImplementedError("subclasses must override get_type()")


class TextPart:
    def get_type(self) -> TextPartType:
        raise NotImplementedError("subclasses must override get_type()")

class CrossReference(TextPart):
    def __init__(self, report_part:ReportPart):
        self.report_part = report_part

    def __str__(self) -> str:
        return "{} {}".format(type(self.report_part).__name__,self.report_part.part_type_number)

    def get_type(self) -> TextPartType:
        return TextPartType.CrossReference


class Paragraph(ReportPart):
    
    def __init__(self, text_parts : typing.Optional[typing.List] = None):
        super().__init__()
        if text_parts is not None:
            self.text_parts = text_parts
        else:
            self.text_parts = []

    def append(self, text: str):
        self.text_parts.append(text)
        pass

    def append_cross_reference(self, report_part : ReportPart):
        self.text_parts.append(CrossReference(report_part))

    def get_type(self) -> ReportPartType:
        return ReportPartType.Paragraph


class Figure(ReportPart):
    def __init__(self):
        super().__init__()
        self.matplotlib_figure = plt.figure()
        self.caption = ""
    
    def save_to_file(self, file_path:str):
        self.matplotlib_figure.savefig(file_path)

    def get_type(self) -> ReportPartType:
        return ReportPartType.Figure

    def set_bar_graph_data(self, component_labels,component_values,title):
        ax = self.matplotlib_figure.add_subplot(1,1,1)
        y_pos = np.arange(len(component_labels))

        ax.bar(y_pos, component_values, align='center', alpha=0.5)
        ax.set_xticks(y_pos)
        ax.set_xticklabels(component_labels)
        #ax.ylabel('Usage')
        #ax.set_title(title)
        self.caption = title
        self.matplotlib_figure.tight_layout()

    def set_line_plot(self,x,y,title,x_axis_title,y_axis_title):
        ax = self.matplotlib_figure.add_subplot(1,1,1)
        ax.plot(x,y)
        #ax.set_title(title)
        self.caption = title
        self.matplotlib_figure.tight_layout()
        #ax.set_xaxis(x_axis_title)
        #ax.set_yaxis(y_axis_title)


class Table(ReportPart):

    def __init__(self):
        super().__init__()
        self.header = []
        self.data = []
        self.caption = ""

    def set_header(self,header_names):
        for header_name in header_names:
            self.header.append(header_name)

    def set_data(self, data):
        self.data = data


    def get_type(self) -> ReportPartType:
        return ReportPartType.Table


class Section(ReportPart):

    def __init__(self, title : str, children : typing.Optional[typing.List[ReportPart]] = None):
        self.title = title
        if children is not None:
            self.children = children
        else:
            self.children = []

    def add_section(self, section_title: str) -> 'Section':
        new_section = Section(section_title)
        self.children.append(new_section)
        return new_section

    def add_paragraph(self) -> Paragraph:
        new_para = Paragraph()
        self.children.append(new_para)
        return new_para
    
    def add_table(self) -> Table:
        new_table = Table()
        self.children.append(new_table)
        return new_table

    def add_figure(self) -> Figure:
        new_figure = Figure()
        self.children.append(new_figure)
        return new_figure
    
    def get_type(self) -> ReportPartType:
        return ReportPartType.Section
    

class Report:
    def __init__(self, title : str, sections : typing.Optional[typing.List[Section]] = None):
        self.title = title
        if sections is not None:
            self.sections = sections
        else:
            self.sections = []

        self.footer = ""

    def add_section(self, section_title: str):
        new_section = Section(section_title)
        self.sections.append(new_section)
        return new_section


class ReportContext:
    def _assign_part_numbers(self,report_part:ReportPart,number_counts:typing.Dict[ReportPartType,int]):
        t = report_part.get_type()
        number_counts[t] += 1
        number_counts[ReportPartType.All] += 1
        report_part.part_number = number_counts[ReportPartType.All]
        report_part.part_type_number = number_counts[t]
        if t == ReportPartType.Section:
            section_part : Section = typing.cast(Section,report_part)
            for child in section_part.children:
                self._assign_part_numbers(child,number_counts)

    def assign_part_numbers(self, report:Report):
        number_counts = {ReportPartType.Paragraph:0,ReportPartType.Figure:0,ReportPartType.Table:0,ReportPartType.Section:0,ReportPartType.All:0}
        for section in report.sections:
            self._assign_part_numbers(section,number_counts)


class SubParts(enum.Enum):
    SectionTitle = 0


class HTMLReportContext(ReportContext):
    def __init__(self, folder_path:str):
        self.folder_path = folder_path
        self.figure_count = 0 # this tracks how many figures have been written to folder
        self._init_part_write_strategies()
        self._init_text_write_strategies()
        self._init_subpart_write_strategies()


    def _init_part_write_strategies(self):
        self.part_write_strategies = {}
        self.part_write_strategies[ReportPartType.Paragraph] = self._decorate_anchor_name(self._write_paragraph)
        self.part_write_strategies[ReportPartType.Table] = self._decorate_anchor_name(self._write_table)
        self.part_write_strategies[ReportPartType.Figure] = self._decorate_anchor_name(self._write_figure)
        self.part_write_strategies[ReportPartType.Section] = self._decorate_anchor_name(self._write_section)

    def _init_text_write_strategies(self):
        self.text_write_strategies = {}
        self.text_write_strategies[TextPartType.CrossReference] = self._write_cross_reference

    def _init_subpart_write_strategies(self):
        self.subpart_write_strategies = {}
        self.subpart_write_strategies[SubParts.SectionTitle] = self._write_sub_part_section_title

    @staticmethod
    def _write_cross_reference(context:"HTMLReportContext",html_file: TextOutputStream, text_part:TextPart, level:int = 2):
        cross_reference = typing.cast(CrossReference,text_part)
        html_file.write("<a href='#{}' class='cross_reference'>{}</a>".format(cross_reference.report_part.part_number,cross_reference))


    @staticmethod
    def _write_sub_part_section_title(context:"HTMLReportContext",html_file: TextOutputStream, section:Section, level:int = 2):
        html_file.write("<h{}>{} <a href='#top' class='jump'>&#8679;</a></h{}>".format(level,html.escape(section.title),level))


    @staticmethod
    def _decorate_anchor_name(write_strategy):
        def anchor_strategy(context:"HTMLReportContext",html_file: TextOutputStream, report_part:ReportPart, level:int = 2):
            html_file.write("<a name='{}' class='part_anchor'>{}</a>".format(report_part.part_number,report_part.part_number))
            write_strategy(context,html_file,report_part,level)

        return anchor_strategy

    @staticmethod
    def _write_paragraph(context:"HTMLReportContext",html_file: TextOutputStream, report_part:ReportPart, level:int = 2):
        html_file.write("<p>")
        paragraph : Paragraph = typing.cast(Paragraph,report_part)
        for text_part in paragraph.text_parts:
            if isinstance(text_part,TextPart):
                context.text_write_strategies[text_part.get_type()](context,html_file,text_part,level)
            else:
                html_file.write(html.escape(str(text_part)))
        html_file.write("</p>")

    @staticmethod
    def _write_table(context:"HTMLReportContext",html_file: TextOutputStream, report_part:ReportPart, level:int = 2):
        table: Table = typing.cast(Table,report_part)
        html_file.write("<table>")
        html_file.write("<caption>Table {}. {}</caption>".format(table.part_type_number, html.escape(table.caption)))
        html_file.write("<thead>")
        html_file.write("<tr>")
        for header_name in table.header:
            html_file.write("<th>{}</th>".format(html.escape(header_name)))
        html_file.write("</tr>")
        html_file.write("</thead>")

        html_file.write("<tbody>")
        for element in table.data:
            html_file.write("<tr>")
            for data_element in element:
                html_file.write("<td>{}</td>".format(html.escape(str(data_element))))
            html_file.write("</tr>")

        html_file.write("</tbody>")

        html_file.write("</table>")

    @staticmethod
    def _write_figure(context:"HTMLReportContext",html_file: TextOutputStream, report_part:ReportPart, level:int = 2):
        figure : Figure = typing.cast(Figure,report_part)
        relative_image_path = "{}.png".format(context.figure_count)
        figure.save_to_file(os.path.join(context.folder_path,relative_image_path))
        html_file.write("<figure>")
        html_file.write("<img src='{}'/>".format(relative_image_path))
        html_file.write("<figcaption>Figure {}. {}</figcaption>".format(figure.part_type_number,html.escape(figure.caption)))
        html_file.write("</figure>")
        context.figure_count += 1

    @staticmethod
    def _write_section(context:"HTMLReportContext",html_file: TextOutputStream, report_part:ReportPart, level:int = 2):
        section = typing.cast(Section,report_part)

        html_file.write("<div class='section'>")

        context.subpart_write_strategies[SubParts.SectionTitle](context,html_file,section,level)
        
        for child_report_part in section.children:
            context.part_write_strategies[child_report_part.get_type()](context,html_file,child_report_part, level+1)
            
        html_file.write("</div>")

    def generate_to_stream(self, report:Report, html_file:TextOutputStream):
        # Make sure every report part has an up-to-date part number
        self.assign_part_numbers(report)

        html_file.write("<html>")
        html_file.write("<head>")
        html_file.write('<meta charset="utf-8"/>')
        html_file.write('<link rel="stylesheet" type="text/css" href="html_support_files/style.css"/>')
        
        # The following HTML makes the tables in the report interactive
        html_file.write('<link rel="stylesheet" type="text/css" href="html_support_files/datatables.min.css"/>')
        html_file.write('<script type="text/javascript" src="html_support_files/datatables.min.js"></script>')
        html_file.write('<script type="text/javascript">')
        html_file.write('$(document).ready(function() {$("table").DataTable();} )')
        html_file.write('</script>')

        html_file.write("<title>{}</title>".format(html.escape(report.title)))
        html_file.write("</head>")
        html_file.write("<body>")
        html_file.write("<a name='top' class='part_anchor'></a>")
        html_file.write("<div class='report'>")
        html_file.write("<div class='header'>")
        html_file.write("<img src='logo.png' class='logo'/><h1>{}</h1>".format(html.escape(report.title)))
        html_file.write("</div>")
        html_file.write("<div class='content'>")
        for section in report.sections:
            self.part_write_strategies[section.get_type()](self,html_file,section)
        html_file.write("</div>")
        html_file.write("<div class='footer'>")
        html_file.write("{}".format(html.escape(report.footer)))
        html_file.write("</div>")
        html_file.write("</div>")
        html_file.write("</body>")
        html_file.write("</html>")

    def generate(self, report:Report, file_name:str):
        with open(os.path.join(self.folder_path,"{}.html".format(file_name)),'w', encoding='utf-8') as html_file:
            self.generate_to_stream(report, html_file)
        
    

