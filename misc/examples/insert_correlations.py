#!/usr/bin/env python
if __name__ == "__main__":
    import os, sys
    import numpy as np
    from models import Simulation, CorrelationComponent, get_session, db_file

    corr_folder = os.path.realpath(os.path.join(
        os.path.split(__file__)[0],
        os.pardir, os.pardir,
        'output', 'polarization-zstar', 'correlations'))

    session = get_session(db_file)

    for simulation in session.query(Simulation).all():
        jid = simulation.name
        print >> sys.stderr, "# (Calculating and) inserting correlations for {}...".format(jid)

        prefix = 'corr_{}_cubic_'.format(jid)
        suffix = '.dat'
        correlations = [fname for fname in os.listdir(corr_folder)
                        if fname.startswith(prefix) and fname.endswith(suffix)]
        
        for fname in correlations:
            neighbor_info, component = fname[len(prefix):-len(suffix)].split(
                '_')

            ## With .first() we check if there is at least one result
            if session.query(CorrelationComponent).filter(
                    CorrelationComponent.simulation==simulation, 
                    CorrelationComponent.component==component, 
                    CorrelationComponent.neighbor_info==neighbor_info).first():
                print "Skipping {}_{} ({})".format(
                    jid, component, neighbor_info)
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
            # two columns: time and correlation
            corr_value = data[:,1].mean()
            corr_value_2nd_half = data[int(num_time_frames/2.):,1].mean()

            #Insert correlation components
            corr_comp = CorrelationComponent(
                simulation=simulation, 
                component=component, 
                neighbor_info=neighbor_info,
                value=corr_value,
                value_second_half=corr_value_2nd_half)
            session.add(corr_comp)

        # Commit after each simulation
        session.commit()

