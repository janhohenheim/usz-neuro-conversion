from pathlib import Path
from zoneinfo import ZoneInfo
import nixio
from dataclasses import dataclass
from pynwb import NWBFile, NWBHDF5IO
from os.path import join
import pandas as pd
import numpy as np
from datetime import datetime
import pathlib


@dataclass(frozen=True)
class NixContext:
    subject: int
    session: int
    project: str

    def to_session_context(self, nix: nixio.File, nwb: NWBFile) -> 'SessionContext':
        return SessionContext(self.subject, self.session, nix, nwb, self.project)


@dataclass(frozen=True)
class NwbContext:
    subject: int
    session: int
    project: str


@dataclass(frozen=True)
class SessionContext:
    subject: int
    session: int
    nix: nixio.File
    nwb: NWBFile
    project: str

    def to_nix_context(self) -> NixContext:
        return NixContext(self.subject, self.session, self.project)

    def to_nwb_context(self) -> NwbContext:
        return NwbContext(self.subject, self.session, self.project)


def read_nix(ctx: NixContext) -> nixio.File:
    nix_dir = join(_get_in_dir(), "to_convert", ctx.project, "data_nix")
    file_path = join(nix_dir, f"Data_Subject_{ctx.subject:02}_Session_{ctx.session:02}.h5")
    return nixio.File.open(file_path, nixio.FileMode.ReadOnly)


def _get_in_dir() -> str:
    current_file = pathlib.Path(__file__).parent.parent.resolve()
    return join(current_file, "in")


def _get_in_dir() -> str:
    return join(_get_project_dir(), "in")


def _get_out_dir() -> str:
    return join(_get_project_dir(), "out")


def _get_project_dir() -> Path:
    return pathlib.Path(__file__).parent.parent.resolve()


def get_metadata_row(ctx: NixContext) -> pd.Series:
    df = _read_session_metadata()
    right_participant = df["Participant"] == ctx.subject
    right_session = df["Session"] == ctx.session
    right_dataset = df["Dataset"] == ctx.project
    return df.loc[right_participant & right_session & right_dataset].iloc[0]


def get_date(ctx: NixContext) -> datetime:
    metadata = get_metadata_row(ctx)
    date = metadata["Date"].to_pydatetime()
    # IANA time zone format: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#ZURICH
    zone_info = ZoneInfo("Europe/Zurich")
    return date.replace(tzinfo=zone_info)


def _read_session_metadata() -> pd.DataFrame:
    # This file was manually verified. Prefer the data in it over the one in the NIX file.
    trial_data_path = join(_get_in_dir(), "metadata", "participants.csv")
    df = pd.read_csv(
        trial_data_path,
        usecols=[
            "Participant",
            "Session",
            "Age",
            "Sex",
            "Pathology",
            "sEEG electrodes analysed",
            "Electrodes in seizure onset zone (SOZ)",
            "Handedness",
            "Date",
            "Session Start Time",
            "Dataset"
        ],
        dtype={
            "Participant": np.int32,
            "Session": np.int32,
            "Age": np.int32,
            "Sex": str,
            "Pathology": str,
            "sEEG electrodes analysed": str,
            "Electrodes in seizure onset zone (SOZ)": str,
            "Handedness": str,
            "Date": str,
            "Session Start Time": str,
            "Dataset": str,
        },
    )
    df["Date"] = df["Date"] + " " + df["Session Start Time"]
    df["Date"] = df["Date"].apply(lambda date: datetime.strptime(date, "%y%m%d %H:%M"))
    df.drop(columns=["Session Start Time"], inplace=True)
    return df


def create_nwb_io_for_reading(ctx: NwbContext) -> NWBHDF5IO:
    filename = _get_nwb_filename(ctx.subject, ctx.session)
    return NWBHDF5IO(join(_get_out_dir(), "converted", ctx.project, filename), mode="r", load_namespaces=True)


def write_nwb(ctx: SessionContext):
    filename = _get_nwb_filename(ctx.subject, ctx.session)
    with NWBHDF5IO(join(_get_out_dir(), "converted", ctx.project, filename), "w") as io:
        io.write(ctx.nwb)


def _get_nwb_filename(subject: int, session: int) -> str:
    return f"subject{subject:02}_session{session:02}.nwb"


def standardize_sex(raw: str) -> str:
    male = ["male", "m", "männlich", "maennlich", "mannlich", "männchen", "mannchen"]
    female = ["female", "f", "weiblich", "weibchen"]
    sex = raw.lower()
    return "M" if sex in male else "F" if sex in female else "O"
