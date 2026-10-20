# ANTLR in Python Interpreter

## 配置教程

### 配置 Antlr C++ 运行环境

Python 解释器采用 Antlr 作为前端语法分析器，其中核心代码编译时间较长，因此我们提前编译好了 Antlr 的运行环境，这样你的程序在编译时就不需要再编译 Antlr 的运行环境了。

为了在你自己的电脑上也使用 Antlr 运行环境，你需要将 Antlr 编译好的运行环境安装到你的电脑上。

将 `antlr4-runtime_4.13.1_amd64.deb` 文件下载到 WSL 中，打开文件所在目录，执行以下命令安装：

```shell
sudo apt install ./antlr4-runtime_4.13.1_amd64.deb
```

在这个包中，含有 Antlr 4.13.1 的动态链接库、静态链接库以及头文件，如果不装这个包，
将导致你的程序在编译时找不到 Antlr 的头文件和动态链接库，从而编译失败。

使用 Archlinux 的同学可以直接使用以下命令安装运行环境:
```shell
pacman -S antlr4-runtime
```

如有在其他环境下编程的同学（比如 Windows、Mac 和除 Debian,Arch 之外的 Linux 系统），请联系助教。

### 生成语法树

#### 使用ANTLR内置的可视化工具

请确保ANTLR4的jar包已经被正常安装至 `/usr/local/lib`，如果没有，先运行

```bash
sudo wget https://www.antlr.org/download/antlr-4.13.1-complete.jar --directory-prefix=/usr/local/lib
```

进行安装。然后进入 `./resources` 目录：

```bash
cd resources
```

然后，运行`visualize.bash`。格式为：

```bash
bash visualize.bash [Parser Rule] -gui
```

其中`[Parser Rule]`表示你希望生成的语法树的根节点的类型，例如：如果你的输入为一整个程序，则参数为`file_input`；如果你希望输入函数定义，则参数为`funcdef`等，具体可用的Parser Rule类型即为Python3Parser.g4中包含的语法规则。

为了确保java生成的GUI界面可以被正常展示，请确保你的操作系统是Win11/最新版Win10/Linux系统，否则你的windows有概率无法正常显示语法树（只有高版本Windows才配了转接WSL图像的库和支持）。

生成可视化语法树基于的文件是`Python3Demo.g4`，除此之外，这个文件没有特殊的作用（即与Coding没有直接关联），因此你不必理解其中的内容。如果要对其进行修改，请确保你理解其中的内容。

## ANTLR 是什么

ANTLR（全名：ANother Tool for Language Recognition）是基于 LL(\*)算法实现的语法解析器生成器（parser generator），用 Java 语言编写，使用自上而下（top-down）的递归下降 LL 剖析器方法。

ANTLR 可以将输入的代码转化成与之对应的**树形结构**，即语法树，以便后续程序操作。按照上面的配置操作，即可得到一份 `Python` 代码对应的语法树。
