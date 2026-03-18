from __future__ import annotations

from typing import List

from core.models import Initiative, RoadmapItem


class RoadmapService:
    def initiatives_to_roadmap(self, initiatives: List[Initiative]) -> List[RoadmapItem]:
        items: List[RoadmapItem] = []
        for idx, initiative in enumerate(initiatives, start=1):
            items.append(
                RoadmapItem(
                    id=f"R-{idx:03d}",
                    initiative_id=initiative.id,
                    time_horizon=initiative.time_horizon or "6_12_months",
                    stream=initiative.stream or "trasversale",
                    priority_class=initiative.priority_class or "Foundational",
                    owner=initiative.owner,
                    dependencies=initiative.dependencies,
                    success_kpis=initiative.success_kpis,
                    status="proposed",
                    notes=initiative.notes,
                )
            )
        return items
