from MLDashboard.DashboardModules.Module import Module

class ImageModule(Module):
    """Base class for modules that rely on rendering images"""
    def __init__(self, ax, config, title):
        super().__init__(ax, config, title, noticks=True, reqkeys=["width", "height", "rows", "cols"])

    def displayImage(self, img, subtitle):
        pass #TODO - THIS!