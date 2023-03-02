from datetime import datetime
from dateutil.tz import tzlocal

import numpy as np
from pynwb import NWBFile, NWBHDF5IO
from pynwb.ecephys import ElectricalSeries, LFP

nwbfile = NWBFile(
    session_description="	Human_MTL_units_scalp_EEG_and_iEEG_verbal_WM",
    identifier="TODO_ID",
    session_start_time=datetime(2019, 3, 27),  # TODO: That was just publication date
    experimenter="Dr. Johannes Sarnthein",  # TODO: I don't know
    lab="Johannes Sarnthein Lab",
    institution="University of Zurich",
    experiment_description="TODO",
    session_id="TODO_ID2",
)

device = nwbfile.create_device(
    name="NicoletOne EEG", description="TODO", manufacturer="Natus Medical Incorporated"
)
nwbfile.add_electrode_column(name="label", description="label of electrode")

nshanks = 19
nchannels_per_shank = 3
electrode_counter = 0

for ishank in range(nshanks):
    # create an electrode group for this shank
    electrode_group = nwbfile.create_electrode_group(
        name="shank{}".format(ishank),
        description="electrode group for shank {}".format(ishank),
        device=device,
        location="brain area",
    )
    # add electrodes to the electrode table
    for ielec in range(nchannels_per_shank):
        nwbfile.add_electrode(
            group=electrode_group,
            label="shank{}elec{}".format(ishank, ielec),
            location="brain area",
        )
        electrode_counter += 1
nwbfile.electrodes.to_dataframe()
