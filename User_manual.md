# S-DES 加密工具用户指南

## 1. 软件概述

S-DES（Simplified Data Encryption Standard）简化数据加密标准工具是一个用于教学和实验的加密软件。它实现了10位密钥的简化DES算法，提供了图形化界面进行加密、解密和密码分析操作。

## 2. 系统要求

- **操作系统**: Windows 10/11
- **Python版本**: 3.6 或更高版本
- **必要库**: tkinter

## 3. 安装步骤

### 3.1 基础安装
1. 确保已安装Python 3.6+
2. 下载`作业1.py`文件
3. 在命令行运行：`python 作业1.py`

### 3.2 验证安装
启动程序后，如果看到图形界面，说明安装成功。
  - <img width="444" height="408" alt="image" src="https://github.com/user-attachments/assets/f2a01c60-3f73-4591-92b0-bc12a996c61c" />
## 4. 功能使用指南

### 4.1 基本加解密功能

**用途**: 对8位二进制数据进行加解密

**操作步骤**:
1. 选择"基本加解密"标签页
2. 在"明文"输入框输入8位二进制数（如：`01110010`）
3. 在"密钥"输入框输入10位二进制密钥（如：`1010000010`）
4. 点击"加密"按钮查看结果
5. 结果区域显示密文和生成的子密钥K1、K2
  - 加密
    - <img width="451" height="412" alt="image" src="https://github.com/user-attachments/assets/f99e2a14-626d-4703-b1f2-c3f88959b180" />
  - 解密
    - <img width="448" height="419" alt="image" src="https://github.com/user-attachments/assets/7717f8b8-f63a-4a5c-a295-22fbf7c223f8" />

### 4.2 文本加解密功能

**用途**: 对文本字符串进行加解密

**操作步骤**:
1. 选择"文本加解密"标签页
2. 在文本区域输入要加密的文本
3. 输入10位二进制密钥
4. 点击"加密文本"按钮
5. 结果区域显示加密后的文本和十六进制表示
- 加密
  - <img width="395" height="445" alt="image" src="https://github.com/user-attachments/assets/5fdb7cd2-a689-4c19-a6ef-90906c08d466" />
- 解密
  - <img width="395" height="441" alt="image" src="https://github.com/user-attachments/assets/0cde62dd-84d0-4f10-9c53-46ba86f02671" />

**注意事项**:
- 加密结果可能包含不可见字符
- 解密时需要完全相同的加密文本

### 4.3 暴力破解功能

**用途**: 通过已知明密文对破解密钥

**操作步骤**:
1. 选择"暴力破解"标签页
2. 输入已知的8位二进制明文
3. 输入对应的8位二进制密文
4. 点击"开始暴力破解"按钮
5. 观察进度条，等待破解完成
6. 查看找到的可能密钥列表
- <img width="341" height="346" alt="image" src="https://github.com/user-attachments/assets/bd122899-c43b-4ca9-92b7-19d790749ef8" />

### 4.4 封闭测试分析

**用途**: 学习S-DES算法原理和安全性分析

**内容包含**:
- 密钥空间分析
- 多密钥情况说明
- 算法安全性评估
- 碰撞分析
- <img width="527" height="385" alt="image" src="https://github.com/user-attachments/assets/1fb2bde6-a81c-4b4e-bf08-5e88a7aff7a3" />

## 5. 输入格式要求

### 5.1 二进制输入
- **明文/密文**: 必须为8位二进制数，只包含0和1
- **密钥**: 必须为10位二进制数，只包含0和1

### 5.2 文本输入
- 支持任意可打印字符
- 自动处理编码转换

## 6. 常见问题解答

### Q1: 为什么加密后的文本显示乱码？
A: 这是正常现象，加密后的数据以二进制形式存储，可能对应不可见字符。

### Q2: 暴力破解需要多长时间？
A: 最多尝试1024个密钥，通常几秒内完成。

### Q3: 为什么有时会找到多个密钥？
A: 这是S-DES算法的特性，不同密钥可能产生相同的加密结果。
