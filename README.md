# psy_exps

> Keep rebuilding wheels. 
---

## 运行需求
- 由于 Windows 不支持将两只键盘或鼠标作为独立的输入源，因此除了 `graph_dyeing` 中 带有`_kb` (keyboard) 字段的脚本外，其它脚本均需要连接**两只手柄**运行。
- 由于 macOS 对手柄的支持较差，因此无法在 macOS 上运行。
- 环境：
    - `graph_dyeing` & `grid_moving`
        - Python 3.8.8
        - psychopy 2023.2.3 (standalone)
    - `original_pgg`
        - Python 3.10.0
        - psychopy 2023.2.3 (package)
- 实验机连接两台独立的显示器；单显示器模式仅供调试。