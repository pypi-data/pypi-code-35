import pandas as pd


class Output:
    """
    This class is called by the Manager component and is used to manage print operations on an output csv file
    """

    def __init__(self, pathoutput, comparisons):
        """
        The __init__ method is used to create the output file in the received path as input and to write only the header

        Parameters
        ----------
        pathoutput
            This is the path of output csv file
        comparisons
            This is the list of used comparisons
        """
        self.pathoutput = pathoutput
        self.comparisons = []
        for c in comparisons:
            self.comparisons.append(c['id'])
        self.file = open(self.pathoutput, 'w')
        self.col = ['Human id', 'Plant id']
        for x in self.comparisons:
            self.col.append(x)
        self.file.write(','.join(self.col) + '\n')  # write header on file
        self.data = pd.DataFrame({}, columns=self.col, index=[0])  # initialization
        self.match = []

    def stack(self, line):
        """
        The stack method is used to stack the line passed in input into an array

        Parameters
        ----------
        line
            The line to be stacked in the array
        """
        self.match.append(dict(line))

    def close(self):
        """
        The close method is used to close the file and to complete the operations to be done on the file
        """
        matchprint = []
        couple = []

        # For every match found
        for m in self.match:
            newcouple = {"Human id": m['Human id'], "Plant id": m['Plant id']}
            # If the couple examined is not present in the list of couples already examined
            if newcouple not in couple:
                couple.append(dict(newcouple))  # Add to list
                newmatch = {"Human id": m['Human id'], "Plant id": m['Plant id']}
                # This is the position of the comparison within the comparison list
                num = [i for i, x in enumerate(self.comparisons) if x == m['Comparison id']]
                # For each position before the position of the match where the match is, add 0
                for i in range(0, num[0]):
                    newmatch[self.comparisons[i]] = str(0)

                # In the position of the match, add 1
                newmatch[m['Comparison id']] = str(1)

                # In the following positions, add 0
                for i in range(num[0]+1, len(self.comparisons)):
                    newmatch[self.comparisons[i]] = str(0)
                matchprint.append(newmatch)
            else:
                # This is the position of the couple already examined in the list of all couple
                num = [i for i, x in enumerate(matchprint)
                       if x["Human id"] == newcouple["Human id"]
                       if x["Plant id"] == newcouple["Plant id"]]
                # Change with 1 the comparison that has the match of this couple
                matchprint[num[0]][m['Comparison id']] = str(1)

        for m in matchprint:
            self.data = pd.DataFrame(m, columns=self.col, index=[0])
            self.data.to_csv(self.file, encoding='utf-8', index=False, header=False, line_terminator='\n')

        self.file.close()
