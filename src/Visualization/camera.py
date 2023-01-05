class Camera:
    """Represent view of the game world
    width: width and height of view (in grid cells)
    """
    def __init__(self, x: int = 50, y: int = 50, max_width: int = 100):
        self.x = x
        self.y = y
        self.max_width = max(max_width, 20)
        self.allowed_width = [10, 16, 20, 32, 50, 80, 100, 160, 200, 400]  # dividers of 400
        if self.max_width not in self.allowed_width:
            import warnings
            warnings.warn("Camera maxSize should be one of the following: " + str(self.allowed_width))
        self.size = 2
        self.width = self.allowed_width[self.size]

    def move(self, x: int, y: int):
        """Move camera on grid"""
        self.x += x * self.width // 20
        self.y += y * self.width // 20
        self._normalize_position()

    def zoom_in(self):
        self.size = min(self.size + 1, len(self.allowed_width) - 1)
        self.width = self.allowed_width[self.size]
        self._normalize_position()

    def zoom_out(self):
        self.size = max(self.size - 1, 0)
        self.width = self.allowed_width[self.size]
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

