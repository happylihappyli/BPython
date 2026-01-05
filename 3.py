import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from datetime import datetime, timedelta
import os
from warnings import filterwarnings
from matplotlib import font_manager as fm
filterwarnings('ignore')

def ensure_chinese_font():
    """在 Windows 上自动选择支持中文的 Matplotlib 字体并全局设置"""
    candidates = [
        'Microsoft YaHei',
        'SimSun',
        'NSimSun',
        'SimHei',
        'KaiTi',
        'Microsoft JhengHei',
        'Arial Unicode MS'
    ]
    chosen = None
    for name in candidates:
        try:
            path = fm.findfont(name, fallback_to_default=False)
            if path and os.path.exists(path):
                chosen = name
                break
        except Exception:
            continue
    if chosen:
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = [chosen]
    plt.rcParams['axes.unicode_minus'] = False
    sns.set_style("whitegrid")

ensure_chinese_font()

class DataAnalyzer:
    def __init__(self):
        self.data = None
        self.df = None
        
    def load_sample_data(self):
        """加载多种类型的数据"""
        # 使用sklearn的iris数据集
        iris = load_iris()
        self.df = pd.DataFrame(
            data=np.c_[iris['data'], iris['target']],
            columns=iris['feature_names'] + ['target']
        )
        self.df['species'] = pd.Categorical.from_codes(
            iris.target, iris.target_names
        )
        
        # 添加时间序列数据
        dates = pd.date_range('2023-01-01', periods=150, freq='D')
        self.df['date'] = dates[:150]
        
        # 添加一些随机数据
        np.random.seed(42)
        self.df['random_value'] = np.random.randn(150)
        
        return self.df
    
    def analyze_data(self):
        """展示数据分析和统计"""
        print("="*50)
        print("数据基本信息:")
        print(f"数据形状: {self.df.shape}")
        print(f"数据类型:\n{self.df.dtypes}")
        
        print("\n统计描述:")
        print(self.df.describe())
        
        print("\n相关系数矩阵:")
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        corr_matrix = self.df[numeric_cols].corr()
        print(corr_matrix)
        
        return corr_matrix
    
    def visualize(self):
        """创建多种可视化图表"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('多维度数据可视化分析', fontsize=16)
        
        # 1. 散点图
        axes[0, 0].scatter(self.df['sepal length (cm)'], 
                          self.df['sepal width (cm)'],
                          c=self.df['target'], alpha=0.6)
        axes[0, 0].set_title('花萼长度 vs 宽度')
        axes[0, 0].set_xlabel('花萼长度 (cm)')
        axes[0, 0].set_ylabel('花萼宽度 (cm)')
        
        # 2. 箱线图
        self.df.boxplot(column=['sepal length (cm)', 'sepal width (cm)',
                               'petal length (cm)', 'petal width (cm)'], 
                       ax=axes[0, 1])
        axes[0, 1].set_title('特征分布箱线图')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. 热力图
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        sns.heatmap(self.df[numeric_cols].corr(), 
                   annot=True, fmt='.2f',
                   cmap='coolwarm', ax=axes[0, 2])
        axes[0, 2].set_title('特征相关性热力图')
        
        # 4. 折线图（时间序列）
        time_series = self.df.groupby(self.df['date'].dt.month)['random_value'].mean()
        axes[1, 0].plot(time_series.index, time_series.values, 
                       marker='o', linewidth=2)
        axes[1, 0].set_title('月度平均值变化')
        axes[1, 0].set_xlabel('月份')
        axes[1, 0].set_ylabel('平均值')
        
        # 5. 饼图
        species_count = self.df['species'].value_counts()
        axes[1, 1].pie(species_count.values, 
                      labels=species_count.index,
                      autopct='%1.1f%%', 
                      colors=sns.color_palette('pastel'))
        axes[1, 1].set_title('鸢尾花种类分布')
        
        # 6. 直方图
        axes[1, 2].hist(self.df['sepal length (cm)'], 
                       bins=20, edgecolor='black',
                       alpha=0.7, color='skyblue')
        axes[1, 2].set_title('花萼长度分布直方图')
        axes[1, 2].set_xlabel('花萼长度 (cm)')
        axes[1, 2].set_ylabel('频数')
        
        plt.tight_layout()
        plt.show()
    
    def advanced_operations(self):
        """展示Pandas高级操作"""
        print("\n" + "="*50)
        print("Pandas高级操作演示:")
        
        # 使用apply函数
        self.df['sepal_area'] = self.df.apply(
            lambda row: row['sepal length (cm)'] * row['sepal width (cm)'],
            axis=1
        )
        
        # 分组聚合
        grouped = self.df.groupby('species').agg({
            'sepal length (cm)': ['mean', 'std', 'min', 'max'],
            'sepal width (cm)': ['mean', 'std']
        })
        print("\n按种类分组统计:")
        print(grouped)
        
        # 数据透视表
        pivot_table = pd.pivot_table(
            self.df,
            values='sepal length (cm)',
            index=self.df['date'].dt.month,
            columns='species',
            aggfunc='mean'
        )
        print("\n透视表（月度平均花萼长度）:")
        print(pivot_table)
        
        return grouped, pivot_table

# 使用示例
if __name__ == "__main__":
    analyzer = DataAnalyzer()
    df = analyzer.load_sample_data()
    analyzer.analyze_data()
    grouped, pivot = analyzer.advanced_operations()
    analyzer.visualize()
