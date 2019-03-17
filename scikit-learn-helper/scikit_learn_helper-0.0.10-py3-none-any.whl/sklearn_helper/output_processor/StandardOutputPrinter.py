class StandardOutputPrinter:
    def print_results(self, results, main_metric, maximize_metric):
        for result in sorted(results, key=lambda x: x["metrics"][main_metric], reverse=maximize_metric):
            self.__print_single_result(results, result, main_metric)

    def __print_single_result(self, results, result, main_metric):
        base_str_format = self.__get_base_string_format(results, main_metric)
        final_str = base_str_format.format(result["model_name"], result["cleaner_name"], result["metrics"][main_metric],
                                           result["time"])

        final_str += self.__additional_metrics_to_str(result, main_metric)

        final_str += "Time:{:.2f} sec".format(result["time"])
        print(final_str)

    def __get_base_string_format(self, results, main_metric):
        str_format = "Model: {:<" + self.__get_longest_attribute_name(results, "model_name") + "} | "
        str_format += "cleaner:{:<" + self.__get_longest_attribute_name(results, "cleaner_name") + "} | "
        str_format += main_metric.__name__ + ":{:.4f} |"
        return str_format

    @staticmethod
    def __get_longest_attribute_name(results, attribute):
        return str(max(map(len, map(lambda r: r[attribute], results))))

    @staticmethod
    def __additional_metrics_to_str(result, main_metric):
        additional_metrics_str = ""
        for metric, value in result["metrics"].items():
            if metric != main_metric:
                additional_metrics_str += "{}:{:.4f} |".format(metric.__name__, value)
        return additional_metrics_str
