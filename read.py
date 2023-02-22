import nixio
from os.path import join

nix_dir = join("/", "mnt", "c", "Users", "conta", "git", "USZ_NCH", "Human_MTL_units_scalp_EEG_and_iEEG_verbal_WM",
               "data_nix")
file_path = join(nix_dir, "Data_Subject_01_Session_01.h5")
nixfile = nixio.File.open(file_path, nixio.FileMode.ReadOnly)
print(nixfile.sections)
# nixfile.pprint()
