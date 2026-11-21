
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, model_validator

from gen.generator import SignalGenerator
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="BANC_TEST - GEN API")

BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = BASE_DIR / "web"

app.mount(
    "/static",
    StaticFiles(directory=WEB_DIR),
    name="static"
)

@app.get("/")
def home():
    return FileResponse(WEB_DIR / "index.html")


generator = SignalGenerator()


class ChannelConfig(BaseModel):

    waveform: str
    frequency: float = Field(ge=0)
    amplitude: float = Field(ge=0)
    offset: float
    phase: float
    enabled: bool

    @model_validator(mode="after")
    def validate_signal(self):

        if self.waveform not in {
            "sine", "square", "triangle", "dc"
        }:
            raise ValueError("Forme de signal inconnue")

        if self.waveform != "dc" and self.frequency == 0:
            raise ValueError(
                "La fréquence doit être positive"
            )

        return self


@app.get("/channels/{channel}")
def read_channel(channel: int):

    try:
        return generator.get_channel(channel)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@app.post("/channels/{channel}")
def configure_channel(
    channel: int,
    config: ChannelConfig
):

    try:
        generator.configure_channel(
            channel,
            config.model_dump()
        )

        return {
            "status": "ok",
            "channel": channel,
            "configuration": generator.get_channel(channel)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
