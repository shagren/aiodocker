from aiohttp import (
    BaseConnector,
    ClientConnectorError,
    NamedPipeConnector,
    UnixConnector,
)


_CUSTOM_ERROR_CODE = 900


class DockerError(Exception):
    def __init__(self, status, data, *args):
        super().__init__(*args)
        self.status = status
        self.message = data["message"]

    def __repr__(self):
        return "DockerError({self.status}, {self.message!r})".format(self=self)

    def __str__(self):
        return "DockerError({self.status}, {self.message!r})".format(self=self)


class DockerContainerError(DockerError):
    def __init__(self, status, data, container_id, *args):
        super().__init__(status, data, *args)
        self.container_id = container_id

    def __repr__(self):
        return (
            "DockerContainerError("
            "{self.status}, {self.message!r}, "
            "{self.container_id!r})"
        ).format(self=self)

    def __str__(self):
        return (
            "DockerContainerError("
            "{self.status}, {self.message!r}, "
            "{self.container_id!r})"
        ).format(self=self)


class DockerConnectionError(DockerError):
    def __init__(
        self, error: ClientConnectorError, connector: BaseConnector, docker_host: str
    ):
        if isinstance(connector, (NamedPipeConnector, UnixConnector)):
            path = connector.path
        else:
            path = docker_host
        message = (
            f"Cannot connect to Docker engine via {path}, {error.os_error.strerror}"
        )
        super().__init__(_CUSTOM_ERROR_CODE, {"message": message})

    def __str__(self):
        return self.message
