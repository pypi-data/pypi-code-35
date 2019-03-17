import json
import re
import itertools


class LangTranslateClient:
    translations: dict = {}
    publicKey: str
    isProduction: bool

    def __init__(self, publicKey, jsonFile):
        self.publicKey = publicKey
        self.translations = json.loads(open(jsonFile).read())
        print(self.translations)
        self.isProduction = self.isProductionKey(publicKey)

    def tr(self, phrase, forceLanguage):
        if not self.translations or not forceLanguage:
            return phrase

        originalLanguage = self.translations['originalLanguage']

        testOrProd = self.getTestOrProductionCache()

        (strippedPhrase, parameters) = self.replaceParametersWithGenerics(phrase)
        try:
            return self.replaceGenericsWithParameters(self.translations[testOrProd][originalLanguage][forceLanguage][strippedPhrase], parameters)
        except:
            return self.replaceGenericsWithParameters(strippedPhrase, parameters)

    def param(self, phrase):
        return f'[[[__{phrase}__]]]'

    def getTestOrProductionCache(self):
        if self.isProduction:
            return "prod"
        return "test"

    def isProductionKey(self, apiKey):
        return apiKey[0:8] == "pk_test_"

    def replaceParametersWithGenerics(self, phrase):
        strippedPhrase = phrase
        parameters = []

        index = itertools.count(0)
        paramRegex = r'\[\[\[__((\S|\s)*?)__\]\]\]'

        def captureAndReplace(match):
            parameters.append(match[0][5:-5])
            output = '[[[__{}__]]]'.format(next(index))
            return output
        strippedPhrase = re.sub(paramRegex, captureAndReplace, strippedPhrase)

        return (strippedPhrase, parameters)

    def replaceGenericsWithParameters(self, strippedPhrase, parameters):
        index = 0
        finalPhrase = strippedPhrase
        while (index < len(parameters)):
            paramRegex = r'\[\[\[__' + \
                re.escape('{}'.format(index)) + r'__\]\]\]'
            finalPhrase = re.sub(
                paramRegex, parameters[index], finalPhrase)
            index += 1

        return finalPhrase
