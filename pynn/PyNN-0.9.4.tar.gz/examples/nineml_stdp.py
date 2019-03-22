"""
This example doesn't run at the moment

Based on https://github.com/NeuralEnsemble/pype9/blob/0d4eb0c9a6a4fe041cff114de3831de79157e634/test/test_simulations/test_network.py

"""

from nineml.abstraction import (
    Parameter, Dynamics, Regime, On, OutputEvent, StateVariable,
    StateAssignment, Constant, Alias)
from nineml.abstraction.ports import (
    AnalogSendPort, AnalogReceivePort, AnalogReducePort, EventSendPort,
    EventReceivePort)
from nineml import units as un


import pyNN.neuron as sim


# Define synapse type in 9ML

# this model is purely event based, but it is also possible to define
# rules with explicit ODEs for the state variables
stdp_cls = Dynamics(
            name="PartialStdpGuetig",
            parameters=[
                Parameter(name='tauLTP', dimension=un.time),
                Parameter(name='aLTD', dimension=un.dimensionless),
                Parameter(name='wmax', dimension=un.dimensionless),
                Parameter(name='muLTP', dimension=un.dimensionless),
                Parameter(name='tauLTD', dimension=un.time),
                Parameter(name='aLTP', dimension=un.dimensionless)],
            analog_ports=[
                AnalogSendPort(dimension=un.dimensionless, name="wsyn"),
                AnalogSendPort(dimension=un.current, name="wsyn_current")],
            event_ports=[
                EventReceivePort(name="incoming_spike")],
            state_variables=[
                StateVariable(name='tlast_post', dimension=un.time),
                StateVariable(name='tlast_pre', dimension=un.time),
                StateVariable(name='deltaw', dimension=un.dimensionless),
                StateVariable(name='interval', dimension=un.time),
                StateVariable(name='M', dimension=un.dimensionless),
                StateVariable(name='P', dimension=un.dimensionless),
                StateVariable(name='wsyn', dimension=un.dimensionless)],
            constants=[Constant('ONE_NA', 1.0, un.nA)],
            regimes=[
                Regime(
                    name="sole",
                    transitions=On(
                        'incoming_spike',
                        to='sole',
                        do=[
                            StateAssignment('tlast_post', 't'),
                            StateAssignment('tlast_pre', 'tlast_pre'),
                            StateAssignment(
                                'deltaw',
                                'P*pow(wmax - wsyn, muLTP) * '
                                'exp(-interval/tauLTP) + deltaw'),
                            StateAssignment('interval', 't - tlast_pre'),
                            StateAssignment(
                                'M', 'M*exp((-t + tlast_post)/tauLTD) - aLTD'),
                            StateAssignment(
                                'P', 'P*exp((-t + tlast_pre)/tauLTP) + aLTP'),
                            StateAssignment('wsyn', 'deltaw + wsyn')]))],
            aliases=[Alias('wsyn_current', 'wsyn * ONE_NA')])


# Define PyNN network

sim.setup(timestep=0.1, min_delay=0.5, max_delay=2.0)

synapse_type_cls = sim.nineml.nineml_synapse_type_from_model(
    name="PartialStdpGuetig",
    nineml_model=stdp_cls,
    units_scheme="default")  # e.g. mV for voltages
synapse_type = synapse_type_cls(**{'tauLTP': 10.0,
                                   'aLTD': 1.0,
                                   'wmax': 2.0,
                                   'muLTP': 3.0,
                                   'tauLTD': 20.0,
                                   'aLTP': 4.0})

neurons = sim.Population(100, sim.EIF_cond_exp_isfa_ista())

connections = sim.Projection(neurons, neurons,
                             sim.FixedProbabilityConnector(p_connect=0.2),
                             synapse_type=synapse_type,
                             receptor_type="excitatory")

sim.run(100.0)

sim.end()
