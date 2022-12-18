class Camera:
    """Represent view of the game world
    width: width and height of view (in grid cells)
    """
    def __init__(self, x: int = 50, y: int = 50, max_width: int = 100, width: int = 20):
        self.x = x
        self.y = y
        self.max_width = max_width
        self.width = width

    def move(self, x: int, y: int):
        """Move camera on grid"""
        self.x += x
        self.y += y
        self._normalize_position()

    def zoom_in(self):
        self.width /= 1.3
        self.width = int(self.width)
        self._normalize_position()

    def zoom_out(self):
        self.width *= 1.3
        self.width = int(self.width)
        self._normalize_position()

    def _normalize_position(self):
        if self.width < 10:
            self.width = 10
        if self.width > self.max_width:
            self.width = self.max_width
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x + self.width > self.max_width:
            self.x = self.max_width - self.width
        if self.y + self.width > self.max_width:
            self.y = self.max_width - self.width

    # translate coordinates on screen to grid coordinates (for mouse input)
    def screen_to_grid_point(self, x: int, y: int, cell_size: int):
        return self.x + x // cell_size,  self.y + y // cell_size

    # can return value outside of screen if argument is invisible
    def grid_to_screen_point(self, x: int, y: int, cell_size: int):
        return (x - self.x) * cell_size, (y - self.y) * cell_size

