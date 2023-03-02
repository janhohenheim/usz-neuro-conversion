import nixio
from os.path import join
import numpy as np

nix_dir = join("/", "mnt", "c", "Users", "conta", "git", "USZ_NCH", "Human_MTL_units_scalp_EEG_and_iEEG_verbal_WM",
               "data_nix")
file_path = join(nix_dir, "Data_Subject_01_Session_01.h5")
nixfile = nixio.File.open(file_path, nixio.FileMode.ReadOnly)

# print(nixfile.sections)
# print(nixfile.sections["General"].props["Recording location"].values)
# print(nixfile.sections["General"].sections["Recording setup"].props["Recording setup EEG"].values)

electrode_map = nixfile.blocks[
    "Data_Subject_01_Session_01"].groups[
    "Scalp EEG electrode information"].data_arrays[
    "Scalp_Electrode_EEGLAB_BESA_Coordinates"]
electrode_map_array = np.ndarray(electrode_map.shape)
electrode_map.read_direct(electrode_map_array)
print(electrode_map_array)
print(electrode_map_array.shape)
# nixfile.pprint()
