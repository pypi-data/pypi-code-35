# This file is part of Sympathy for Data.
# Copyright (c) 2013 System Engineering Software Society
#
# Sympathy for Data is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sympathy for Data is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sympathy for Data.  If not, see <http://www.gnu.org/licenses/>.
import os
import sys
import copy
import unittest
import traceback

import six
from nose.plugins.attrib import attr
from Qt import QtWidgets

from sympathy.utils.prim import limit_traceback


LIB_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir, 'Python'))
sys.path.append(LIB_DIR)

import Gui.interactive


def diff_print(a, b, depth=0):
    pad = '-'*depth*2
    if isinstance(a, dict):
        for key in set(a.keys()) | set(b.keys()):
            if key not in a:
                print('{}Key {} missing in a'.format(pad, key))
            elif key not in b:
                print('{}Key {} missing in b'.format(pad, key))
            elif a[key] != b[key]:
                print('{}{}'.format(pad, key))
                diff_print(a[key], b[key], depth=depth+1)
    elif a != b:
        print('{}Different values: {} vs. {}'.format(pad, a, b))


class TestInteractive(unittest.TestCase):
    """
    Library tests using interactive.

    Add your library tests and node unit tests bellow or in a separate file
    with a similar base.
    """

    def setUp(self):
        self.library = Gui.interactive.load_library()

    @attr('gui')
    def test_library_widgets(self):
        """
        Test that all configuration widgets can be created without errors.
        """
        failed = []
        tracebacks = {}
        nodeids = self.library.nodeids()
        qapp = QtWidgets.QApplication.instance()

        for nodeid in nodeids:
            try:
                testnode = self.library.node(nodeid)
                widget = testnode._SyiNode__configure_widget()
                qapp.processEvents()
                if hasattr(widget, 'cleanup'):
                    widget.cleanup()
                widget.deleteLater()
                qapp.processEvents()
            except Gui.interactive.InteractiveNotNodeError:
                pass
            except:
                tb = traceback.format_exception(*sys.exc_info())
                filename = os.path.basename(testnode.filename)
                tb = limit_traceback(tb, filename=filename)

                tracebacks[nodeid] = tb
                failed.append(nodeid)

                print('{}\n{}:\n\n{}'.format('-' * 30, nodeid, tb))

        print('=' * 30)
        print('({}/{}) configuration GUIs failed.'.format(
            len(failed), len(nodeids)))

        assert(not len(tracebacks))

    @unittest.skip('No longer needed?')
    @attr('gui')
    def test_library_widgets_modify_parameters(self):
        """
        Test that config widgets don't modify their parameters during init.
        """
        failed = []
        tracebacks = {}
        nodeids = self.library.nodeids()
        qapp = QtWidgets.QApplication.instance()

        for nodeid in nodeids:
            try:
                testnode = self.library.node(nodeid)
                tags = testnode._SyiNode__node.tags
                if any(six.text_type(t) == 'Hidden.Deprecated' for t in tags):
                    continue
                node_context = testnode._SyiNode__build_node_context()
                adjusted = testnode._SyiNode__adjust_parameters(node_context)
                if adjusted is not None:
                    node_context = adjusted
                try:
                    old_parameters = copy.deepcopy(
                        node_context.parameters.parameter_dict)
                except AttributeError:
                    old_parameters = copy.deepcopy(
                        node_context.parameters)
                widget = testnode._SyiNode__configure_widget(
                    node_context=node_context)
                qapp.processEvents()
                # Force widget to save parameters in node_context:
                if hasattr(widget, 'save_parameters'):
                    widget.save_parameters()
                qapp.processEvents()
                if hasattr(widget, 'cleanup'):
                    widget.cleanup()
                qapp.processEvents()
                try:
                    new_parameters = node_context.parameters.parameter_dict
                except AttributeError:
                    new_parameters = node_context.parameters
                # self.assertEqual(old_parameters, new_parameters)
                if new_parameters != old_parameters:
                    failed.append(nodeid)
                    print('{}\n{}:\n\n'.format('-' * 30, nodeid))
                    diff_print(new_parameters, old_parameters)
                widget.deleteLater()
                qapp.processEvents()
            except:
                tb = traceback.format_exception(*sys.exc_info())
                tb = ''.join(tb)

                tracebacks[nodeid] = tb
                print('{}\n{}:\n\n{}'.format('-' * 30, nodeid, tb))

        print('=' * 30)
        print('({}/{}) configuration GUIs modified their parameters.'.format(
            len(failed), len(nodeids)))
        print('({}/{}) configuration GUIs failed to open.'.format(
            len(tracebacks), len(nodeids)))
        print('The following configuration GUIs modified their '
              'parameters:\n{}'.format('\n'.join(failed)))

        # This number should be decreased as nodes are fixed to ensure that we
        # eventually reach and keep it at zero.
        assert(len(failed) + len(tracebacks) <= 34)

    def test_nodes_in_workflows(self):

        def get_nodeids(flow_dict):
            res = []
            for node in flow_dict.get('nodes', []):
                node_id = node.get('id')
                if node_id:
                    res.append(node_id)
            for flow in flow_dict.get('flows', []):
                flow_id = flow.get('id')
                if flow_id:
                    res.append(flow_id)

                res.extend(get_nodeids(flow))
            return res

        nodeids = set(self.library.nodeids())
        paths = self.library.paths()
        import fnmatch
        from sympathy.platform import workflow_converter

        tested_nodeids = set()

        for suffix in [['Examples'], ['Test', 'Workflow']]:
            for path in paths:
                root = os.path.join(path, *suffix)
                for base, dirs, files in os.walk(root):
                    for filename in fnmatch.filter(files, '*.syx'):
                        with open(os.path.join(base, filename), 'r') as source:
                            converter = workflow_converter.XMLToJson(source)
                            flow_dict = converter.dict()

                            if 'NO_TEST' not in flow_dict.get(
                                    'environment', {}):
                                tested_nodeids.update(get_nodeids(flow_dict))

        exceptions = set([
            'org.sysess.builtin.propagate',
            'org.sysess.list.append.flow',
            'org.sysess.sympathy.data.adaf.detrendadafnodes',
            'org.sysess.sympathy.data.json.importjsons',
            'org.sysess.sympathy.data.json.removekeyjsons',
            'org.sysess.sympathy.data.json.selectkeyjsons',
            'org.sysess.sympathy.data.json.splitonkeyjsons',
            'org.sysess.sympathy.data.table.dropnantables',
            'org.sysess.sympathy.data.table.indextable',
            'org.sysess.sympathy.data.table.matlabtable',
            'org.sysess.sympathy.data.table.matlabtables',
            'org.sysess.sympathy.data.table.selecttablerowss',
            'org.sysess.sympathy.datasources.rename',
            'org.sysess.sympathy.datasources.renames',
            'org.sysess.sympathy.examples.allparameters',
            'org.sysess.sympathy.examples.controller',
            'org.sysess.sympathy.examples.daskmax',
            'org.sysess.sympathy.examples.daskstack',
            'org.sysess.sympathy.examples.dasktail',
            'org.sysess.sympathy.examples.daskvisualize',
            'org.sysess.sympathy.examples.errorexample',
            'org.sysess.sympathy.examples.extras.antigravitynode',
            'org.sysess.sympathy.examples.helloworld',
            'org.sysess.sympathy.examples.helloworldcustomizable',
            'org.sysess.sympathy.examples.outputexample',
            'org.sysess.sympathy.examples.progress',
            'org.sysess.sympathy.examples.readwrite',
            'org.sysess.sympathy.files.downloadfile',
            'org.sysess.sympathy.filters.columnfiltertables',
            'org.sysess.sympathy.html.dicttogeojson',
            'org.sysess.sympathy.html.htmltotext',
            'org.sysess.sympathy.html.report',
            'org.sysess.sympathy.keyvaluecalculation',
            'org.sysess.sympathy.machinelearning.category_encoder',
            'org.sysess.sympathy.machinelearning.cond_prob_cat',
            'org.sysess.sympathy.machinelearning.count_vectorizer',
            'org.sysess.sympathy.machinelearning.crossval_score',
            'org.sysess.sympathy.machinelearning.decision_function',
            'org.sysess.sympathy.machinelearning.export',
            'org.sysess.sympathy.machinelearning.extract_parameters',
            'org.sysess.sympathy.machinelearning.fit_text',
            'org.sysess.sympathy.machinelearning.fit_transform_text',
            'org.sysess.sympathy.machinelearning.generate_blobs',
            'org.sysess.sympathy.machinelearning.generate_blobs_from_table',
            'org.sysess.sympathy.machinelearning.generate_classification',
            'org.sysess.sympathy.machinelearning.images_to_features',
            'org.sysess.sympathy.machinelearning.import',
            'org.sysess.sympathy.machinelearning.inverse_transform',
            'org.sysess.sympathy.machinelearning.k_means',
            'org.sysess.sympathy.machinelearning.kpca',
            'org.sysess.sympathy.machinelearning.label_binarizer',
            'org.sysess.sympathy.machinelearning.label_encoder',
            'org.sysess.sympathy.machinelearning.learningcurve',
            'org.sysess.sympathy.machinelearning.linearregression',
            'org.sysess.sympathy.machinelearning.mini_batch_k_means',
            'org.sysess.sympathy.machinelearning.multioutput_classifier',
            'org.sysess.sympathy.machinelearning.multioutput_regressor',
            'org.sysess.sympathy.machinelearning.one_class_svm',
            'org.sysess.sympathy.machinelearning.one_hot_encoder',
            'org.sysess.sympathy.machinelearning.parameter_distribution',
            'org.sysess.sympathy.machinelearning.pls',
            'org.sysess.sympathy.machinelearning.r2_score',
            'org.sysess.sympathy.machinelearning.random_forest_classifier',
            'org.sysess.sympathy.machinelearning.randomized_parsearch',
            'org.sysess.sympathy.machinelearning.robust_scaler',
            'org.sysess.sympathy.machinelearning.sim_anneal_parsearch',
            'org.sysess.sympathy.machinelearning.standard_scaler',
            'org.sysess.sympathy.machinelearning.svr',
            'org.sysess.sympathy.machinelearning.transform_text',
            'org.sysess.sympathy.machinelearning.votingclassifier',
            'org.sysess.sympathy.matlab.matlabcalculator',
            'org.sysess.sympathy.visualize.figures',
            'org.sysess.sympathy.visualize.figuresfromtableswithtable',
            'org.sysess.sympathy_course.getcolumnattributestables',
            'se.combine.sympathy.data.table.cartesian_product_table',
            'se.combine.sympathy.data.table.cartesian_product_tables',
            'syip.convert_image_to_table_2d',
            'syip.convert_table2d_to_image',
            'syip.corner_detection',
            'syip.edge_detection',
            'syip.imagefiltering2',
            'syip.labelling',
            'syip.loadimage',
            'syip.loadimage_list',
            'syip.overlay_list',
            'syip.saveimage'])

        untested_nodeids = nodeids.difference(tested_nodeids)
        new_untested_nodeids = untested_nodeids.difference(exceptions)

        if new_untested_nodeids:
            print('Untested nodes:\n  {}'.format('\n  '.join(
                sorted(new_untested_nodeids))))

        assert len(new_untested_nodeids) == 0, (
            'Newly added nodes should be present in test flows or be '
            'manually excluded')

    def test_random_table(self):
        """
        Test example that executes Random Table and checks the output length.
        """
        rtnode = self.library.node('Random Table')
        output = rtnode.execute()
        assert(output[0].number_of_columns() == 5)
        assert(output[0].number_of_rows() == 5)
        return output

    def test_random_adaf(self):
        """
        Test example that executes Random ADAF and checks number of
        meta entries.
        """
        rtnode = self.library.node('Random ADAF')
        output = rtnode.execute()

        assert(len(output[0].meta.keys()) == 5)
        return output

    def test_random_table_with_configure(self):
        """
        Test example that configures and executes Random Table and checks the
        output length.
        """
        rtnode = self.library.node('Random Table')
        rtnode.parameters.attributes.column_entries.value = 3
        rtnode.parameters.attributes.column_length.value = 3
        output = rtnode.execute()
        assert(output[0].number_of_columns() == 3)
        assert(output[0].number_of_rows() == 3)
        return output

    def test_two_nodes(self):
        """
        Test example that executes Random Table and uses that as input for
        Item to List checking that the data is preserved.
        """
        i2lnode = self.library.node('Item to List')
        rtoutput = self.test_random_table()
        output = i2lnode.execute(rtoutput)
        assert((rtoutput[0].to_matrix() == output[0][0].to_matrix()).all())

    def test_few_nodes(self):
        """
        Test example that executes Random Table and Random ADAF and uses the
        results as input to Update ADAF with Table, checking that
        the resulting meta in the new ADAF comes from the table.
        """
        rtoutput = self.test_random_table()
        raoutput = self.test_random_adaf()
        updawtnode = self.library.node('Update ADAF with Table')
        upadwtoutput = updawtnode.execute(rtoutput + raoutput)
        assert (upadwtoutput[0].meta['0'].value() ==
                rtoutput[0].get_column_to_array('0')).all()


if __name__ == '__main__':
    unittest.main()
