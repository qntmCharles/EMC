from __future__ import division #Bloody python2

class author:
    def __init__(self,name='',data={}):
        self.name = name
        self.Data = data
        self.data = data.values()
        self.years = data.keys()


