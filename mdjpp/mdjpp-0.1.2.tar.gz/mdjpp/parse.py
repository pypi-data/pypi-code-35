from mdjpp.tags import istag, maketag
from mdjpp.tags import Tag,Date,Verbatim,NoTag,Multi,Global
from mdjpp.render import sstr,Null,HTML,MD
from mdjpp.options import default_options


################################################################################
# Parser
################################################################################

class JournalParser(object):
    
    def __init__(self):
        
        self.open_tags = [NoTag()]
        self.metastable_tag = None
        
        if default_options.mdjpp_null:
            self.engine = Null()
        elif default_options.mdjpp_md:
            self.engine = MD()
        elif default_options.mdjpp_html:
            self.engine = HTML()
            
    
    def __del__(self):
        self.finalize()
    
    @property
    def otag(self):
        return self.open_tags[-1]
        
    def printable(self):
        return True
    
    def printme(self,line):
        self.otag.printme(line)
        
    def open_tag(self,tag):
        # is it global tag?
        if len(self.open_tags) == 1 and isinstance(tag,Multi):
            tag = Global(tag)
        self.open_tags.append(tag)
        # print tag opening if current state is printable
        if self.printable():
            self.printme(self.engine.tag_opener(tag))
            self.printme(self.engine.tag(tag))
        
    def close_tag(self,tag):
        # check is tag closes last tag(s)
        if self.open_tags:
            if isinstance(tag,type(self.otag)):
                closed_printable = False
                if self.printable():
                    self.printme(self.engine.tag_closer(self.otag))
                    closed_printable = True
                closed_tag = self.open_tags.pop(-1)
                if self.printable() and closed_printable:
                    self.printme(closed_tag)
            elif isinstance(tag,Date) and Date in list(map(type,self.open_tags)):
                while True:
                    closed_printable = False
                    if self.printable():
                        self.printme(self.engine.tag_closer(self.otag))
                        closed_printable = True
                    closed_tag = self.open_tags.pop(-1)
                    if self.printable() and closed_printable:
                        self.printme(closed_tag)
                    #if isinstance(closed[-1],Date):
                    if isinstance(closed_tag,Date):
                        break
        
    def proceed(self,source):
        """
        Proceed with source.
        """
        for line in source:
            line = line.rstrip()
            # not a tag!
            if not istag(line):
                if self.metastable_tag:
                    # open metastable tag
                    self.open_tag(self.metastable_tag)
                    self.metastable_tag = None
                # print line
                if self.printable():
                    self.printme(line)
            # tag!
            else:
                this_tag = maketag(line)
                # no metastable tag
                if not self.metastable_tag:
                    # make new metastable tag
                    self.metastable_tag = this_tag
                    # does new tag close last tag?
                    self.close_tag(this_tag)
                # metastable tag present
                else:
                    # is metastable tag or this tag of Date type?
                    if isinstance(self.metastable_tag,Date) or isinstance(this_tag,Date):
                        # open metastable tag
                        self.open_tag(self.metastable_tag)
                        # recreate metastable tag with new tag
                        self.metastable_tag = this_tag
                        # does new tag close last tag?
                        self.close_tag(this_tag)
                    else:
                        # add new tag to metastable tag
                        self.metastable_tag.append(this_tag)
    
    def finalize(self):
        for tag in self.open_tags[:0:-1]:
            self.close_tag(tag)
        if self.open_tags:
            self.final_printout(self.open_tags.pop())
    
    def final_printout(self,tag):
        for line in tag.body:
            if isinstance(line,Tag):
                self.final_printout(line)
            else:
                if isinstance(line,sstr) and len(line) == 0:
                    continue
                print(line)


################################################################################
# Filtered parser
################################################################################

class JournalParserFilter(JournalParser):

    def printable(self):
        return self.is_tag_printable()
    
    def printme(self,line):
        if self.is_line_printable(line):
            self.otag.printme(line)
    
    def final_printout(self,tag):
        if self.skip_this_tag(tag):
            return
        return super().final_printout(tag)
    
    def skip_this_tag(self,tag):
        if default_options.mdjpp_date_skip_notags and isinstance(tag,Date):
            for line in tag.body:
                if isinstance(line,Tag):
                    return False
            return True
        if default_options.mdjpp_date_skip_empty and isinstance(tag,Date):
            if len([t for t in tag.body if not isinstance(t,sstr) and str(t).strip()]) == 0:
                return True
        return False
    
    def is_tag_printable(self):
        if default_options.mdjpp_date_from or default_options.mdjpp_date_to:
            date_tag = [tag for tag in self.open_tags if isinstance(tag,Date)]
            if date_tag:
                date_tag = date_tag[0]
                if not default_options.mdjpp_date_from:
                    if not date_tag.value <= default_options.mdjpp_date_to:
                        return False
                elif not default_options.mdjpp_date_to:
                    if not date_tag.value >= default_options.mdjpp_date_from:
                        return False
                elif not date_tag.value <= default_options.mdjpp_date_to and date_tag.value >= default_options.mdjpp_date_from:
                    return False
        if default_options.mdjpp_skip_tag:
            for tag in (tag for tag in self.open_tags if isinstance(tag,Multi)):
                for tag_tag in tag.value:
                    if tag_tag.value in default_options.mdjpp_skip_tag:
                        return False
        if default_options.mdjpp_only_tag:
            if len(self.open_tags) >= 2 and isinstance(self.open_tags[-2],Date) and isinstance(self.otag,Multi):
                for tag in self.otag.value:
                    if tag.value in default_options.mdjpp_only_tag:
                        break
                else:
                    return False
        if default_options.mdjpp_only_global_tag:
            if len(self.open_tags) >= 2 and isinstance(self.open_tags[1],Multi):
                for tag in self.open_tags[1].value:
                    if tag.value in default_options.mdjpp_only_global_tag:
                        break
                else:
                    return False
                
        return True

    def is_line_printable(self,line):
        if not isinstance(line,Tag) and not isinstance(line, sstr):
            # skip_notag_content
            if default_options.mdjpp_skip_notag_content and isinstance(self.otag,NoTag):
                return False
            # skip_global_tag_content
            if default_options.mdjpp_skip_global_tag_content and len(self.open_tags) == 2 and isinstance(self.otag,Multi):
                return False
        return True
