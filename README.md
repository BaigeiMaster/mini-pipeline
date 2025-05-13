# Mini Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-0.1.0-green)](https://github.com/username/mini-pipeline)

A lightweight and flexible pipeline framework for chaining tasks in Python.

[English](#english) | [中文](#中文)

<a id="english"></a>
## English

### Overview

Mini Pipeline is a lightweight framework that allows you to create and chain tasks in a pipeline. It provides a flexible way to define task sequences, control data flow between tasks, and manage task execution. The framework is designed to be simple yet powerful, making it easy to build complex data processing workflows.

### Features

- Create pipelines with multiple tasks
- Chain tasks automatically or manually
- Control data flow between tasks using receiver IDs
- Support for nested pipelines
- Easy to extend with custom tasks
- Flexible task routing and data handling
- Support for multiple receivers for a single task output

### Installation

```bash
# Install from local directory
pip install .

# Or directly from GitHub
pip install git+https://github.com/BaigeiMaster/mini-pipeline.git
```

### Requirements

- Python 3.8 or higher

### Basic Usage

#### Creating a Simple Pipeline

```python
from mini_pipeline import Pipeline, BaseTask

# Create custom tasks by inheriting from BaseTask
class AddTask(BaseTask):
    def run(self, arg=None):
        if arg is None:
            return 5
        return arg + 5

class MultiplyTask(BaseTask):
    def run(self, arg=None):
        if arg is None:
            return 2
        return arg * 2

# Create a pipeline with tasks
pipeline = Pipeline([
    AddTask(),
    MultiplyTask()
])

# Run the pipeline
result = pipeline.run(10)
print(result)  # Output: 30 ((10 + 5) * 2)
```

#### Manual Task Chaining

You can manually specify which task should receive the output of another task:

```python
from mini_pipeline import Pipeline, BaseTask

class GenerateTask(BaseTask):
    def run(self, arg=None):
        return [1, 2, 3, 4, 5]

class FilterTask(BaseTask):
    def run(self, arg=None):
        if arg is None:
            return []
        return [x for x in arg if x % 2 == 0]

class SumTask(BaseTask):
    def run(self, arg=None):
        if arg is None:
            return 0
        return sum(arg)

# Create tasks with specific receiver_id
generate_task = GenerateTask(receiver_id=1)  # Send output to task with ID 1
filter_task = FilterTask(receiver_id=2)      # Send output to task with ID 2
sum_task = SumTask()                         # No specific receiver

pipeline = Pipeline(
    tasks=[generate_task, filter_task, sum_task]
)

result = pipeline.run()
print(result)  # Output: 6 (sum of [2, 4])
```

### Advanced Usage

#### Adding Tasks to a Pipeline

You can add tasks to a pipeline in several ways:

```python
# Method 1: During initialization
pipeline = Pipeline([task1, task2, task3])

# Method 2: Using the add method
pipeline = Pipeline()
pipeline.add(task1)
pipeline.add(task2)

# Method 3: Using the + operator
pipeline = Pipeline([task1]) + task2 + [task3, task4]
```

#### Nested Pipelines

You can create nested pipelines for more complex workflows:

```python
preprocessing_pipeline = Pipeline([
    NormalizeTask(),
    FilterTask()
])

main_pipeline = Pipeline([
    LoadDataTask(),
    preprocessing_pipeline,
    ProcessTask(),
    SaveResultTask()
])

result = main_pipeline.run()
```

#### Using Negative Indices for Receiver IDs

You can use negative indices to specify receivers relative to the end of the pipeline:

```python
# Send output to the last task in the pipeline
task = ProcessTask(receiver_id=-1)

# Send output to the second-to-last task
task = ProcessTask(receiver_id=-2)
```

#### Multiple Receivers

A task can send its output to multiple receivers:

```python
# Send output to tasks with IDs 2 and 4
task = ProcessTask(receiver_id=[2, 4])
```

#### Complex Data Processing Example

Here's a more complex example that demonstrates data processing with multiple paths:

```python
from mini_pipeline import Pipeline, BaseTask

class DataLoaderTask(BaseTask):
    def run(self, arg=None):
        # Simulate loading data from a source
        return {"text": "Sample text", "numbers": [1, 2, 3, 4, 5]}

class TextProcessorTask(BaseTask):
    def run(self, arg=None):
        if arg is None or "text" not in arg:
            return {"processed_text": ""}
        text = arg["text"]
        # Process text (convert to uppercase)
        return {"processed_text": text.upper()}

class NumberProcessorTask(BaseTask):
    def run(self, arg=None):
        if arg is None or "numbers" not in arg:
            return {"processed_numbers": []}
        numbers = arg["numbers"]
        # Process numbers (square each number)
        return {"processed_numbers": [n**2 for n in numbers]}

class ResultCombinerTask(BaseTask):
    def run(self, arg=None):
        if arg is None:
            return {"result": "No data"}

        # Combine results from different processors
        result = {}
        if isinstance(arg, list):
            for item in arg:
                result.update(item)
        else:
            result = arg

        return {"final_result": result}

# Create tasks with specific routing
data_loader = DataLoaderTask(receiver_id=[1, 2])  # Send to both processors
text_processor = TextProcessorTask(receiver_id=3)  # Send to combiner
number_processor = NumberProcessorTask(receiver_id=3)  # Send to combiner
result_combiner = ResultCombinerTask()

pipeline = Pipeline(
    tasks=[data_loader, text_processor, number_processor, result_combiner]
)

result = pipeline.run()
print(result)
# Output: {'final_result': {'processed_text': 'SAMPLE TEXT', 'processed_numbers': [1, 4, 9, 16, 25]}}
```

### API Reference

#### BaseTask

Abstract base class for all tasks.

**Methods:**
- `run(arg=None)`: Execute the task with an optional input argument.

**Properties:**
- `id_`: The task's ID in the pipeline.
- `id_inverse`: The task's ID from the end of the pipeline.
- `receiver_id`: The ID of the task(s) that should receive this task's output.

#### Pipeline

A pipeline that contains and executes tasks.

**Methods:**
- `__init__(tasks=None, chained=True, receiver_id=None)`: Initialize a pipeline.
- `add(task)`: Add a task to the pipeline.
- `init()`: Initialize the pipeline and its tasks.
- `run(arg=None)`: Run the pipeline with an optional input argument.
- `create_chain(tasks)`: Create a chain of tasks.

**Properties:**
- `tasks`: The list of tasks in the pipeline.
- `chained`: Whether tasks are automatically chained. If True, receiver_id will be incremented automatically; if False, receiver_id needs to be specified manually.
- `results`: The results dictionary.
- `inited`: Whether the pipeline has been initialized.

### License

This project is licensed under the MIT License - see the LICENSE file for details.

<a id="中文"></a>
## 中文

### 概述

Mini Pipeline 是一个轻量级框架，允许您在管道中创建和链接任务。它提供了一种灵活的方式来定义任务序列，控制任务之间的数据流，并管理任务执行。该框架设计简单但功能强大，使构建复杂的数据处理工作流变得容易。

### 特性

- 创建包含多个任务的管道
- 自动或手动链接任务
- 使用接收者 ID 控制任务之间的数据流
- 支持嵌套管道
- 易于扩展自定义任务
- 灵活的任务路由和数据处理
- 支持单个任务输出到多个接收者

### 安装

```bash
# 从本地目录安装
pip install .

# 或直接从 GitHub 安装
pip install git+https://github.com/BaigeiMaster/mini-pipeline.git
```

### 要求

- Python 3.8 或更高版本

### 基本用法

#### 创建简单管道

```python
from mini_pipeline import Pipeline, BaseTask

# 通过继承 BaseTask 创建自定义任务
class AddTask(BaseTask):
    def run(self, arg=None):
        if arg is None:
            return 5
        return arg + 5

class MultiplyTask(BaseTask):
    def run(self, arg=None):
        if arg is None:
            return 2
        return arg * 2

# 创建包含任务的管道
pipeline = Pipeline([
    AddTask(),
    MultiplyTask()
])

# 运行管道
result = pipeline.run(10)
print(result)  # 输出: 30 ((10 + 5) * 2)
```

#### 手动任务链接

您可以手动指定哪个任务应该接收另一个任务的输出：

```python
from mini_pipeline import Pipeline, BaseTask

class GenerateTask(BaseTask):
    def run(self, arg=None):
        return [1, 2, 3, 4, 5]

class FilterTask(BaseTask):
    def run(self, arg=None):
        if arg is None:
            return []
        return [x for x in arg if x % 2 == 0]

class SumTask(BaseTask):
    def run(self, arg=None):
        if arg is None:
            return 0
        return sum(arg)

# 创建具有特定 receiver_id 的任务
generate_task = GenerateTask(receiver_id=1)  # 将输出发送到 ID 为 1 的任务
filter_task = FilterTask(receiver_id=2)      # 将输出发送到 ID 为 2 的任务
sum_task = SumTask()                         # 没有特定接收者

pipeline = Pipeline(
    tasks=[generate_task, filter_task, sum_task]
)

result = pipeline.run()
print(result)  # 输出: 6 (对 [2, 4] 求和)
```

### 高级用法

#### 向管道添加任务

您可以通过多种方式向管道添加任务：

```python
# 方法 1: 在初始化期间
pipeline = Pipeline([task1, task2, task3])

# 方法 2: 使用 add 方法
pipeline = Pipeline()
pipeline.add(task1)
pipeline.add(task2)

# 方法 3: 使用 + 运算符
pipeline = Pipeline([task1]) + task2 + [task3, task4]
```

#### 嵌套管道

您可以创建嵌套管道以实现更复杂的工作流：

```python
# 创建预处理管道
preprocessing_pipeline = Pipeline([
    NormalizeTask(),
    FilterTask()
])

# 创建包含预处理管道的主管道
main_pipeline = Pipeline([
    LoadDataTask(),
    preprocessing_pipeline,  # 嵌套管道
    ProcessTask(),
    SaveResultTask()
])

result = main_pipeline.run(data)
```

#### 使用负索引作为接收者 ID

您可以使用负索引来指定相对于管道末尾的接收者：

```python
# 将输出发送到管道中的最后一个任务
task = ProcessTask(receiver_id=-1)

# 将输出发送到管道中的倒数第二个任务
task = ProcessTask(receiver_id=-2)
```

#### 多个接收者

一个任务可以将其输出发送给多个接收者：

```python
# 将输出发送到 ID 为 2 和 4 的任务
task = ProcessTask(receiver_id=[2, 4])
```

#### 复杂数据处理示例

这是一个更复杂的示例，演示了具有多条路径的数据处理：

```python
from mini_pipeline import Pipeline, BaseTask

class DataLoaderTask(BaseTask):
    def run(self, arg=None):
        # 模拟从源加载数据
        return {"text": "示例文本", "numbers": [1, 2, 3, 4, 5]}

class TextProcessorTask(BaseTask):
    def run(self, arg=None):
        if arg is None or "text" not in arg:
            return {"processed_text": ""}
        text = arg["text"]
        # 处理文本（转换为大写）
        return {"processed_text": text.upper()}

class NumberProcessorTask(BaseTask):
    def run(self, arg=None):
        if arg is None or "numbers" not in arg:
            return {"processed_numbers": []}
        numbers = arg["numbers"]
        # 处理数字（对每个数字求平方）
        return {"processed_numbers": [n**2 for n in numbers]}

class ResultCombinerTask(BaseTask):
    def run(self, arg=None):
        if arg is None:
            return {"result": "无数据"}

        # 合并来自不同处理器的结果
        result = {}
        if isinstance(arg, list):
            for item in arg:
                result.update(item)
        else:
            result = arg

        return {"final_result": result}

# 创建具有特定路由的任务
data_loader = DataLoaderTask(receiver_id=[1, 2])  # 发送到两个处理器
text_processor = TextProcessorTask(receiver_id=3)  # 发送到合并器
number_processor = NumberProcessorTask(receiver_id=3)  # 发送到合并器
result_combiner = ResultCombinerTask()

pipeline = Pipeline(
    tasks=[data_loader, text_processor, number_processor, result_combiner]
)

result = pipeline.run()
print(result)
# 输出: {'final_result': {'processed_text': '示例文本', 'processed_numbers': [1, 4, 9, 16, 25]}}
```

### API 参考

#### BaseTask

所有任务的抽象基类。

**方法:**
- `run(arg=None)`: 使用可选输入参数执行任务。

**属性:**
- `id_`: 任务在管道中的 ID。
- `id_inverse`: 任务从管道末尾开始的 ID。
- `receiver_id`: 应接收此任务输出的任务 ID。

#### Pipeline

包含并执行任务的管道。

**方法:**
- `__init__(tasks=None, chained=True, receiver_id=None)`: 初始化管道。
- `add(task)`: 向管道添加任务。
- `init()`: 初始化管道及其任务。
- `run(arg=None)`: 使用可选输入参数运行管道。
- `create_chain(tasks)`: 创建任务链。

**属性:**
- `tasks`: 管道中的任务列表。
- `chained`: 任务是否自动链接。如果为 True ,receiver_id 自动递增；如果为 False ,receiver_id 需要手动指定。
- `results`: 结果字典。
- `inited`: 管道是否已初始化。

### 许可证

该项目根据 MIT 许可证授权 - 有关详细信息，请参阅 LICENSE 文件。
