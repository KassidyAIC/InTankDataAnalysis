from dataclasses import dataclass
from typing import Dict, List
import csv
import re
from pathlib import Path


@dataclass(frozen=True)
class TankConfig:
    number: int
    name: str
    ballast_group: int


class AppConfig:
    def __init__(self, tanks: List[TankConfig]):
        if not tanks:
            raise ValueError("Config contains no tanks")
        self.tanks = tanks
        self._by_number: Dict[int, TankConfig] = {t.number: t for t in tanks}

    def tank_by_number(self) -> Dict[int, TankConfig]:
        return self._by_number

    def tank_name_map(self) -> Dict[int, str]:
        return {n: t.name for n, t in self._by_number.items()}

    def ballast_group_map(self) -> Dict[int, int]:
        return {n: t.ballast_group for n, t in self._by_number.items()}


_TANK_RE = re.compile(r"tank\s*(\d+)", re.IGNORECASE)


def load_config(path: str) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    tanks: List[TankConfig] = []
    in_tanks = False

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue

            first = (row[0] or "").strip()
            if first.startswith("Tanks:"):
                in_tanks = True
                continue

            if not in_tanks:
                continue

            # Expected:
            # [ "", "Tank 1:", "1", "FWD WBT (P)", ... ]
            if len(row) < 4:
                continue

            tank_cell = (row[1] or "").strip()
            m = _TANK_RE.search(tank_cell)
            if not m:
                continue

            number = int(m.group(1))

            try:
                ballast_group = int(str(row[2]).strip())
            except ValueError:
                continue

            name = str(row[3]).strip()
            if not name:
                continue

            tanks.append(
                TankConfig(
                    number=number,
                    ballast_group=ballast_group,
                    name=name,
                )
            )

    if not tanks:
        raise ValueError("No tanks found — invalid or unsupported config file")

    tanks.sort(key=lambda t: t.number)
    return AppConfig(tanks)