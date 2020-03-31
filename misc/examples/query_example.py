#!/usr/bin/env python
from models import Simulation, CorrelationComponent, get_session, db_file

session = get_session(db_file)

# Make a query to find all Simulations in the database
print "# All simulations:"
for res in session.query(Simulation).order_by(
        Simulation.species_name, Simulation.cell_shape, 
        Simulation.temperature).all():
    extra = " ({})".format(res.label_extra.strip()) if res.label_extra else ""
    print "- {:6s}, {} ({}), T={:3.0f} +- {:4.1f}K, {:3.0f} ps{}".format(
        res.name, res.species_name, res.cell_shape[:3], 
        res.temperature, res.temperature_error, res.max_time,
        extra)

# First simulation
simulation = session.query(Simulation).first()
print "# Example of one simulation: ({}) {}".format(simulation.id, simulation.name)

# Find all 'xx' correlations of this simulation
print "# Only xx:"
for res in session.query(CorrelationComponent).filter(
        CorrelationComponent.simulation == simulation, 
        CorrelationComponent.component == 'xx').all():
    print "{:10s} {}".format(res.neighbor_info, res.value)

