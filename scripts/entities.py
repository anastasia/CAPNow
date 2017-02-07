class Parties:
    def format_for_xml(self, raw_str):
        raw_str = re.sub(r"([A-Z][A-Z\s+.]+)", lambda entity: tag.party(entity.group().title()), raw_str)
        return tag.parties(raw_str)

    def format_for_html(self, raw_str):
        raw_str = re.sub(r"([A-Z][A-Z\s+.]+)", lambda entity: tag.em(entity.group().title()), raw_str)
        return tag.h1(raw_str)

    def __init__(self, raw_str):
        self.xml = self.format_for_xml(raw_str)
        self.html = self.format_for_html(raw_str)

class Casename:
    def get_footnote_num(self, footnote_str):
        return re.search(r"\d+", footnote_str).group()

    def format_for_db(self, raw_str):
        name = re.sub(r"<footnotemark>\d+<\/footnotemark>", "", raw_str)
        return re.sub(r"[A-Z][A-Z]+", lambda entity: entity.group().title(), name)

    def format_for_xml(self, raw_str):
        name = re.sub(r"<footnotemark>\d+<\/footnotemark>", "", raw_str)
        title = re.sub(r"[A-Z][A-Z]+", lambda entity: entity.group().title(), name)
        return tag.name(title)

    def format_for_html(self, raw_str):
        name = re.sub(r"<footnotemark>\d+<\/footnotemark>", lambda footnote: tag.sup(self.get_footnote_num(footnote.group())), raw_str)
        title = re.sub(r"[A-Z][A-Z\s+.]+", lambda entity: tag.em(entity.group().title()), name)
        return tag.h1(title)

    def __init__(self, raw_str):
        self.xml = self.format_for_xml(raw_str)
        self.db_str = self.format_for_db(raw_str)
        self.html = self.format_for_html(raw_str)

class Footnote:
    number = None
    content = ""

    def format_for_xml(self):
        return "<footnotemark>%s</footnotemark>" % self.number

    def __init__(self, xml):
        footnote_id = re.search(r'footnoteReference\s+w\:id\=\"(\d+)\"', xml)
        self.number=int(footnote_id.groups()[0])

class Date:
    def get_enddate_str(self, raw_str):
        return raw_str.split(' - ')[1]

    def get_startdate_str(self, raw_str):
        return re.sub(r'^\w+\.\s+', '', raw_str.split(' - ')[0])

    def format_for_xml(self, raw_str):
        """
        Examples:
        <decisiondate>1997-05-19</decisiondate>
        in <casebody>:
        <decisiondate id="AML" pgmap="66">May 19, 1997.</decisiondate>
        <otherdate id="A6q" pgmap="66">January 9, 1997. -</otherdate>
        """

        enddate = self.get_enddate_str(raw_str)
        decisiondate_casebody = tag.decisiondate(enddate)

        datetime_obj = datetime.strptime(enddate, "%B %d, %Y.")
        decisiondate = tag.decisiondate(datetime.strftime(datetime_obj, "%Y-%d-%m"))

        otherdate = tag.otherdate(self.get_startdate_str(raw_str))
        return decisiondate, decisiondate_casebody, otherdate

    def format_for_html(self, raw_str):
        enddate = self.get_enddate_str(raw_str)
        startdate = self.get_startdate_str(raw_str)
        dates = startdate + " - " + enddate
        return tag.h3(dates)

    def format_for_db(self, raw_str):
        return datetime.strptime(self.get_enddate_str(raw_str), "%B %d, %Y.")

    def __init__(self, raw_str):
        self.xml = self.format_for_xml(raw_str)
        self.db_str = self.format_for_db(raw_str)
        self.html = self.format_for_html(raw_str)

class Categories:
    def format_for_html(self, raw_str):
        return tag.p(raw_str)

    def format_for_xml(self, raw_str):
        return tag.categories(raw_str)

    def __init__(self, raw_str):
        self.xml = self.format_for_xml(raw_str)
        self.html = self.format_for_html(raw_str)

class Judges:
    def format_for_db(self, raw_str):
        judges = re.sub(r'Present:|C.J.,|JJ.|&|\s{1}', '', raw_str).split(',')
        return judges

    def format_for_html(self, raw_str):
        return tag.h4(raw_str)

    def format_for_xml(self, raw_str):
        return tag.judges(raw_str)

    def __init__(self, raw_str):
        self.xml = self.format_for_xml(raw_str)
        self.db_list = self.format_for_db(raw_str)
        self.html = self.format_for_html(raw_str)