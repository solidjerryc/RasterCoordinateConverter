# RasterConvert
将有火星坐标加偏的tif数据集转换为无偏

##

根据 [sshuair/coord-convert](https://github.com/sshuair/coord-convert) 开发

本工具可以对小范围内的的栅格数据集纠偏，例如在水经注上下载的有偏栅格底图。仅仅适用于小范围的区域，大范围的区域误差会很大。

需要安装gdal与ogr。

可以直接命令行调用，格式如下：

    python trans.py [原始文件路径]

或者

    python trans.py [原始文件路径] [输出文件路径]

只输入原始文件路径的情况下会在同一目录生成一个带_new 的数据集。
