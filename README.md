# RasterToVector
用python将tif转换为shapefile，使用libtiff，pyshp，numpy

原本的代码是c++写的，用python重写了一下，由于对python不是很熟悉，遇到了不少问题。

1、python的类
   class py:
     a
     //这个区域的变量是所有的实例共用的
     
     def __init__(self):
        self.b
        //这里的变量是实例独有的
     
     def function(self):
        self.a
        self.b
        //很奇怪，两种变量都是这么调用的，那就是不能重载了
     
 2、list
 
    a=[1,2,3]
    b=a
    b.pop()
    >>>a=[1,2]
    
    也就是说，(list)b=(list)a这个=是引用的意思，二者会同时改变。如果不想同时改变，需要：
    
    b=copy.deepcopy(a)

3、pyshp  
   
   ·用pyshp写入shapefile时，需要手动闭合多边形，如果不做这一步，虽然也可以输出的矢量图，但放大的时候最后一条边会丢失  
   ·另外shp的坐标原点在左下角，所以会有上下颠倒的事情发生
