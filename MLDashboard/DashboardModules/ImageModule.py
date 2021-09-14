from MLDashboard.DashboardModules.Module import Module
from PIL import Image

class ImageModule(Module):
    """Base class for modules that rely on rendering images"""
    def __init__(self, ax, config, title):
        super().__init__(ax, config, title, noticks=True, reqkeys=["width", "height", "rows", "cols"])
        if 'conversion' not in self.config:
            self.config['conversion'] = 'L' #grayscale
        if 'cmap' not in self.config:
            self.config['cmap'] = 'gray'
        self.aximages = []

    def createImages(self, rawdata):
        images = []
        for image in rawdata:
            image = image.reshape(self.config['width'],self.config['height'])
            img = Image.fromarray(image * 255)
            images.append(img.convert(self.config['conversion']))
        return images

    def displayImageGrid(self, imgs, text):
        #get bounding box of main axes
        b = self.ax.get_position()
        x = b.x0
        y = b.y0
        width = b.width
        height = b.height

        rows = self.config['rows']
        cols = self.config['cols']

        imgwidth = (width / cols)
        imgheight = (height / rows)

        ypos = y
        for row in range(0, rows):
            xpos = x
            for col in range(0, cols):
                self.aximages.append(self.displayImage(xpos + imgwidth/6, ypos + imgheight/8, imgwidth/1.5, imgheight/1.5,
                                                       imgs[col + row*cols], text[col + row*cols]))
                xpos += imgwidth
            ypos += imgheight

    def displayImage(self, x, y, width, height, img, text, textcolor='black'):
        #imshow will only shrink and resize axes
        fig = self.ax.get_figure()
        ax = fig.add_axes((x, y, width, height))
        ax.imshow(img, cmap=self.config['cmap'])
        ax.tick_params(axis='both', which='both', bottom=False, top=False,
                                labelbottom=False, right=False, left=False, labelleft=False)
        ax.set_title(text, color=textcolor)
        return ax

    def recalcImageBoxes(self):
        b = self.ax.get_position()
        x = b.x0
        y = b.y0
        width = b.width
        height = b.height

        rows = self.config['rows']
        cols = self.config['cols']

        imgwidth = (width / cols)
        imgheight = (height / rows)

        counter = 0
        ypos = y
        for row in range(0, rows):
            xpos = x
            for col in range(0, cols):
                self.aximages[counter].set_position((xpos + imgwidth/6, ypos + imgheight/8, imgwidth/1.5, imgheight/1.5))
                counter += 1
                xpos += imgwidth
            ypos += imgheight

