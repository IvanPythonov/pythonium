from pythonium.engine.entity.components.base import Component


class GravityComponent(Component):
    """Gravity."""

    def tick(self, current_tick: int) -> None:
        if self.entity.on_ground:
            return

        self.entity.velocity_y -= 0.04

        self.entity.velocity_y *= 0.98
        self.entity.velocity_x *= 0.98
        self.entity.velocity_z *= 0.98
