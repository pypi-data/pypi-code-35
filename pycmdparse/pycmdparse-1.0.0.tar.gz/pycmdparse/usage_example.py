class UsageExample:
    """
    Supports providing a usage example to help the end user. In cases with complex
    functionality and lots of options/params, an example can help the user get
    started. An example consists of two parts: one part showing a command line
    exemplar, and a second part consisting of a narrative that explains the
    result. See the yaml in teh example.

    There's no functionality here - its just help for the end user.
    """
    def __init__(self, example):
        """
        Initializes the instance from the passed dictionary. The dictionary is expected
        to have been produced from yaml. The yaml spec for an example is:

        examples:
          - example: foo-utility FROM TO
            explanation: >
              Reads from file FROM and writes to file TO

        :param example: According the the spec above, this would be a single
        example's dictionary, containing two keys: "example", and "explanation"
        """
        self._example = example.get("example")
        self._explanation = example.get("explanation")

    @property
    def example(self):
        return self._example

    @property
    def explanation(self):
        return self._explanation
