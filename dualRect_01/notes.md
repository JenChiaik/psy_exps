# dualRect_01
> renjiayi, 2025.06.13

**比较 type1 和 type2 报告的可靠性及其对集体效益的影响**

## 操纵变量

- 报告指标
    - 置信度：报告对当前选择正确的信心。
    - 百分比：报告当前刺激中黑色部分的平均比例估计值。

## 实验流程

- *solo* / 单人任务（置信度 + 百分比；被试内，顺序平衡）
    - 准备按键
    - 注视点
    - 刺激
    - 个人报告 / *private*
    - 结果反馈

- *dual* / 双人任务（置信度 + 百分比；被试内，顺序平衡）
    - 准备按键
    - 注视点
    - 刺激
    - 个人报告 / *private*
    - 联合报告 / *public*（如果双方二分类判断不一致）
    - 结果反馈

## 数据记录

- rawData_trial（单个被试）

    'exp_num,mode,resolution,sys_time,exp_time,' 
    'block_name,block_index,trail_index,duration,' # block_name(solo,dual)
    'diff_0,diff_1,subject,report_type,report_param,choice,duration,' # report_type(private,public); report_param(confidence,ratio)
