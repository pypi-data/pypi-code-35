# Copyright (c) 2013, System Engineering Software Society
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the System Engineering Software Society nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.
# IN NO EVENT SHALL SYSTEM ENGINEERING SOFTWARE SOCIETY BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
Part of the sympathy package.
"""
from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import os
import copy
import functools
import sys
import collections

import six

from . import message
from . import message_util
from . import os_support
# from . import qt_compat2
from . import settings
from . exceptions import sywarn
from . import widget_library as sywidgets
from .. utils.context import with_files, original
from .. utils import port as port_util
from .. utils.prim import uri_to_path, nativepath, format_display_string
from . parameter_helper import ParameterRoot, ParameterGroup, update_list_dict
from . parameter_helper_gui import ParameterView
from . parameter_helper_visitors import WidgetBuildingVisitor
from .. utils.context import InputPortDummy
from .. utils import preview
from .. utils import network

import Qt.QtCore as QtCore
import Qt.QtWidgets as QtWidgets
import Qt.QtGui as QtGui

# QtCore = qt_compat2.QtCore
# QtGui = qt_compat2.QtGui


def void(*args):
    pass


class NodeContext(object):
    def __init__(self, input, output, definition, parameters, typealiases,
                 objects=None, own_objects=None):
        self.input = input
        self.output = output
        self.definition = definition
        self.parameters = parameters
        self.typealiases = typealiases
        self._objects = {} if objects is None else objects
        self._own_objects = set() if own_objects is None else own_objects

    def __iter__(self):
        return iter((self.input, self.output, self.definition, self.parameters,
                    self.typealiases))

    def __len__(self):
        return sum(1 for _ in self)

    def manage_input(self, filename, fileobj):
        """
        Let the lifetime of fileobj be decided outside of the node.
        Normally, it will be more long-lived than regular inputs
        and outputs, making it possible to add inputs that need to be
        live when writeback takes place.
        """
        self._objects[filename] = fileobj

    def __enter__(self):
        return self

    def __exit__(self, *args):
        for output_ in self.output:
            output_.close()

        for obj in self._objects.values():
            try:
                obj.close()
            except Exception:
                pass

        for input_ in self.input:
            input_.close()

        self._objects.clear()


def managed_context(function):
    """
    Decorator function used to provide automatic management of node_context
    input and output fields.

    When using a managed context the input and output fields will contain the
    value yielded by the generator instead of the generator itself.
    """
    def adapt(self, node_context, managers, **kwargs):
        """Adapter for running node function using 'with_files'."""
        # Splitting inputs and outputs.
        length = len(node_context.input)
        inputs = managers[:length]
        outputs = managers[length:]

        update_lists = function.__name__ not in ["execute_basic",
                                                 "verify_parameters_basic"]
        managed_node_context = self.update_node_context(
            node_context, inputs, outputs,
            sy_parameters(node_context.parameters,
                          update_lists=update_lists))

        managed_node_context._objects = node_context._objects

        return function(
            self,
            managed_node_context,
            **kwargs)

    def wrapper(self, node_context, **kwargs):
        """
        The managers list argument contain both input and output, in the
        same list. The reason for this is the interface of with_files.
        The input elements will be first and the output elements last.
        """
        def runner(managers):
            return adapt(self, node_context, managers, **kwargs)

        result = with_files(runner,
                            list(node_context.input) +
                            list(node_context.output))
        node_context.__exit__()
        return result

    wrapper.function = function
    return wrapper


def update_parameters(node, old_params):
    """
    Update parameters of old nodes using new node definition from library.
    """
    def default_list_params_update(old_params):
        type_ = old_params.get('type')
        if type_ == 'list':
            if bool(old_params['value']) != bool(old_params['value_names']):
                update_list_dict(old_params)
        for key in old_params:
            if isinstance(old_params[key], dict):
                default_list_params_update(old_params[key])

    def default_params_update(definition_params, old_params):
        type_ = old_params.get('type')
        for key in definition_params:
            if key == 'type':
                continue
            elif (key in ('order', 'label', 'description') and
                    key in definition_params and
                    old_params.get(key) != definition_params[key]):
                old_params[key] = definition_params[key]
            elif (type_ == 'list' and
                    key == 'list' and
                    definition_params[key] and
                    old_params.get(key) != definition_params[key]):
                old_params[key] = definition_params[key]
                list_ = old_params['list']
                old_params['value'] = [
                    list_.index(n) for n in old_params['value_names']
                    if n in list_]
            elif key not in old_params:
                old_params[key] = definition_params[key]
            elif (isinstance(definition_params[key], dict) and
                    isinstance(old_params[key], dict) and
                    not (type_ == 'json' and key == 'value')):
                default_params_update(definition_params[key], old_params[key])

    try:
        definition_params = node.parameters
        if isinstance(definition_params, ParameterGroup):
            definition_params = definition_params.parameter_dict

        # We need to make sure that definition parameters have correct values
        # for 'order'. The call to reorder will fix that, but does so by
        # mutating the parameter dictionary, so we make a copy of the
        # dictionary to avoid unwanted side-effects.
        definition_params = copy.deepcopy(definition_params)
        ParameterRoot(definition_params, warn=False).reorder()
    except AttributeError:
        definition_params = {}

    # Node specific parameter updating if applicable.
    try:
        old_params = node.update_parameters_basic(old_params)
    except NotImplementedError:
        pass
    # And then default parameter updating.
    default_list_params_update(old_params)
    default_params_update(definition_params, old_params)


def update_bindings(params, definition, inputs, outputs):

    def update(param, data):
        if param:
            if param['type'] in ['group', 'page']:
                for k, v in data.items():
                    param_ = param.get(k)
                    if param_ and isinstance(param_, dict):
                        update(param_, v)
            else:
                for k, v in data.items():
                    if k not in ['type', 'order', 'label', 'description']:
                        param[k] = v

    def prune(param):
        def prune_names(param):
            return set(param).difference(
                ['editor', 'order', 'description'])

        if not isinstance(param, dict):
            return param
        elif param['type'] in ['group', 'page']:
            return {k: prune(param[k]) for k in prune_names(param.keys())}
        else:
            return {k: param[k] for k in prune_names(param.keys())}

    idefs = definition['ports'].get('inputs', [])
    if (idefs and len(idefs) == len(inputs) and
            idefs[-1].get('name') == '__sy_conf__'):
        try:
            update(params, inputs[-1].get())
        except Exception:
            sywarn('Could not update parameters with configuration data.')

    odefs = definition['ports'].get('outputs', [])
    if (odefs and len(odefs) == len(outputs) and
            odefs[-1].get('name') == '__sy_conf__'):
        try:
            outputs[-1].set(prune(params))
        except Exception:
            sywarn('Could not write parameters as configuration data.')


def _build_mem_port(port_dict):
    return port_util.port_mem_maker(port_dict)


def _build_mem_ports(port_dicts):
    return [
        _build_mem_port(port_dict)
        for port_dict in port_dicts]


class BaseContextBuilder(object):
    def build(self, node, parameters, typealiases, exclude_output=False,
              exclude_input=False, read_only=False, bind=False):
        """Build node context object."""
        # Creates a dictionary of typealiases with inter-references expanded.
        node_typealiases = port_util.typealiases_parser(typealiases)

        # Take input port definitions and convert to the required
        # structure for the node context object.
        input_ports = parameters['ports'].get('inputs', [])
        if exclude_input:
            node_input = _build_mem_ports(input_ports)
        else:
            node_input = node._build_file_ports_or_dummys(
                port_util.dummy_input_port_maker, input_ports, 'r')

        # Do the same for the output port. In some cases we are not
        # allowed to access the output port and this is when we set
        # the structure to None.
        output_ports = parameters['ports'].get('outputs', [])
        if exclude_output:
            node_output = _build_mem_ports(output_ports)
        else:
            # Generate output port object structure.
            node_output = node._build_file_ports_or_dummys(
                port_util.dummy_output_port_maker, output_ports,
                'r' if read_only else 'w')

        # Users should not really need to have access to the node definition?
        node_definition = parameters

        # Copy parameter structure
        node_parameters = parameters['parameters'].get('data', {})
        update_parameters(node, node_parameters)
        if bind:
            update_bindings(
                node_parameters, node_definition, node_input, node_output)

        # Initialize instance of NodeContext.
        return node.create_node_context(
            node_input,
            node_output,
            node_definition,
            node_parameters,
            node_typealiases.values(),
            own_objects=set(node_input + node_output))


class ManualContextBuilder(object):
    """
    Build node context object with the ability to supply inputs that override
    the ones provided by the parameters.  The resulting inputs and outputs are
    available for access and closing through public fields.
    """

    def __init__(self, inputs, outputs, is_output_node, port_dummies=False,
                 objects=None, check_fns=True):
        self.inputs = inputs
        self.outputs = outputs
        self.input_fileobjs = {}
        self.output_fileobjs = {}
        self.objects = {} if objects is None else objects
        self._port_dummies = port_dummies
        self._is_output_node = is_output_node
        self._check_fns = check_fns

    def build(self, node, parameters, typealiases, exclude_output=False,
              exclude_input=False, read_only=False, bind=False):
        """Build node context object."""
        # Creates a dictionary of typealiases with inter-references expanded.
        node_typealiases = port_util.typealiases_parser(typealiases)

        # Take input port definitions and convert to the required
        # structure for the node context object.
        input_ports = parameters['ports'].get('inputs', [])
        if exclude_input:
            node_input = _build_mem_ports(input_ports)
        else:
            node_input = []
            for input_port in input_ports:
                # requires_deepcopy = input_port.get('requires_deepcopy', True)
                requires_deepcopy = True
                filename = input_port['file']
                if self._check_fns:
                    assert(filename != '')
                data = self.inputs.get(filename)

                if data is None:
                    try:
                        data = port_util.port_maker(input_port, 'r', True,
                                                    expanded=node._expanded,
                                                    managed=node._managed)
                        if requires_deepcopy:
                            data = data.__deepcopy__()
                    except (IOError, OSError) as e:
                        # E.g. the file doesn't exist yet.
                        if self._port_dummies:
                            data = InputPortDummy(e)
                        else:
                            raise
                    self.input_fileobjs[filename] = data
                    self.inputs[filename] = data
                    self.objects[filename] = data
                else:
                    if requires_deepcopy:
                        data = data.__deepcopy__()

                node_input.append(data)

        # Do the same for the output port. In some cases we are not
        # allowed to access the output port and this is when we set
        # the structure to None.
        output_ports = parameters['ports'].get('outputs', [])
        if exclude_output:
            node_output = _build_mem_ports(output_ports)
        else:
            # Generate output port object structure.
            node_output = []
            for output_port in output_ports:
                filename = output_port['file']
                if self._check_fns:
                    assert(filename != '')
                data = self.outputs.get(filename)

                if data is None:
                    if self._is_output_node:
                        data = port_util.port_maker(
                            output_port, 'r' if read_only else 'w',
                            True,
                            expanded=node._expanded,
                            managed=node._managed)
                        self.output_fileobjs[filename] = data
                    else:
                        data = port_util.port_maker(output_port, None,
                                                    None,
                                                    no_datasource=True)
                    self.outputs[filename] = data
                    self.objects[filename] = data

                node_output.append(data)

        # Users should not really need to have access to the node definition?
        node_definition = parameters

        # Copy parameter structure
        node_parameters = parameters['parameters'].get('data', {})
        update_parameters(node, node_parameters)
        if bind:
            update_bindings(
                node_parameters, node_definition, node_input, node_output)

        own_objects = dict(self.output_fileobjs)
        own_objects.update(self.input_fileobjs)

        # Initialize instance of NodeContext.
        node_context = node.create_node_context(
            node_input,
            node_output,
            node_definition,
            node_parameters,
            node_typealiases.values(),
            self.objects,
            set(own_objects.values()))
        node_context.__exit__ = void
        return node_context


class ConfirmChangesDialogMixin(object):
    """
    Add this mixin class as a parent class to any configuration QDialog where
    you want a confirmation dialog when pressing cancel.

    There are two requirements on subclasses:
    1. ConfirmChangesDialogMixin must come before the QDialog in the list of
       parent classes. Otherwise keyPressEvent, reject, and done will not be
       called.
    2. Subclasses must override parameters_changed and cleanup.
    """
    def __init__(self, *args, **kwargs):
        super(ConfirmChangesDialogMixin, self).__init__(*args, **kwargs)
        self._use_dialog = settings.settings()['Gui/nodeconfig_confirm_cancel']

    def parameters_changed(self):
        raise NotImplementedError

    def cleanup(self):
        raise NotImplementedError

    def keyPressEvent(self, event):
        # Only accept Ctrl+Enter as Ok and Esc as Cancel.
        # This is to avoid closing the dialog by accident.
        if ((event.key() == QtCore.Qt.Key_Return or
                event.key() == QtCore.Qt.Key_Enter) and
                event.modifiers() & QtCore.Qt.ControlModifier):
            self.accept()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.reject()

    def reject(self):
        """
        Ask the user if the dialog should be closed.
        Reject/accept the dialog as appropriate.
        """
        # For a QDialog reject is the place to modify closing behavior, not
        # closeEvent.
        if not self._use_dialog:
            self._reject_immediately()
        elif self.parameters_changed():
            res = self._confirm_cancel_dialog()
            if res is None:
                return
            else:
                if res:
                    self.accept()
                else:
                    self._reject_immediately()
        else:
            self._reject_immediately()

    def done(self, r):
        # At this point we know that the dialog will close, so this is a good
        # place to do cleanup.
        self.cleanup()
        super(ConfirmChangesDialogMixin, self).done(r)

    def _reject_immediately(self):
        super(ConfirmChangesDialogMixin, self).reject()

    def _confirm_cancel_dialog(self):
        """
        Ask the user if the parameter dialog should be closed.

        Returns True if the parameters were accepted, False if they were
        rejected and None if the user cancels.
        """
        choice = QtWidgets.QMessageBox.question(
            self, 'Save changes to configuration',
            "The node's configuration has changed. Save changes in node?",
            QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard |
            QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Cancel)

        if choice == QtWidgets.QMessageBox.Discard:
            return False
        elif choice == QtWidgets.QMessageBox.Save:
            return True
        else:
            return None


class ParametersWidgetMixin(object):
    def __init__(self, *args, **kwargs):
        super(ParametersWidgetMixin, self).__init__(*args, **kwargs)
        self._widget = None
        self._message_widget = None
        self._parameters_changed = None
        self._valid = False

    def set_configuration_widget(self, widget):
        self._widget = widget

    def set_message_widget(self, widget):
        self._message_widget = widget

    def set_changed_checker(self, func):
        self._parameters_changed = func

    def parameters_changed(self):
        if self._parameters_changed is None:
            return None
        else:
            # First notify the widget that it should save its parameters so
            # that they can be compared.
            self.save_parameters()
            return self._parameters_changed()

    def save_parameters(self):
        if hasattr(self._widget, 'save_parameters'):
            self._widget.save_parameters()

    def cleanup(self):
        if hasattr(self._widget, 'cleanup'):
            self._widget.cleanup()

    def update_status(self):
        status = self._widget.valid
        self._valid = status
        # set ok button status
        if self._message_widget is not None:
            message = self._widget.status
            color_state = (not status) + (message != '')

            self._message_widget.set_state(color_state)
            self._message_widget.set_message(six.text_type(message))
        self.valid_changed.emit()

    def has_preview(self):
        return hasattr(self._widget, 'set_preview_active')

    def set_preview_active(self, value):
        if self.has_preview():
            self._widget.set_preview_active(value)

    def preview_active(self):
        if self.has_preview():
            return self._widget.preview_active()
        return False

    @property
    def valid(self):
        return self._valid

    @valid.setter
    def valid(self, value):
        self._valid = value


class ParametersWidget(ParametersWidgetMixin, QtWidgets.QWidget):
    valid_changed = QtCore.Signal()


class ParametersDialog(ParametersWidgetMixin, ConfirmChangesDialogMixin,
                       QtWidgets.QDialog):
    help_requested = QtCore.Signal()
    valid_changed = QtCore.Signal()

    def __init__(self, widget, name, socket_bundle,
                 *args, **kwargs):
        super(ParametersDialog, self).__init__(*args, **kwargs)

        self._input_comm = socket_bundle
        self._input_reader = message_util.QtSocketMessageReader(
            socket_bundle.socket, self)
        self._input_reader.received.connect(self.handle_input)

        layout = QtWidgets.QVBoxLayout()
        button_box = QtWidgets.QDialogButtonBox()
        self._help_button = button_box.addButton(
            QtWidgets.QDialogButtonBox.Help)

        if isinstance(widget, preview.ParameterPreviewWidget):
            self._preview_button = sywidgets.PreviewButton()
            self._preview_button.toggled.connect(widget.set_preview_active)

            button_box.addButton(self._preview_button,
                                 QtWidgets.QDialogButtonBox.ActionRole)

        self._ok_button = button_box.addButton(QtWidgets.QDialogButtonBox.Ok)
        self._cancel_button = button_box.addButton(
            QtWidgets.QDialogButtonBox.Cancel)
        self._ok_button.setDefault(False)

        # Reducing white space around widgets
        widget.setContentsMargins(0, 0, 0, 0)
        widgetlayout = widget.layout()
        if widgetlayout:
            widget.layout().setContentsMargins(0, 0, 0, 0)

        # Message box
        message_box = MessageBox(parent=self)
        layout.addWidget(message_box)
        layout.addWidget(widget)
        layout.addWidget(button_box)
        self.setLayout(layout)
        self.set_configuration_widget(widget)
        self.set_message_widget(message_box)
        self.setWindowFlags(QtCore.Qt.Window)

        self._help_button.clicked.connect(self.help_requested)
        self._ok_button.clicked.connect(self.accept)
        self._cancel_button.clicked.connect(self.reject)
        self.accepted.connect(self.save_parameters)

        if isinstance(widget, ParameterView):
            widget.status_changed.connect(self.update_status)

        self.setWindowTitle(name)
        self.show()
        self.raise_()
        self.activateWindow()
        if isinstance(widget, ParameterView):
            self.update_status()
        QtCore.QTimer.singleShot(0, focus_widget(self))

    def handle_input(self, msgs):
        for msg in msgs:
            if msg.type == message.RaiseWindowMessage:
                self.raise_window()
            elif msg.type == message.NotifyWindowMessage:
                self.notify_in_taskbar()

    def raise_window(self):
        if not self.isActiveWindow():
            os_support.raise_window(self)

    def notify_in_taskbar(self):
        QtWidgets.QApplication.alert(self, 2000)

    def update_status(self):
        status = self._widget.valid
        # set ok button status
        if self._ok_button is not None:
            self._ok_button.setEnabled(status)

        super(ParametersDialog, self).update_status()


class MessageBox(QtWidgets.QScrollArea):
    """
    Widget showing messages in the ParametersDialog.

    The messages allow html formatting and hyperlinks are opened in an
    external browser. The background color can be set with `set_state`.
    The MessageBox can be set to disappear after a given timeout interval.
    """

    def __init__(self, parent=None):
        super(MessageBox, self).__init__(parent)
        self._init_gui()
        self.hide()

    def _init_gui(self):
        self.setFrameStyle(QtWidgets.QFrame.Box)
        self.message_label = QtWidgets.QLabel(self)
        self.message_label.setTextFormat(QtCore.Qt.RichText)
        self.message_label.setWordWrap(True)
        self.message_label.setOpenExternalLinks(True)
        self.message_label.setContentsMargins(5, 5, 5, 5)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidget(self.message_label)
        self.setWidgetResizable(True)
        policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                       QtWidgets.QSizePolicy.Minimum)
        self.setSizePolicy(policy)

        self._timer_show = QtCore.QTimer()
        self._timer_show.setInterval(500)
        self._timer_show.setSingleShot(True)

        font_height = self.message_label.fontMetrics().height()
        self.setMinimumHeight(font_height * 1 + 12)
        self.setMaximumHeight(font_height * 4 + 12)

        self._timer_show.timeout.connect(self._show)

    def minimumSizeHint(self):
        return QtCore.QSize(
            self.minimumWidth(),
            min([self.maximumHeight(),
                 self.message_label.minimumSizeHint().height()]))

    def set_background_color(self, color):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def set_message(self, message):
        message = six.text_type(message)
        self.message_label.setText(message)
        if message == '':
            self.disable()
        else:
            self.enable()

    def set_state(self, state):
        """
        Set the state which defines the color. Allowed [0,1,2].

        Parameters
        ----------
        state : int
            The state defines the color of the message box background.
            0 : green   (info)
            1 : yellow  (warning)
            2 : red     (error)
        """
        if state not in [0, 1, 2]:
            state = 2

        colors = {0: QtGui.QColor.fromRgb(204, 235, 197),
                  1: QtGui.QColor.fromRgb(254, 217, 166),
                  2: QtGui.QColor.fromRgb(251, 180, 174)}

        self.set_background_color(colors[state])

    def set_show_interval(self, interval):
        """Set the time after which the error is shown."""
        self._timer_show.setInterval(int(interval))

    def _show(self):
        self.setVisible(True)

    def enable(self):
        if not self.isVisible():
            self._timer_show.start()

    def disable(self):
        self.setVisible(False)
        self._timer_show.stop()


class BasicNode(object):
    """
    Base class for Sympathy nodes. Fully implements the
    language interface needed to work as a fully functional
    node inside the Sympathy platform. All Python2 nodes
    should extend this class.
    """

    def __init__(self):
        self.active_file = None
        self.address = None
        self.abort_flag = False
        self.filenames = []
        self._expanded = True
        self._managed = False
        self.socket_bundle = None

    def set_progress(self, value):
        """Set and send progress to main program."""
        if self.socket_bundle:
            network.send_all(
                self.socket_bundle.socket,
                self.socket_bundle.output_func(
                    message.ProgressMessage(value)))

    def set_status(self, status):
        """Send status message to main program."""
        msg = b'STATUS %s\n' % status
        if self.socket_bundle:
            network.send_all(
                self.socket_bundle.socket,
                self.socket_bundle.output_func(
                    message.StatusMessage(msg)))

    # Methods to be overidden by user.
    @original
    def verify_parameters_basic(self, node_context):
        """Check if configuration is ok."""
        return True

    def update_parameters_basic(self, old_params):
        """
        Update parameters to newer version of node.
        Returns updated parameters.
        """
        raise NotImplementedError(
            'update_parameters() has no default implementation')

    def adjust_parameters_basic(self, node_context):
        """Adjust parameter object."""
        # Default to no changes.
        return node_context

    def execute_basic(self, node_context):
        """
        Execute node. This method should always be extended by
        the inhereting class.
        """
        raise NotImplementedError('execute() must be implemented')

    @managed_context
    def __execute_pass_basic(self, node_context):
        pass

    def available_components(self):
        """
        Return a list of available visual components which the node
        can visualize things through.
        """
        return []

    def exec_parameter_view_basic(self, node_context):
        """
        Return parameter dictionary which was edited by the
        user. Accept and reject is handled by the platform.
        """
        raise NotImplementedError('Specialized class must be '
                                  'used for parameter view.')

    def _manual_context(self, node_context):
        # Used for enabling the user to close the context afterwards.
        # In this base class the close function, int, does nothing and is used
        # as an empty close action since the base behavior is manual
        # context management.
        close_function = int
        close_handles = {'inputs': {key: close_function
                                    for key in node_context.input},
                         'outputs': {key: close_function
                                     for key in node_context.output}}
        return node_context, close_handles

    def _preview_ports(self, node_context):
        def should_preview(pdef, i):
            name = pdef.get('name')
            if not name:
                name = i
            try:
                return self.outputs[name].preview
            except (KeyError, IndexError, AttributeError):
                return False

        return [should_preview(pdef, i) for i, pdef in
                enumerate(
                    node_context.definition['ports']['outputs'])]

    def _build_parameter_widget(self, node_context):
        """
        Creates the configuration widget either from a custom widget
        (exec_parameter_view) or from the parameter definition. The return
        value is a tuple of the parameter root (or None) and the widget.
        """

        try:
            # Custom GUI.
            return None, self.exec_parameter_view_basic(node_context)
        except NotImplementedError:
            pass

        # Generated GUI.
        proot = ParameterRoot(node_context.parameters,
                              update_lists=True)
        visitor = WidgetBuildingVisitor
        if not self._managed:
            # Validator is disabled for basic nodes.
            widget_builder = visitor()
        else:
            widget_builder = visitor(self.verify_parameters)

        proot.accept(widget_builder)
        widget = widget_builder.gui()
        # Controller support.
        controllers = getattr(self, 'controllers', None)
        if controllers is not None:
            widget_dict = widget_builder.widget_dict()
            if isinstance(controllers, collections.Iterable):
                for controller in controllers:
                    controller.connect(widget_dict)
            else:
                controllers.connect(widget_dict)

        preview_ports = self._preview_ports(node_context)

        if any(preview_ports):
            preview_widget = preview.PreviewWidget(self, node_context, proot)
            widget = preview.ParameterPreviewWidget(widget, preview_widget)

        return (proot, widget)

    def _execute_parameter_view(self, node_context, return_widget=False,
                                include_messagebox=False):
        """
        Builds the parameters widget and (if return_widget is False) wraps it
        in a ParametersDialog.

        If return_widget is True the parameters widget is returned as is.
        """
        if hasattr(self, 'execute_parameter_view'):
            sywarn('Overriding execute_parameter_view '
                   'is no longer supported.')
        if (hasattr(self, 'has_parameter_view') or
                hasattr(self, 'has_parameter_view_managed')):
            sywarn('Implementing has_parameter_view or '
                   'has_parameter_view_managed no longer has any effect.')

        proot, widget = self._build_parameter_widget(node_context)

        if isinstance(widget, ParameterView):
            # Save any changes to the parameters from just creating the
            # widget. Each node is responsible that such changes don't
            # change how the node executes.
            widget.save_parameters()
        if isinstance(node_context.parameters, ParameterRoot):
            parameter_dict = node_context.parameters.parameter_dict
        else:
            parameter_dict = node_context.parameters
        old_parameter_dict = copy.deepcopy(parameter_dict)

        # Save parameters in a closure so that ParametersDialog can check
        # them after parameter_dict has (possibly) been mutated.
        def parameters_changed():
            return old_parameter_dict != parameter_dict

        if return_widget:
            if return_widget == 'parameters_widget':
                layout = QtWidgets.QVBoxLayout()
                parameters_widget = ParametersWidget()
                message_box = MessageBox(parent=parameters_widget)
                layout.addWidget(message_box)
                layout.addWidget(widget)
                parameters_widget.set_configuration_widget(widget)
                parameters_widget.set_message_widget(message_box)
                parameters_widget.set_changed_checker(parameters_changed)
                parameters_widget.setLayout(layout)
                parameters_widget.setWindowFlags(QtCore.Qt.Window)

                if isinstance(widget, ParameterView):
                    widget.status_changed.connect(
                        parameters_widget.update_status)

                if proot is not None:
                    proot.value_changed.add_handler(
                        parameters_widget.update_status)

                if isinstance(widget, ParameterView):
                    parameters_widget.update_status()
                else:
                    parameters_widget.valid = True
                return parameters_widget
            return widget

        dialog = None
        try:
            application = QtWidgets.QApplication.instance()
            app_name = format_display_string(
                node_context.definition['label'])
            name = '{} - Parameter View'.format(app_name)
            application.setApplicationName(name)

            dialog = ParametersDialog(widget, name, self.socket_bundle)
            if proot is not None:
                proot.value_changed.add_handler(dialog.update_status)
            dialog.help_requested.connect(functools.partial(
                self._open_node_documentation, node_context))
            dialog.set_changed_checker(parameters_changed)

            icon = node_context.definition.get('icon', None)
            if icon:
                try:
                    icon_data = QtGui.QIcon(uri_to_path(icon))
                    application.setWindowIcon(icon_data)
                except Exception:
                    pass

            application.exec_()
            return dialog.result()
        finally:
            if dialog and hasattr(dialog, 'close'):
                dialog.close()
            # Ensure GC
            dialog = None

    def _sys_exec_parameter_view(self, parameters, type_aliases,
                                 return_widget=False,
                                 builder=BaseContextBuilder()):
        """Execute parameter view and return any changes."""
        # Remember old parameters.
        old = copy.deepcopy(parameters)

        adjusted_parameters = self._sys_adjust_parameters(parameters,
                                                          type_aliases,
                                                          builder=builder)

        node_context = self._build_node_context(adjusted_parameters,
                                                type_aliases,
                                                exclude_output=True,
                                                builder=builder)

        result = self._execute_parameter_view(
            node_context, return_widget=return_widget)
        if return_widget:
            # In this case the result from self.exec_parameter_view is the
            # configuration widget
            return result
        elif result == QtWidgets.QDialog.Accepted:
            return adjusted_parameters
        else:
            return old

    def exec_port_viewer(self, parameters):
        from sympathy.platform.viewer import MainWindow as ViewerWindow
        filename, index, node_name, icon = parameters
        try:
            application = QtWidgets.QApplication.instance()
            name = format_display_string(
                '{}: {} - Viewer'.format(node_name, index))
            application.setApplicationName(name)
            viewer = ViewerWindow(name, self.socket_bundle, icon)
            viewer.open_from_filename(filename)

            viewer.show()
            viewer.resize(800, 600)
            viewer.raise_()
            viewer.activateWindow()
            QtCore.QTimer.singleShot(0, focus_widget(viewer))

            if icon:
                try:
                    icon_data = QtGui.QIcon(viewer.build_icon())
                    application.setWindowIcon(QtGui.QIcon(icon_data))
                except Exception:
                    pass

            application.exec_()
        finally:
            viewer = None

    def _sys_before_execute(self):
        """Always executed before main execution."""
        pass

    def _sys_execute(self, parameters, type_aliases,
                     builder=BaseContextBuilder()):
        """Called by the Sympathy platform when executing a node."""
        node_context = self._build_node_context(parameters, type_aliases,
                                                builder=builder, bind=True)
        if self._only_conf(parameters, node_context):
            self.__execute_pass_basic(node_context)
        else:
            self.execute_basic(node_context)

    def _sys_after_execute(self):
        """Always executed after main execution."""
        pass

    def _sys_verify_parameters(self, parameters, type_aliases):
        """Check if parameters are valid."""
        node_context = self._build_node_context(parameters,
                                                type_aliases,
                                                exclude_output=True,
                                                exclude_input=True)
        try:
            return self.verify_parameters_basic(node_context)
        except: # NOQA (capture any error in user code)
            sywarn('Error in validate_parameters, input data should not be'
                   ' used for validation.')
            return False

    def _sys_adjust_parameters(self, parameters, type_aliases,
                               builder=BaseContextBuilder()):
        """Adjust node parameters."""
        adjusted_parameters = copy.deepcopy(parameters)
        node_context = self._build_node_context(adjusted_parameters,
                                                type_aliases,
                                                exclude_output=True,
                                                builder=builder)
        self.adjust_parameters_basic(node_context)
        return adjusted_parameters

    def _build_node_context(self, parameters, typealiases,
                            exclude_output=False,
                            exclude_input=False,
                            read_only=False,
                            builder=BaseContextBuilder(), bind=False):
        """Build node context object."""
        return builder.build(self, parameters, typealiases,
                             exclude_output=exclude_output,
                             exclude_input=exclude_input,
                             read_only=read_only, bind=bind)

    def _build_file_port_or_dummy(self, dummy_port_maker, port_dict, mode):
        return dummy_port_maker(port_dict, mode, True,
                                expanded=self._expanded,
                                managed=self._managed)

    def _build_file_ports_or_dummys(self, dummy_port_maker, port_dicts, mode):
        return [
            self._build_file_port_or_dummy(dummy_port_maker, port_dict, mode)
            for port_dict in port_dicts]

    @staticmethod
    def create_node_context(inputs, outputs, definition, parameters,
                            typealiases, objects=None, own_objects=None):
        objects = {} if objects is None else objects
        input_ports = definition['ports'].get('inputs', [])
        output_ports = definition['ports'].get('outputs', [])

        return NodeContext(port_util.RunPorts(inputs,
                                              input_ports),
                           port_util.RunPorts(outputs,
                                              output_ports),
                           definition,
                           parameters,
                           typealiases,
                           objects,
                           own_objects)

    @classmethod
    def update_node_context(cls, node_context, inputs=None, outputs=None,
                            parameters=None):
        if parameters is None:
            parameters = node_context.parameters
        if inputs is None:
            inputs = node_context.input
        if outputs is None:
            outputs = node_context.output

        return cls.create_node_context(
            inputs, outputs, node_context.definition,
            parameters, node_context.typealiases, node_context._objects,
            node_context._own_objects)

    def _open_node_documentation(self, node_context):
        path_in_library = os.path.dirname(os.path.relpath(
            uri_to_path(node_context.definition['source_file']),
            uri_to_path(node_context.definition['library'])))
        doc_path = nativepath(os.path.join(
            'Library', path_in_library, self.__class__.__name__ + '.html'))

        if self.socket_bundle:
            network.send_all(
                self.socket_bundle.socket,
                self.socket_bundle.output_func(
                    message.RequestHelpMessage(doc_path)))

    def _beg_capture_text_streams(self, node_context):
        self._org_sys_stdout = sys.stdout
        self._org_sys_stderr = sys.stderr
        self._cap_sys_stdout = six.StringIO()
        self._cap_sys_stderr = six.StringIO()
        out = node_context.output.group('__sy_out__')
        err = node_context.output.group('__sy_err__')
        both = node_context.output.group('__sy_both__')

        if both:
            sys.stdout = self._cap_sys_stdout
            sys.stderr = self._cap_sys_stdout
        else:
            if out:
                sys.stdout = self._cap_sys_stdout
            if err:
                sys.stderr = self._cap_sys_stderr

    def _end_capture_text_streams(self, node_context):
        sys.stdout = self._org_sys_stdout
        sys.stderr = self._org_sys_stderr
        out = node_context.output.group('__sy_out__')
        err = node_context.output.group('__sy_err__')
        both = node_context.output.group('__sy_both__')

        if both:
            both[0].set(self._cap_sys_stdout.getvalue())
        else:
            if out:
                out[0].set(self._cap_sys_stdout.getvalue())
            if err:
                err[0].set(self._cap_sys_stderr.getvalue())
        self._cap_sys_stderr = None
        self._cap_sys_stdout = None
        self._org_sys_stdout = None
        self._org_sys_stderr = None

    def _text_stream_ports(self, node_context):
        return [port for name in ['__sy_out__', '__sy_err__', '__sy_both__']
                for port in node_context.output.group(name)]

    def _conf_ports(self, node_context):
        return [port for name in ['__sy_conf__']
                for port in node_context.output.group(name)]

    def _only_conf(self, parameters, node_context):
        name = 'only_conf'
        return parameters.get(name) and self._conf_ports(node_context)


def focus_widget(dialog):
    def inner():
        os_support.focus_widget(dialog)
    return inner


def sy_parameters(obj=None, update_lists=False, warn=True):
    if obj is None:
        return ParameterRoot()
    elif isinstance(obj, ParameterRoot):
        return obj
    return ParameterRoot(obj, update_lists=update_lists, warn=warn)
