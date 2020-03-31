#!/usr/bin/env python
"""
This script has to be run after insert_correlations.py.
It adds data to the value_second_half column, with the correlation, but only for the second
half of the simulation. This will be used as an estimate of the error.
"""
if __name__ == "__main__":
    import os, sys
    import numpy as np
    from models import Simulation, CorrelationComponent, get_session, db_file
    from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

    corr_folder = os.path.realpath(os.path.join(
        os.path.split(__file__)[0],
        os.pardir, os.pardir,
        'output', 'polarization-zstar', 'correlations'))

    session = get_session(db_file)

    for simulation in session.query(Simulation).all():
        jid = simulation.name
        print >> sys.stderr, "# (Calculating and) inserting correlations (only 2nd half) for {}...".format(jid)

        prefix = 'corr_{}_cubic_'.format(jid)
        suffix = '.dat'
        correlations = [fname for fname in os.listdir(corr_folder)
                        if fname.startswith(prefix) and fname.endswith(suffix)]
        
        for fname in correlations:
            neighbor_info, component = fname[len(prefix):-len(suffix)].split(
                '_')

            try:
                # Get pre-filled correlation component, should be only one
                corr_comp = session.query(CorrelationComponent).filter(
                    CorrelationComponent.simulation==simulation, 
                    CorrelationComponent.component==component, 
                    CorrelationComponent.neighbor_info==neighbor_info).one()
            except NoResultFound:
                print "NO CORRELATION FOR {}_{} ({})! Did you run ./insert_correlations.py first? Skipping...".format(
                    jid, component, neighbor_info)
                continue
            except MultipleResultsFound:
                print "MULTIPLE CORRELATIONS FOR {}_{} ({})! How can it be? It should be unique... I stop.".format(
                    jid, component, neighbor_info)
                sys.exit(1)
                
            if corr_comp.value_second_half is not None:
                print "Skipping {}_{} ({}), has already {}".format(
                    jid, component, neighbor_info, corr_comp.value_second_half)
                continue
            else:
                print "Analyzing {}_{} ({})".format(
                    jid, component, neighbor_info)               

            # Doing it manually is much faster
            #data = np.loadtxt(os.path.join(
            #    corr_folder, fname))
            data = []
            with open(os.path.join(
                    corr_folder, fname)) as f:
                for l in f:
                    data.append(map(float, l.split()))
            data = np.array(data)

            num_time_frames = data.shape[0]

            # average = autocorr at Delta t=0
            # two columns: time and correlation. I 
            # only use the second half of the data!
            corr_value_2nd_half = data[int(num_time_frames/2.):,1].mean()

            #Insert correlation components
            corr_comp.value_second_half = corr_value_2nd_half

        # Commit after each simulation
        session.commit()

