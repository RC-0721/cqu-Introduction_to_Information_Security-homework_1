# 信息安全导论 作业1
## 1. 作业任务
根据"信息安全导论"课程第5次课讲述的S-DES算法，使用你们自己最擅长的程序语言(C++/QT或Java+Swing、Python+QT等)来编程实现加、解密程序。
## 2. 标准设定
### 2.1 分组长度
8-bit
### 2.2 密钥长度
10-bit
### 2.3 算法描述
- 加密算法：C=IP<sup>-1</sup>(f<sub>k<sub>2</sub></sub>(SW(f<sub>k<sub>1</sub></sub>(IP(P)))))
- 解密算法：P=IP<sup>-1</sup>(f<sub>k<sub>1</sub></sub>(SW(f<sub>k<sub>2</sub></sub>(IP(C)))))
- 密钥扩展：k<sub>i</sub>=P<sub>8</sub>(Shift<sup>i</sup>(P<sub>10</sub>(K))),  (i=1,2)
### 2.4 转换装置设定
- 密钥扩展置: 
  - P<sub>10</sub>=(3,5,2,7,4,10,1,9,8,6)
    - <img width="679" height="207" alt="image" src="https://github.com/user-attachments/assets/368d042c-8884-471f-bfea-5434e790c25b" />
  - P<sub>8</sub>=(6,3,7,4,8,5,10,9)
    - <img width="681" height="194" alt="image (1)" src="https://github.com/user-attachments/assets/bedc5fd3-23bd-4f61-95c3-10fb3e93c184" />
  - Left_Shift<sup>1</sup>=(2,3,4,5,1)
  - Left_Shift<sup>2</sup>=(3,4,5,1,2)
- 初始置换盒:
  - IP=(2,6,3,1,4,8,5,7)
    - <img width="691" height="207" alt="image (2)" src="https://github.com/user-attachments/assets/5c751a31-e55b-43f4-b3be-664094a99c50" />
- 最终置换盒:
  - IP<sup>-1</sup>=(4,1,3,5,7,2,8,6)
    - <img width="691" height="208" alt="image (7)" src="https://github.com/user-attachments/assets/1295080a-1839-49e7-ac07-22e7747302e9" />
- 轮函数F:
  - EPBox=(4,1,2,3,2,3,4,1)
    - <img width="637" height="308" alt="image (3)" src="https://github.com/user-attachments/assets/aac70985-f45a-4478-bfb8-2d8853f059b4" />
  - SBox<sub>1</sub>=[(1,0,3,2);(3,2,1,0);(0,2,1,3);(3,1,0,2)]
    - <img width="298" height="230" alt="image (4)" src="https://github.com/user-attachments/assets/6069906c-6b6c-4503-aa7f-bbadc10e1a63" />
  - SBox<sub>2</sub>=[(0,1,2,3);(2,3,1,0);(3,0,1,2);(2,1,0,3)]
    - <img width="297" height="230" alt="image (5)" src="https://github.com/user-attachments/assets/c8e5783a-2424-44cb-9ed7-21260e9806c2" />
  - SPBox=(2,4,3,1)
    - <img width="535" height="260" alt="image (6)" src="https://github.com/user-attachments/assets/6f930f35-dfb5-46ed-8a1c-ef28275a066b" />

## 3. 编程和测试要求
- 第1关：基本测试。根据S-DES算法编写和调试程序，提供GUI解密支持用户交互。输入可以是8bit的数据和10bit的密钥，输出是8bit的密文。
- 第2关：交叉测试考虑到是算法标准，所有人在编写程序的时候需要使用相同算法流程和转换单元(P-Box、S-Box等)，以保证算法和程序在异构的系统或平台上都可以正常运行。设有A和B两组位同学(选择相同的密钥K)；则A、B组同学编写的程序对明文P进行加密得到相同的密文C；或者B组同学接收到A组程序加密的密文C，使用B组程序进行解密可得到与A相同的P。
- 第3关：扩展功能考虑到向实用性扩展，加密算法的数据输入可以是ASII编码字符串(分组为1 Byte)，对应地输出也可以是ACII字符串(很可能是乱码)。
- 第4关：暴力破解假设你找到了使用相同密钥的明、密文对(一个或多个)，请尝试使用暴力破解的方法找到正确的密钥Key。在编写程序时，你也可以考虑使用多线程的方式提升破解的效率。请设定时间戳，用视频或动图展示你在多长时间内完成了暴力破解。
- 第5关：封闭测试根据第4关的结果，进一步分析，对于你随机选择的一个明密文对，是不是有不止一个密钥Key？进一步扩展，对应明文空间任意给定的明文分组P<sub>n</sub>，是否会出现选择不同的密钥K<sub>i</sub> != K<sub>j</sub>加密得到相同密文C<sub>n</sub>的情况？
## 4. 代码规范
- 变量命名规范尽量使用有意义的名字来为变量、函数和类命名，描述其用途。建议使用驼峰命名法（CamelCase）或下划线分隔命名法（snake_case）。使用描述性的名字，避免使用单个字符的变量名，除非是临时变量。
- 代码注释请使用各编程语言对应的符号进行单行或多行注释，在注释中需使用清晰、有意义的语言，用于解释单行代码或代码块的功能、算法或特定说明（如代码的创新）。同时避免过多的注释，只需复制相对复杂或不明显的部分。
- 函数式编程请使用函数式编程，将代码模块化，每个小模块负责特定的功能实现。对于重复的代码，可以使用函数或类来实现代码的复用，推荐使用标准库和第三方库辅助算法的实现。
## 5. 用户手册
[https://github.com/RC-0721/cqu-Introduction_to_Information_Security-homework_1/blob/main/User_manual.md]

