from __future__ import annotations
from typing import Optional
from pydantic import AliasChoices, BaseModel, Field
import configparser
import os
from pathlib import Path

class FossyConfig(BaseModel):
    url: str
    uname: Optional[str] = None
    pwd: Optional[str] = None
    access: Optional[str] = None
    bearer_token: Optional[str] = None
    token_expire: Optional[str] = None
    # Canonical spelling. The historical typo "token_valdity_days" is still
    # accepted from ini files and env vars, and is no longer written back.
    token_validity_days: int = Field(
        365,
        validation_alias=AliasChoices("token_validity_days", "token_valdity_days"),
    )
    reports_location: str = "reports/"
    group_name: Optional[str] = None
    verify: bool = False

    @classmethod
    def from_ini(cls, path: str, section: str = "test") -> FossyConfig:
        config = configparser.ConfigParser()
        if not Path(path).exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        config.read(path)
        if section not in config:
            raise KeyError(f"Section {section} not found in config file {path}")

        data = dict(config[section])
        # Handle specific types from ini
        for key in ("token_validity_days", "token_valdity_days"):
            if key in data:
                data[key] = int(data[key])
        if "verify" in data:
            data["verify"] = data["verify"].lower() == "true"

        return cls(**data)

    @classmethod
    def from_env(cls) -> FossyConfig:
        return cls(
            url=os.environ["FOSSY_URL"],
            uname=os.environ.get("FOSSY_UNAME"),
            pwd=os.environ.get("FOSSY_PWD"),
            access=os.environ.get("FOSSY_ACCESS"),
            bearer_token=os.environ.get("FOSSY_BEARER_TOKEN"),
            token_expire=os.environ.get("FOSSY_TOKEN_EXPIRE"),
            reports_location=os.environ.get("FOSSY_REPORTS_LOCATION", "reports/"),
            group_name=os.environ.get("FOSSY_GROUP_NAME"),
            verify=os.environ.get("FOSSY_VERIFY", "false").lower() == "true",
            token_validity_days=int(
                os.environ.get("FOSSY_TOKEN_VALIDITY_DAYS")
                or os.environ.get("FOSSY_TOKEN_VALDITY_DAYS")
                or 365
            ),
        )

    def save_to_ini(self, path: str, section: str = "test"):
        config = configparser.ConfigParser()
        if Path(path).exists():
            config.read(path)

        if section not in config:
            config.add_section(section)

        # Drop the historical typo so a rewritten file carries one spelling.
        if config.has_option(section, "token_valdity_days"):
            config.remove_option(section, "token_valdity_days")

        for field, value in self.model_dump().items():
            config.set(section, field, str(value))

        with open(path, "w") as f:
            config.write(f)
