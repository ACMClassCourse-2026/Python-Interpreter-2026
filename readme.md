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

本工程先使用 ANTLR 将输入程序解析为解析树（parse tree），再由你编写的 C++ Visitor 按语言语义执行。

## 📅课程信息

- 负责助教：杨奕辰、陈奕珲。
- 解释器在 OJ 上通过 Git 仓库地址提交，构建与评分说明见下文。
- **解释器作业截止日期：2026 年 12 月 3 日，原则上不接受迟交。**

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

1. **必须使用 Visitor pattern（访问者模式）**，以面向对象的方式实现 Python Interpreter。在给定框架中，继承 `Python3ParserBaseVisitor`，在 `EvalVisitor` 中重写所需的 `visitXxx` 方法，并通过 `visit(...)` 访问相应的解析树节点。Visitor 模式是实现要求，不是可选建议；若不按照要求，会在 Code review 时扣除一定分数。入门说明见[实现指南](docs/workflow_details.md)。
2. 评分按下文的 OJ 分组权重与 Code review 比例计算。仓库只提供部分测试点，请根据语法文档自行补充合法测试；如果不确定自造测试是否符合要求，请向助教询问。
3. 首先完成 `./resources/prework.zip` 里面的四则运算计算器，重写 Visitor 接口并提交 `calc.h`。前置任务不计分，但要求**必做**；未完成时，本次解释器作业没有分数。该任务与解释器所需的高精度整数 `int2048` 是两项不同的工作。提交入口和截止时间以课程通知为准。
4. 功能与语义范围以当前 [`docs/grammar.md`](docs/grammar.md) 为准，包括格式化字符串、序列解包与序列增量赋值。输入保证符合规定的词法和语法、没有未定义行为或运行时错误，且输入程序本身不需要标准输入。基础要求不包含语法错误诊断。

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

| 测试分组 | 测试点 | 分值 |
| --- | --- | --- |
| BigIntegerTest | 1 - 20 | 25 |
| Sample | 21 - 34, 67 - 68 | 25 |
| AdvancedTest | 35 - 52, 69 - 71 | 25 |
| ComplexTest | 53 - 56 | 12.5 |
| CornerTest | 57 - 66, 72, 73 | 12.5 |
| **合计** | 1 - 73 | **100** |

- 前置任务（`resources/prework.zip`）不计分，但**必做**；未完成前置任务时本次作业没有分数。
- 公开测试共 36 个，对应 OJ 的 50 分，折算为作业基础成绩中的 40 分；其余 37 个测试点对应另 50 分，折算为 40 分。
- Code review 会检查 Visitor 模式的使用、面向对象的实现与代码质量；具体安排和评分细则以课程通知为准。
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
