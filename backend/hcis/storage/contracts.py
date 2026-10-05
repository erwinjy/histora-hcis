from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass

@dataclass(frozen=True)
class WorkspacePaths:
    root: str
    database: str
    source_vault: str
    derived: str
    cache: str
    logs: str
    backups: str

class WorkspaceManager(Protocol):
    def create(self, root: str) -> WorkspacePaths: ...
    def locate(self, root: str) -> WorkspacePaths: ...
    def verify(self) -> dict: ...
    def relocate_database(self, target: str) -> dict: ...
    def relocate_source_vault(self, target: str) -> dict: ...
