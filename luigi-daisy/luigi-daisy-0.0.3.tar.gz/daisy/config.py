import luigi

class daisy(luigi.Config):

    # default output folder
    data_dir = luigi.Parameter("./data")

    # updating 
    progress_update_span = luigi.FloatParameter(0.5)

