#import
import yaml

class argparseGraph:

    def __init__(self, configuration_file, argpars, verbose=False):
        self.__conf_path = configuration_file
        try:
            with open(configuration_file, 'r') as stream_file:
                self.__conf = yaml.load(stream_file)
        except OSError as err:
            raise OSError(err)
        if verbose:
            for key, value in self.__conf.items():
                print("strategie: {}".format(key))

        self.__args = argpars.__dict__
        self.__loop_options_available()

    def __loop_options_available(self):
        for title, scenario in self.__conf.items():

            scenario.update(dict({"name": title, "status": None}))
            options_list = []
            if len(scenario["options"]) > 0:
                if type(scenario["options"]) is str:
                    # one line list
                    if "," in scenario["options"]:
                        scenario["options"] = scenario["options"].replace(" ", '').split(",")
                        self.__check_option_scenario(scenario)
                    # all
                    if scenario["options"] == "all":
                        for k, item in self.__args.items():
                            if item is None:
                                scenario["status"] =  "Fail"
                                break
                else:
                    # list format
                    self.__check_option_scenario(scenario)
            else:
                scenario["status"] =  "Fail"

    def __check_option_scenario(self, scenario):
        for needed_args in scenario["options"]:
            if needed_args in self.__args:
                scenario["status"] = "Fail" if self.__args[needed_args] is None else None
            else:
                print("APG error: Bad param name in {}".format(self.__conf_path))
                exit(-1)
        for k, item in self.__args.items():
            if (k not in scenario["options"] and item != None) or \
               (k in scenario["options"] and item is None):
                scenario["status"] = "Fail"

    def get_one(self):
        for scenario, obj in sorted(self.__conf.items()):
            if obj["status"] == None:
                return scenario
        return dict({"Error": "Not scenario found", "status": -1})

    def get_dict(self):
        for scenario, obj in sorted(self.__conf.items()):
            if obj["status"] == None:
                return obj
        return dict({"Error": "Not scenario found", "status": -1})

    def get_all(self):
        return self.__conf
