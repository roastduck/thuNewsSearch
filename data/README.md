data
=========

本文件夹存放爬取网页的中间结果，其中`pages.json`是爬取的所有网页，大小321MB、`inverted.json`是倒排表，大小108MB。

由于文件过大，故提供两个节取文件：`pages\_sample.json`和`inverted\_sample.json`作演示用。其中字符串为utf8转义字符串，若不方便阅读，可在python中import `src/data.json`，使用`data.load("pages\_sample"或"inverted\_sample")`读取查看。
