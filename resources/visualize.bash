#!/bin/bash

# Command format: bash visualize.bash [Parser Rule Name] -gui
# e.g. If you want to see AST for the whole python program, use the following command:
#     bash visualize.bash file_input -gui
# Please ensure that you've already installed ANTLR4 to directory /usr/local/lib/antlr-4.13.1-complete.jar
# (or set ANTLR_JAR to the path of antlr-4.13.1-complete.jar).

set -u

# Work from the directory that contains this script, so it can be launched from anywhere.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

ANTLR_JAR="${ANTLR_JAR:-/usr/local/lib/antlr-4.13.1-complete.jar}"
export CLASSPATH=".:${ANTLR_JAR}:${CLASSPATH:-}"

# 检查 Python3Demo.g4 文件是否存在
if [ ! -f "Python3Demo.g4" ]; then
    echo "Error: Python3Demo.g4 not found in $SCRIPT_DIR."
    exit 1
fi

# 设置工作目录
output_dir="/tmp/Python3Demo"

# 如果输出目录不存在，则创建它
mkdir -p "$output_dir"

# 检查目录权限，若权限不足则修改权限
if [ ! -w "$output_dir" ]; then
    echo "Directory $output_dir is not writable. Changing permissions..."
    if ! sudo chmod 777 -R "$output_dir"; then
        echo "Error: Failed to change permissions for $output_dir."
        exit 1
    fi
    echo "Permissions for $output_dir have been changed."
fi

# 没有生成过 Java 文件时才运行 antlr4
needs_compile=0
if ! compgen -G "$output_dir/Python3Demo*.java" > /dev/null; then
    echo "Running antlr4 to generate Java files..."
    if ! java -Xmx500M -cp "$ANTLR_JAR:$CLASSPATH" org.antlr.v4.Tool -o "$output_dir" Python3Demo.g4; then
        echo "Error: Failed to generate Java files."
        exit 1
    fi
    needs_compile=1
fi

# 刚生成过 Java 文件，或者还没有 .class 文件时，运行 javac
if [ "$needs_compile" -eq 1 ] || ! compgen -G "$output_dir/Python3Demo*.class" > /dev/null; then
    echo "Compiling Java files..."
    if ! javac "$output_dir"/Python3Demo*.java; then
        echo "Error: Failed to compile Java files."
        exit 1
    fi
fi

# 切换到输出目录，然后运行 grun（即 java）命令，并将所有参数传递给它
echo "Running grun with arguments: $*"
echo "All finished! Please type your code below. Type Ctrl+D to end. Enjoy coding~"
cd "$output_dir" && exec java -Xmx500M -cp "$ANTLR_JAR:$CLASSPATH" org.antlr.v4.gui.TestRig Python3Demo "$@"
