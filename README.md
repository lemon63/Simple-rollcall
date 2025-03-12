# 随机点名器

## 项目描述
基于Tkinter开发的课堂随机点名工具，支持导入学生名单、可视化点名动画效果

## 功能特性
✅ 支持TXT文件导入学生名单  
✅ 5秒随机动画点名效果  
✅ 可视化操作界面  
✅ 中文友好界面

## 快速开始
### 环境要求
- Python 3.6+  
- Tkinter（Python内置）

### 安装运行
```bash
# 克隆仓库
git clone https://github.com/lemon63/Simple-rollcall.git

# 进入目录
cd rollcall-tool

# 编辑学生名单
echo "张三\n李四\n王五" > students.txt

# 运行程序
python main.py
```

## 使用演示
![程序界面截图](https://console.pitimg.com/lagny/2025/03/12/67d18c2808d36.png)

## 项目结构
```
随点/
├── main.py          # 主程序
├── students.txt     # 示例名单
├── requirements.txt # 依赖说明
├── LICENSE         # 开源协议
└── README.md       # 说明文档
```

## 贡献指南
1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/yourfeature`)
3. 提交修改 (`git commit -am 'Add some feature'`)
4. 推送分支 (`git push origin feature/yourfeature`)
5. 创建Pull Request

## 开源协议
[GNU GPL-3.0 License](LICENSE)

## 注意事项
⚠️ students.txt文件需使用UTF-8编码  
⚠️ 每次运行前请检查名单内容  
⚠️ 点击按钮后请等待动画完成

## 已测试平台
- Windows 11专业版 版本号：22H2
- Windows 11专业版 版本号：23H2
