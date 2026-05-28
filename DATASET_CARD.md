# Dataset Card: Multi-topology Power Module Thermal Simulation Dataset

English | [中文](#中文数据集卡)

## Dataset Details

- **Dataset name:** Multi-topology Power Module Thermal Simulation Dataset
- **Domain:** Power electronics, power module packaging, thermal analysis, surrogate modeling
- **Data type:** HDF5 files containing 2D fields and masks
- **Samples:** 20,350
- **Resolution:** 256 x 256
- **Splits:** TrainData, ValData, TestData
- **License:** CC BY 4.0
- **Maintainer:** Ruiting Ke, Shanghai Jiao Tong University

## Purpose

The dataset supports supervised learning for steady-state thermal estimation in power modules with varying topology. It is intended for image-to-field regression, multi-modal learning, topology-aware surrogate modeling, and benchmarking of fast thermal estimation methods.

## Data Generation

The data were generated from an automated CADQuery and COMSOL Multiphysics + MATLAB workflow. Parametric CAD models define chip count, chip placement, copper partitioning, and material regions. Invalid geometries were filtered. FEM simulations then solved steady-state heat conduction with chip heat sources and bottom convection boundary conditions. Outputs were exported as top-surface temperature fields and per-chip maximum temperatures, then merged with material masks, power maps, and cooling labels into HDF5 files.

## Data Fields

Each sample contains:

- `temperature`: FEM top-surface temperature field.
- `power_map`: Spatial power-density map.
- `instance_map`: Chip instance labels.
- `ceramic_mask`, `baseplate_mask`, `copper_mask`: Binary material masks.
- `h_normalized`: Normalized convective heat-transfer coefficient.
- `max_temps`: Per-chip maximum temperatures.
- `row_ids`: Chip ids aligned with `max_temps`.

Path labels encode split, topology family, mask id, `Pigbt`, `Pfwd`, and `h`.

## Splits

| Split | Samples |
| --- | ---: |
| TrainData | 14,242 |
| ValData | 3,050 |
| TestData | 3,058 |

The split is provided at the file-tree level. Users should keep this split for comparable benchmarks unless their study requires a different protocol.

## Intended Uses

- Training and evaluating multi-topology thermal surrogate models.
- Comparing image-based and vector-based representations for power-module thermal estimation.
- Developing uncertainty estimation, active learning, or physics-aware learning methods for FEM-generated thermal data.
- Studying layout-aware temperature-field regression under variable chip counts.

## Out-of-Scope Uses

- Direct certification or safety validation of physical products without additional experimental validation.
- Claims about transient thermal behavior, because the provided fields are steady-state outputs.
- Extrapolation to materials, package structures, cooling conditions, or geometries outside the generated design space without validation.

## Known Limitations

- The data are simulation-derived and inherit assumptions from the CAD/FEM workflow.
- Not every layout id contains every possible operating-condition combination.
- The dataset represents top-surface steady-state temperature fields, not full 3D transient temperature histories.
- Units and scaling should be checked against the HDF5 fields and accompanying paper before integrating into a production engineering workflow.

## Citation

Please cite the accompanying paper and this repository. See `CITATION.cff`.

---

# 中文数据集卡

## 数据集信息

- **数据集名称：** 多拓扑功率模块热仿真数据集
- **领域：** 功率电子、功率模块封装、热分析、代理模型
- **数据类型：** 包含二维场和掩膜的 HDF5 文件
- **样本数：** 20,350
- **分辨率：** 256 x 256
- **划分：** TrainData、ValData、TestData
- **许可证：** CC BY 4.0
- **维护者：** Ruiting Ke，上海交通大学

## 用途

本数据集用于多拓扑功率模块稳态热场估计的监督学习研究，适合图像到温度场回归、多模态学习、拓扑感知热代理模型和快速热估计方法评测。

## 生成方式

数据由 CADQuery 参数化建模与 COMSOL Multiphysics + MATLAB 自动仿真流程生成。参数化 CAD 模型定义芯片数量、芯片位置、铜层分区和材料区域，并过滤几何无效样本。随后通过 FEM 求解稳态热传导问题，芯片作为热源，底板施加对流边界条件。最终将顶表面温度场、每芯片最高温度、材料掩膜、功率图和换热条件合并为 HDF5 文件。

## 数据字段

每个样本包含：

- `temperature`：FEM 顶表面温度场。
- `power_map`：空间功率密度图。
- `instance_map`：芯片实例标签。
- `ceramic_mask`、`baseplate_mask`、`copper_mask`：材料二值掩膜。
- `h_normalized`：归一化对流换热系数。
- `max_temps`：每个芯片的最高温度。
- `row_ids`：与 `max_temps` 对应的芯片编号。

路径标签编码了数据划分、拓扑族、掩膜编号、`Pigbt`、`Pfwd` 和 `h`。

## 推荐用途

- 训练和评估多拓扑热代理模型。
- 比较图像表示与传统数值向量表示在热估计中的效果。
- 开发面向 FEM 热数据的不确定性估计、主动学习或物理约束学习方法。
- 研究芯片数量可变时的布局感知温度场回归。

## 不适用范围

- 未经额外实验验证，不能直接用于实体产品认证或安全验证。
- 数据为稳态结果，不用于瞬态热行为结论。
- 对生成设计空间之外的材料、封装、冷却条件或几何进行外推时，需要额外验证。

## 已知限制

- 数据来自仿真，继承 CAD/FEM 流程中的建模假设。
- 并非每一个版图编号都包含所有可能工况组合。
- 数据提供顶表面稳态温度场，不包含完整三维瞬态温度历史。
- 在工程生产流程中使用前，应结合 HDF5 字段和论文确认单位、缩放和适用范围。
