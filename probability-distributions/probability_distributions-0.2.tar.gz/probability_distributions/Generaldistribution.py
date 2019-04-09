class Distribution:
    
    def __init__(self, mu = 0, sigma = 1):
        """
            Generic Distribution class for calculationg and visualizing
            a probability distribution.
            
            Attributes:
                mean (float) representing the mean value of the distribution
                stdev (float) representing the standard deviation of the distribution
                data_list (a list of float) a list of float extracted from data file
        """
        
        self.mean = mu
        self.stdev = sigma
        self.data = []
        
    def read_data_file(self, filename):
        """
            Function to read in data from txt file. The text file should have one number (float) per line. The numbers are stored in the data attribute.
            
            Args:
                filename (string): name of file to read from 
            Returns:
                None
        """
        
        with open(filename) as f:
            data_list = []
            line = file.readline()
            while line:
                data_list.append(int(line))
                line = file.readline()
        f.close()
        
        self.data = data_list
        