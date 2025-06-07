from flask import Flask, request, render_template
import pandas as pd
import os

app = Flask(__name__)

def load_data():
    # 使用相對路徑載入 Mantis.xlsx
    file_path = os.path.join(os.path.dirname(__file__), 'Mantis.xlsx')
    df = pd.read_excel(file_path)
    df = df[df['MA_WorkLoad'] > 0]
    df['回報日期'] = pd.to_datetime(df['回報日期'])
    # 清理所有欄位中的換行符號
    df = df.applymap(lambda x: str(x).replace('\n', '') if isinstance(x, str) else x)
    # 按回報日期降序排序
    df = df.sort_values(by='回報日期', ascending=False)
    return df

@app.route('/', methods=['GET'])
def index():
    mode = request.args.get('mode', 'monthly')
    assignee_filter = request.args.get('assignee', None)  # 新增分配給篩選條件
    df = load_data()

    # 如果有選擇分配給，則進行篩選
    if assignee_filter:
        df = df[df['分配給'] == assignee_filter]

    if mode == 'monthly':
        stats = monthly_summary(df.copy())  # 使用複本
    elif mode == 'weekly':
        stats = weekly_summary(df.copy())  # 使用複本
    elif mode == 'monthly_assignee':
        stats = monthly_by_assignee(df.copy())  # 使用複本
    elif mode == 'weekly_assignee':
        stats = weekly_by_assignee(df.copy())  # 使用複本
    else:
        stats = monthly_summary(df.copy())  # 使用複本

    print(stats)  # 新增的除錯輸出

    # 清理資料框中的多餘換行符號
    stats = stats.applymap(lambda x: str(x).replace('\n', '') if isinstance(x, str) else x)
    stats = stats.replace(r'\n', '', regex=True)  # 額外清理換行符號

    # 獲取所有唯一的分配給值，供下拉選單使用
    assignees = df['分配給'].unique().tolist()
    table_html = stats.to_html(classes='data', index=False, border=0, table_id="report-table")
    return render_template(
        'index.html',
        table_html=table_html,
        mode=mode,
        assignees=assignees,
        selected_assignee=assignee_filter
    )

def monthly_summary(df):
    # 每月統計邏輯
    df = df.copy()  # 確保使用複本
    df['月份'] = df['回報日期'].dt.to_period('M')
    
    # 先進行分組和加總
    result = df.groupby('月份').agg({
        'MA_WorkLoad': 'sum'  # 加總MA_WorkLoad
    }).reset_index()
    
    # 按月份降序排序
    result = result.sort_values(by='月份', ascending=False)
    
    # 新增 MA_WorkLoad(Day) 欄位
    result['MA_WorkLoad(Day)'] = result['MA_WorkLoad'] / 8
    # 新增 MA_WorkLoad(Month) 欄位
    result['MA_WorkLoad(Month)'] = result['MA_WorkLoad'] / 160
    
    # 確保只有需要的欄位
    result = result[['月份', 'MA_WorkLoad', 'MA_WorkLoad(Day)', 'MA_WorkLoad(Month)']]
    
    # 將月份轉換為字串格式
    result['月份'] = result['月份'].astype(str)
    
    return result

def weekly_summary(df):
    df = df.copy()
    # 取得每筆資料的週一
    df['週一'] = df['回報日期'] - pd.to_timedelta(df['回報日期'].dt.weekday, unit='d')
    # 取得每筆資料的週日
    df['週日'] = df['週一'] + pd.Timedelta(days=6)
    # 產生區間字串
    df['週區間'] = df['週一'].dt.strftime('%Y-%m-%d') + '~' + df['週日'].dt.strftime('%Y-%m-%d')
    
    # 先進行分組和加總
    result = df.groupby('週區間').agg({
        'MA_WorkLoad': 'sum'  # 加總MA_WorkLoad
    }).reset_index()
    
    # 按週區間降序排序
    result = result.sort_values(by='週區間', ascending=False)
    
    # 新增 MA_WorkLoad(Day) 欄位
    result['MA_WorkLoad(Day)'] = result['MA_WorkLoad'] / 8
    # 新增 MA_WorkLoad(Month) 欄位
    result['MA_WorkLoad(Month)'] = result['MA_WorkLoad'] / 160
    
    # 確保只有需要的欄位
    result = result[['週區間', 'MA_WorkLoad', 'MA_WorkLoad(Day)', 'MA_WorkLoad(Month)']]
    return result

def monthly_by_assignee(df):
    # 每月按分配給統計邏輯
    df = df.copy()  # 確保使用複本
    df['月份'] = df['回報日期'].dt.to_period('M')
    # 排除非數值型欄位
    numeric_columns = df.select_dtypes(include='number').columns
    # 移除月份從 numeric_columns 中（如果存在）
    numeric_columns = [col for col in numeric_columns if col != '月份' and col != '編號']
    result = df.groupby(['月份', '分配給'])[numeric_columns].sum().reset_index()
    # 按月份和分配給降序排序
    result = result.sort_values(by=['月份', '分配給'], ascending=[False, True])
    # 新增 MA_WorkLoad(Day) 欄位
    result['MA_WorkLoad(Day)'] = result['MA_WorkLoad'] / 8
    # 新增 MA_WorkLoad(Month) 欄位
    result['MA_WorkLoad(Month)'] = result['MA_WorkLoad'] / 160
    # 只保留需要的欄位
    result = result[['月份', '分配給', 'MA_WorkLoad', 'MA_WorkLoad(Day)', 'MA_WorkLoad(Month)']]
    return result

def weekly_by_assignee(df):
    df = df.copy()
    df['週一'] = df['回報日期'] - pd.to_timedelta(df['回報日期'].dt.weekday, unit='d')
    df['週日'] = df['週一'] + pd.Timedelta(days=6)
    df['週區間'] = df['週一'].dt.strftime('%Y-%m-%d') + '~' + df['週日'].dt.strftime('%Y-%m-%d')
    numeric_columns = df.select_dtypes(include='number').columns
    numeric_columns = [col for col in numeric_columns if col != '編號']
    result = df.groupby(['週區間', '分配給'])[numeric_columns].sum().reset_index()
    result = result.sort_values(by=['週區間', '分配給'], ascending=[False, True])
    # 新增 MA_WorkLoad(Day) 欄位
    result['MA_WorkLoad(Day)'] = result['MA_WorkLoad'] / 8
    # 新增 MA_WorkLoad(Month) 欄位
    result['MA_WorkLoad(Month)'] = result['MA_WorkLoad'] / 160
    result = result[['週區間', '分配給', 'MA_WorkLoad', 'MA_WorkLoad(Day)', 'MA_WorkLoad(Month)']]
    return result

if __name__ == '__main__':
    app.run(debug=True)