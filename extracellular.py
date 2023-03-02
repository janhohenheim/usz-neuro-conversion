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

group_count = 19
channels_per_group = 1

for group in range(group_count):
    # create an electrode group for this group
    electrode_group = nwbfile.create_electrode_group(
        name="group{}".format(group),
        description="electrode group for shank {}".format(group),
        device=device,
        location="brain area",
        position=[0, 0, 0],
    )
    # add electrodes to the electrode table
    for channel in range(channels_per_group):
        nwbfile.add_electrode(
            group=electrode_group,
            label="group{}channel{}".format(group, channel),
            location="brain area",
            reference="Averaged mastoid channels",
        )
print(nwbfile.electrodes.to_dataframe())
