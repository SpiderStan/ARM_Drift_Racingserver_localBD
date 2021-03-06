
"""
Module defining the driftapi core and enum classes.
Note: for a complete server implementation, you probably want to also define some additional classes.

"""
from enum import Enum
from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ValidationError, Field, validator

class game_mode(str, Enum):
    RACE = "RACE"
    LAP_RACE = "LAP_RACE"
    TIME_RACE = "TIME_RACE"
    ELIMINATION = "ELIMINATION"
    GYMKHANA = "GYMKHANA"
    GYMKHANA_TRAINING = "GYMKHANA_TRAINING"

class track_condition(str, Enum):
    drift_asphalt = "drift_asphalt"
    drift_asphalt_wet = "drift_asphalt_wet"
    drift_dirt = "drift_dirt"
    drift_ice = "drift_ice"
    drift_sand = "drift_sand"

class track_bundle(str, Enum):
    none = "none"
    rally = "rally"
    rally_cross = "rally_cross"

class wheels(str, Enum):
    normal = "normal"
    spikes = "spikes"
    gravel_tires = "gravel_tires"

class setup_mode(str, Enum):
    RACE = "RACE"
    DRIFT = "DRIFT"

class bonus_target(str, Enum):
    SPEED = "SPEED"
    ANGLE = "ANGLE"
    THREESIXTY = "360"
    ONEEIGHTY = "180"

class gymkhana_training_targets(str, Enum):
    ANGLE_ONEEIGHTY_SPEED_THREESIXTY = "ANGLE -> 180° -> SPEED -> 360°"
    ANGLE_ONEEIGHTY_THREESIXTY_SPEED = "ANGLE -> 180° -> 360° -> SPEED"
    ANGLE_SPEED_ONEEIGHTY_THREESIXTY = "ANGLE -> SPEED -> 180° -> 360°"
    ANGLE_SPEED_THREESIXTY_ONEEIGHTY = "ANGLE -> SPEED -> 360° -> 180°"
    ANGLE_THREESIXTY_SPEED_ONEEIGHTY = "ANGLE -> 360° -> SPEED -> 180°"
    ANGLE_THREESIXTY_ONEEIGHTY_SPEED = "ANGLE -> 360° -> 180° -> SPEED"
    SPEED_ONEEIGHTY_ANGLE_THREESIXTY = "SPEED -> 180° -> ANGLE -> 360°"
    SPEED_ONEEIGHTY_THREESIXTY_ANGLE = "SPEED -> 180° -> 360° -> ANGLE"
    SPEED_ANGLE_ONEEIGHTY_THREESIXTY = "SPEED -> ANGLE -> 180° -> 360°"
    SPEED_ANGLE_THREESIXTY_ONEEIGHTY = "SPEED -> ANGLE -> 360° -> 180°"
    SPEED_THREESIXTY_ANGLE_ONEEIGHTY = "SPEED -> 360° -> ANGLE -> 180°"
    SPEED_THREESIXTY_ONEEIGHTY_ANGLE = "SPEED -> 360° -> 180° -> ANGLE"
    ONEEIGHTY_ANGLE_THREESIXTY_SPEED = "180° -> ANGLE -> 360° -> SPEED"
    ONEEIGHTY_ANGLE_SPEED_THREESIXTY = "180° -> ANGLE -> SPEED -> 360°"
    ONEEIGHTY_THREESIXTY_ANGLE_SPEED = "180° -> 360° -> ANGLE -> SPEED"
    ONEEIGHTY_THREESIXTY_SPEED_ANGLE = "180° -> 360° -> SPEED -> ANGLE"
    ONEEIGHTY_SPEED_ANGLE_THREESIXTY = "180° -> SPEED -> ANGLE -> 360°"
    ONEEIGHTY_SPEED_THREESIXTY_ANGLE = "180° -> SPEED -> 360° -> ANGLE"
    THREESIXTY_ANGLE_ONEEIGHTY_SPEED = "360° -> ANGLE -> 180° -> SPEED"
    THREESIXTY_ANGLE_SPEED_ONEEIGHTY = "360° -> ANGLE -> SPEED -> 180°"
    THREESIXTY_ONEEIGHTY_ANGLE_SPEED = "360° -> 180° -> ANGLE -> SPEED"
    THREESIXTY_ONEEIGHTY_SPEED_ANGLE = "360° -> 180° -> SPEED -> ANGLE"
    THREESIXTY_SPEED_ONEEIGHTY_ANGLE = "360° -> SPEED -> 180° -> ANGLE"
    THREESIXTY_SPEED_ANGLE_ONEEIGHTY = "360° -> SPEED -> ANGLE -> 180°"

class target_code(int, Enum):
    start_finish = 0 #Gymkhana, Race, Rally, Rally Cross
    speed_drift = 4 #Gymkhana
    drift_asphalt = 4 #Rally, Rally Cross
    angle_drift = 5 #Gymkhana
    drift_asphalt_wet = 5 #Rally, Rally Cross
    oneeighty = 6 #Gymkhana
    drift_dirt = 6 # Rally, Rally Cross
    threesixty = 7 #Gymkhana
    drift_ice = 7 # Rally
    drift_sand = 7 # Rally Cross
    
class PingResponse(BaseModel):
    status:bool = Field(None, example=True)
    start_time:Optional[datetime]
    lap_count:Optional[int] = Field(None, title="number of rounds (for the race mode)")
    track_condition:Optional[ track_condition]
    track_bundle:Optional[ track_bundle]
    wheels:Optional[ wheels]
    setup_mode:Optional[ setup_mode]

class EnterData(BaseModel):
    game_mode: game_mode
    start_time:Optional[datetime]
    lap_count: int = Field(None, title="number of rounds (for the race mode)")
    track_condition: track_condition
    track_bundle: track_bundle
    wheels: wheels
    setup_mode: setup_mode
    engine_type: str = Field(None, title="The id of the motor type. No ENUM because this might get extended. Example: 'DTM', 'V8' etc.", example="V8") 
    tuning_type: str = Field(None, title="The id of the motor setup. No ENUM because this might get extended.", example="BASIC SETUP 550 PS")
    steering_angle: float = Field(None, title="the choosen steering angle as set in the settings menu of the app", example=70.0)
    softsteering:bool = Field(None, title="if softsteering is enabled in the settings menu of the app.", example=False)
    driftassist:bool = Field(None, title="if driftassist is enabled in the settings menu of the app.", example=True)

    @validator('start_time', pre=True)
    def blank_string(value, field):
        if value == "":
            return None
        return value

class StartData(BaseModel):
    signal_time:datetime = Field(None, title="The actual time if the signal lamp shows the green light.")

class TargetData(BaseModel):
    crossing_time: datetime
    target_code: target_code
    false_start: bool = Field(None, title="This is true whenever a false start was detected at the beginning of the race.", example=False)
    driven_distance:float = Field(None, title="The distance driven so far", example=23.0)
    driven_time:float = Field(None, title="Time in seconds the player is driving so far in this race", example=42.0)
    score:int = Field(None, title="Amount of points awarded for this target. Work in progress.", example=100)

class EndData(BaseModel):
    finished_time: datetime
    false_start: bool = Field(None, title="This is true whenever a false start was detected at the beginning of the race.", example=False)
    total_score: int = Field(None, title="The total achieved score at the very end.", example=1000)
    total_driven_distance: float = Field(None, title="The distance driven in this race", example=123.0)
    total_driven_time: float = Field(None, title="Time in seconds the player was driving so far in this race", example=122.0)


class RaceEvent(BaseModel):
    app_version:str = Field(None, title="A string representing the app version the user is running.", example="V.1.14.15_A")
    lobby_id: str = Field(None, title="The id of the lobby that has been opened. This should be the same as the one provided via the uri.", example="Lobby1")
    game_id: str = Field(None, title="The id of the game that has been opened. This should be the same as the one provided via the uri.", example="Race1")
    stage_id: str = Field(None, title="The id of the stage of the game that has been opened.", example="1")
    user_id: UUID = Field(None, title="unique user id", description="unique identifier (for the duration of the current race), can and should be different from the Sturmkind user name for legal and security reasons, for example a hash of the username or a hash of the devices ip address.")
    user_name: str = Field(None, title="the name choosen by the user to be displayed on the scoreboard", description="Can be different from the Sturmkind user name (for legal reasons)", example="PlayerNo1")
    time: datetime = Field(None, title="the exact timestamp down to the precision the sturmkind app uses, so fractions of a second")

class EnterEvent(RaceEvent):
    data:EnterData

class StartEvent(RaceEvent):
    data:StartData

class TargetEvent(RaceEvent):
    data: TargetData

# This event is triggered whenever the user leaves a run (shutting down the motor)
class EndEvent(RaceEvent):
    data:EndData