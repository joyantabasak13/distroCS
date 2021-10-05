######### Input Format ###############
# * --- paperTitle
# @ --- Authors
# t ---- Year
# c  --- publication venue
# index 00---- index id of this paper
# % ---- the id of references of this paper (there are multiple lines, with each indicating a reference)
# ! --- Abstract

class Entry:
    def __init__(self, title, year, authors, venue, index):
        self.title = title
        self.year = year
        self.venue = venue
        self.index = index
        self.author_list = [x.strip() for x in authors.split(',')]

    def print_entry(self):
        print("""Entry {}: 
            \n Titled: {} 
            \n Authors: {} 
            \n Year: {} 
            \n Published Venue: {} """.format(self.index, self.title, self.author_list, self.year, self.venue))

