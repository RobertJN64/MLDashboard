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
        self.axes = []
        self.text = []
        self.imgs = []


    def createImages(self, rawdata):
        images = []
        for image in rawdata:
            image = image.reshape(self.config['width'],self.config['height'])
            img = Image.fromarray(image * 255)
            images.append(img.convert(self.config['conversion']))
        return images

    def updateImageGrid(self, imgs = None, text = None):
        """Will not rerender unless it is necessary."""
        if imgs is None:
            imgs = self.imgs
        if text is None:
            text = self.text

        if len(imgs) > 0:
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
                    if counter >= len(self.axes):
                        self.axes.append(self.displayImage(xpos + imgwidth / 6, ypos + imgheight / 8, imgwidth / 1.5,
                                                           imgheight / 1.5, imgs[counter], text[counter]))
                    else:
                        b2 = self.axes[counter].get_position()
                        if abs(b2.x0 - (xpos + imgwidth / 6)) > 0.001 and abs(b2.y0 - (ypos + imgheight / 8)) > 0.001:
                            self.axes[counter].set_position(
                                (xpos + imgwidth / 6, ypos + imgheight / 8, imgwidth / 1.5, imgheight / 1.5))

                        if text[counter] != self.text[counter]:
                            self.axes[counter].set_title(text[counter])
                        if list(imgs[counter].getdata()) != list(self.imgs[counter].getdata()):
                            self.axes[counter].imshow(imgs[counter], cmap=self.config['cmap'])

                    counter += 1
                    xpos += imgwidth
                ypos += imgheight

        self.imgs = imgs
        self.text = text


    def displayImage(self, x, y, width, height, img, text, textcolor='black'): #TODO - handle text color
        #imshow will only shrink and resize axes
        fig = self.ax.get_figure()
        ax = fig.add_axes((x, y, width, height))
        ax.imshow(img, cmap=self.config['cmap'])
        ax.tick_params(axis='both', which='both', bottom=False, top=False,
                                labelbottom=False, right=False, left=False, labelleft=False)
        ax.set_title(text, color=textcolor)
        return ax