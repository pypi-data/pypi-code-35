from gherkan.decoder.SignalParser import SignalParser

#Translates variables in tree to NLP or back to signals based on the tranType
# (in each node of the tree a variable data.VariableNLP will be filled)
#   st - original statementTree
from gherkan.processing.TreeProcessor import TreeProcessor

if __name__ == "__main__":
    sp = SignalParser()
    st = sp.parseStatement(
     "robotR2ProgramNumber == 1 && robotR1ProgramNumber == 2 && part2Destination == 0 && BoxFull == 1")

    tp = TreeProcessor(language="en")

    # loads yaml file with templates
    tp.load_templ_dic('utils/templates_dic.yaml')
    st.root = tp.process_tree(st.root, dir=TreeProcessor.Direction.SIGNAL_TO_NL)

    # result is saved in node.data.variableNL_full
    print(st)

    # TODO linearize tree