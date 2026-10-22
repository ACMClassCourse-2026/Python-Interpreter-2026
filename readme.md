# 🐍Python Interpreter

## 🧾 目录

- [✨ 简介](#✨简介)
- [📅课程信息](#📅课程信息)
- [🚀快速开始](#🚀快速开始)
  - [环境要求](#环境要求)
  - [编译](#编译)
  - [运行](#运行)
  - [运行公开测试](#运行公开测试)
- [📚 作业说明](#📚作业说明)
  - [⚠️ 实现要求](#⚠️实现要求)
  - [🛎️ 评测方式](#🛎️评测方式)
    - [提交方式](#提交方式)
    - [测试点分布](#测试点分布)
    - [评分方式](#评分方式)
  - [💎Bonus](#💎bonus)
- [📝Guide](#📝guide)
  - [📄 语法](#📄语法)
  - [⚙️ANTLR](#⚙️antlr)
  - [🧪 实现](#🧪实现)
  - [📇 索引](#📇索引)

## ✨简介

本次大作业要求你们实现一个简单的 Python 解释器，接受简化过的 Python 代码，按照控制流执行代码。

> 解释器（Interpreter），是一种计算机程序，能够把解释型语言解释执行。
> 解释器就像一位“中间人”。解释器边解释边执行，因此依赖于解释器的程序运行速度比较缓慢。
> 解释器的好处是它不需要重新编译整个程序，从而减轻了每次程序更新后编译的负担。
> 相对的，编译器一次性将所有源代码编译成二进制文件，执行时无需依赖编译器或其他额外的程序。

## 🚀快速开始

### 环境要求

- Linux 或 WSL（推荐 Ubuntu 22.04 及以上）
- CMake ≥ 3.15.2，支持 C++17 的 g++
- ANTLR4 C++ 运行时 4.13.1
- Python 3（仅在运行公开测试脚本时需要）

在仓库根目录安装 ANTLR4 C++ 运行时：

```bash
sudo apt install ./resources/antlr4-runtime_4.13.1_amd64.deb
```

Arch Linux 可直接使用 `pacman -S antlr4-runtime`；arm64 请安装 `resources/antlr4-runtime_4.13.1-1_arm64.deb`；其他系统的安装方法见 [ANTLR 配置](docs/antlr_guide.md)，或联系助教。

> 开始编码前，请先完成 [`resources/prework.zip`](resources/prework.zip) 中的前置任务，详见[实现要求](#⚠️实现要求)。

### 编译

```bash
cmake -B build
cmake --build build -j
```

生成的可执行文件为 `build/code`。

### 运行

```bash
./build/code < testcases/basic-testcases/test1.in
```

也可以直接运行 `./build/code`，从标准输入读入程序，按 Ctrl+D 结束输入。

### 运行公开测试

```bash
python3 testcases/test.py
```

脚本会自动查找 `build/code`，也可以显式传入可执行文件路径，并通过 `--timeout` 调整单个测试的超时时间：

```bash
python3 testcases/test.py /path/to/code --timeout 60
```

公开测试与测试点编号的对应关系见[测试点分布](#测试点分布)。

## 📚作业说明

### ⚠️实现要求

1. 使用 OOP 实现 Python Interpreter，锻炼 OOP 能力。若不按照要求会在 code review 时扣除一定分数。
2. 作业不低于按数据总的通过比例线性给分。助教会下发部分数据在作业仓库中，还有另一部分数据不会提供。这意味着你需要自己手写测试数据给自己测试，如果你对自己造的数据是否满足要求有疑问，请及时向助教询问。
3. 首先完成 `./resources/prework.zip` 里面的前置任务。前置任务不计分，但要求**必做**。如果不完成前置任务则 Python 解释器将没有分数。

### 🛎️评测方式

使用 `git` 在 OJ 上进行提交。OJ 将根据根目录下的 `CMakeLists.txt` 来构建你的程序。

#### 提交方式

在 OJ 的代码提交页面填写你 Git 仓库的地址。

#### 测试点分布

测试点分布如下：

```text
BigIntegerTest: 1 - 20
Sample: 21 - 34, 67 - 68
AdvancedTest: 35 - 52, 69 - 71
ComplexTest: 53 - 56
CornerTest: 57 - 66, 72, 73
```

仓库中公开的测试点与上表的对应关系如下：

- `testcases/bigint-testcases/BigIntegerTest0`–`BigIntegerTest19` 对应 BigIntegerTest 的 20 个测试点（文件名的顺序与测试点编号不完全一致）。
- `testcases/basic-testcases/test0`–`test15` 依次对应 Sample 中的 21–34、67、68，共 16 个测试点。

其余编号的测试点不随仓库提供。

#### 评分方式

总分 100 分。总体按通过的测试点比例线性给分，各测试分组的权重如下：

| 测试分组 | 测试点 | 分值 |
| --- | --- | --- |
| BigIntegerTest | 1 - 20 | 25 |
| Sample | 21 - 34, 67 - 68 | 25 |
| AdvancedTest | 35 - 52, 69 - 71 | 25 |
| ComplexTest | 53 - 56 | 12.5 |
| CornerTest | 57 - 66, 72, 73 | 12.5 |
| **合计** | 1 - 73 | **100** |

- 前置任务（`resources/prework.zip`）不计分，但**必做**；未完成前置任务时本次作业没有分数。
- 具体计分细则与 Bonus 加分上限以课程通知为准。

### 💎Bonus

1. 修改 `.g4` 与 `Evalvisitor` 来支持更高级的语法规则
2. 增加语法检查
3. 不使用 Antlr4，自己实现 Lexer 和 Parser

实现任何的 bonus 之前，都请与助教联系。

## 📝Guide

关于本次大作业的所有问题，都可以在 [Q&A](https://notes.sjtu.edu.cn/HL4W3qefT-iIBSPkF_pUsA) 中或者本仓库的 issue 中提问。助教会更新在 Q&A 和文档中。

### 📄语法

本次作业使用的 Python 的语法在 [Grammar](docs/grammar.md) 查看。

### ⚙️ANTLR

关于 ANTLR 的安装与使用，详见 [ANTLR](docs/antlr_guide.md)。

### 🧪实现

如果你想知道从何下手，可以参考 [完成流程](docs/workflow_details.md)。

### 📇索引

如果你想查看一段 Python 代码通过 ANTLR 生成的语法树的结构，参考：[可视化工具](docs/antlr_guide.md#使用antlr内置的可视化工具)。

如果你想知道 `std::any` 是什么，可以参考：前置任务的 README。

如果你想知道怎么遍历树，参考：[补全相关代码](docs/workflow_details.md#step-4-完成-srcevalvisitorh)。

如果你想看一个 demo 来理解这个作业，参考：[Apple Pie Interpreter](https://github.com/ACMClassCourse-2021/Apple-Pie-Interpreter)。

还有一些 [小建议](docs/suggestions.md)。
