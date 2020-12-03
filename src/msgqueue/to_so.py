# coding:utf-8
# 导入模块
import Cython.Build

# 传入要编译成pyd的py文件
ext = Cython.Build.cythonize("consume_business.py")

# 下面还要导入另一个模块
import distutils.core

# 调用setup方法
distutils.core.setup(ext_modules=ext)