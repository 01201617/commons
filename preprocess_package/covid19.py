import pandas as pd
from fileoperation_package.common import fileoperation_csv_v1_2

def get_infos(country='Japan'):
    csv_paths = r"D:\Nan\PycharmProjects\team_development\input_files\200425__nssac-ncov-data-country-state\*.csv"
    dfs = fileoperation_csv_v1_2.transform_csvsinfolder_to_dfs(csv_paths)

    df_infos = pd.DataFrame(columns=['cum_days[day]', 'last_update[-]', 'confirmed[person]', 'death[person]'])
    for days, (csv_path, df) in enumerate(dfs.items()):
        # 地域のSeries取得
        boolean = df['name'].str.contains(country)

        if country in list(df['name']):
            country_sr = df[boolean]

            confirmed_num = country_sr['Confirmed'].iloc[0]
            death_num = country_sr['Deaths'].iloc[0]
            update_day = country_sr['Last Update'].iloc[0]

            # output のdfに追加
            addRow = pd.DataFrame([days, update_day, confirmed_num, death_num], index=df_infos.columns).T
            df_infos = df_infos.append(addRow)

            if days % 10 == 0:
                print(days, ' / ', len(dfs))

    return df_infos

if __name__ == '__main__':
    df_infors = get_infos()
    print('fin')