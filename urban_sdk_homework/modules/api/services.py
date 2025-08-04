from pathlib import Path
from typing import Optional

import uvicorn
from dotenv import load_dotenv

from urban_sdk_homework.core.services import Service
from urban_sdk_homework.modules.api.settings import ApiSettings


class ApiService(Service):
    """Web API service."""

    def start(
        self,
        envfile: Optional[Path] = None,
        reload: Optional[bool] = None,
    ):
        """Start the web API service."""
        # Resolve the environment file location.
        envfile_ = Path(envfile or Path.cwd() / ".env").expanduser().resolve()
        # Update the environment.
        load_dotenv(dotenv_path=envfile_, override=True)
        # Create the settings object with the new environment values.
        settings = ApiSettings()
        uvicorn.run(
            app=settings.entry_point,
            host=str(settings.bind),
            port=settings.port,
            workers=settings.workers,
            limit_concurrency=settings.limit_concurrency,
            limit_max_requests=settings.limit_max_requests,
            reload=(settings.reload if reload is None else reload),
            env_file=envfile_,
        )
