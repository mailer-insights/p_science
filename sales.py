import calendar

import pandas as pd
import requests
from tabula import read_pdf
import zipfile

from plotter import line_plot, pie_plot


class Sales:

    def __init__(self, zip_file_path):
        with zipfile.ZipFile(zip_file_path,"r") as zip_ref:
            zip_ref.extractall()
        csv_path = zip_file_path.split(".zip")[0]
        df = pd.read_csv(csv_path)
        self.df = self.preprocess_df(df)

    def preprocess_df(self, df):
        df.columns = ['id', 'date','zip','payment_usd','hospital_id','hospital_name']
        df['date'] = pd.to_datetime(df['date'])
        df['yr'] = pd.DatetimeIndex(df['date']).year
        df['month'] = pd.DatetimeIndex(df['date']).month
        df['year_month'] = df['yr'].astype(str) + '-' + df['month'].astype(str)
        return df

    def get_total_sales(self):
        self.df['payment_usd'].sum().to_csv('results/total_sales.csv')

    def get_sales_by_month(self):
        df_sales_by_month = self.df.groupby(['yr', 'month'])['payment_usd'].sum()
        monthly_sales = df_sales_by_month.reset_index()


        x = [calendar.month_name[i] for i in range(1,13)]
        y=monthly_sales['payment_usd']
        legend='Sales'
        title="Total Montly Revenue"
        x_label='Month'
        y_label='Monthly Revenue (USD)'
        fig = line_plot(x, y, legend, title, x_label, y_label)
        fig.write_html('results/fig1_monthly_revenue.html')
        fig.show()
        monthly_sales.to_csv('results/monthly_sales.csv', index=False)

    def get_sales_by_zip(self):
        df = self.df
        df['5_digit_zip'] = df['zip'].astype('str').apply(self.trim_zip)
        df_zip_sales = df.groupby(['5_digit_zip'])['payment_usd'].sum()
        df_zip_sales = df_zip_sales.reset_index()
        df_top_ten = df_zip_sales.sort_values(['payment_usd'])[-10:]
        df_bottom_ten = df_zip_sales.sort_values(['payment_usd'])[:10]

        # Top 10 Sales by Zip
        labels = df_top_ten['5_digit_zip'].astype('str')
        values = df_top_ten['payment_usd']
        title="Top 10 Revenue Sources by Zip: 2018"
        fig = pie_plot(labels, values, title)
        fig.show()
        fig.write_html('results/fig2_Top_10_Revenue_by_zip.html')

        # Bottom 10 Sales by Zip
        labels = df_bottom_ten['5_digit_zip'].astype('str')
        values = df_bottom_ten['payment_usd']
        title="Bottom 10 Revenue Sources by Zip: 2018"
        fig = pie_plot(labels, values, title)
        fig.show()
        fig.write_html('results/fig3_Bottom_10_Revenue_by_zip.html')

        df_zip_sales.to_csv("results/Sales_by_zip.csv", index=False)

    def get_revenue_by_teaching(self, teach_hosp_url):

        df=self.df

        # download dataset on teaching hospitals (PDF)
        r = requests.get(teach_hosp_url)

        with open('teaching_hospitals.pdf', 'wb') as f:
            f.write(r.content)
        df_teach_hosp = read_pdf('teaching_hospitals.pdf', pages='all', pandas_options={'header': None})


        """
        The PDF Scraper parsed the tables inconsistenly on different pages. I had to manually determine which column numbers correspond to which fields
        9 cols, name=1, zip=8
        12 cols, name=2, zip=7
        13 cols, name =2, zip=8
        14 cols, name=2, zip=8
        """
        parse_dict = {9:(1,8), 12:(2,7), 13:(2,8), 14:(2, 8)}

        # multi-page pdf converted to list of dataframes, parse out the zip and hospital names
        name_list = []
        zip_list = []
        for df_page in df_teach_hosp:
            num_cols = len(df_page.columns)
            name_col, zip_col = parse_dict[num_cols]
            name_list.append(df_page.iloc[:, name_col].tolist())
            zip_list.append(df_page.iloc[:, zip_col].tolist())

        # first two entries on page 1 are nan and header
        flat_name_list = self.list_flatten(name_list)[2:]
        flat_zipcode_list = self.list_flatten(zip_list)[2:]
        df_teaching_hosp = pd.DataFrame(flat_name_list, flat_zipcode_list)
        df_teaching_hosp.columns = ['teaching_hosp']
        df_teaching_hosp['zip_code'] = df_teaching_hosp.index

        # need zip to be str type for join later
        # will join on 5 digit zip for both df
        df['5_digit_zip'] = df['zip'].astype('str').apply(self.trim_zip)
        df_teaching_hosp['5_digit_zip'] = df_teaching_hosp['zip_code'].astype('str').apply(self.trim_zip)
        joined_df = pd.merge(df, df_teaching_hosp,  how='left', left_on=['hospital_name','5_digit_zip'], right_on = ['teaching_hosp','5_digit_zip'])
        joined_df['category_teaching'] = ~joined_df['teaching_hosp'].isna()
        df_teaching_schools = joined_df.groupby(['category_teaching'])['payment_usd'].sum()
        df_teaching_schools = df_teaching_schools.reset_index()
        df_teaching_schools[df_teaching_schools['category_teaching'] == True]
        df_teaching_schools = df_teaching_schools.replace([True, False], ['teaching', 'non-teaching'])

        labels = df_teaching_schools['category_teaching'].astype('str')
        values = df_teaching_schools['payment_usd']
        title="2018 Revenue Breakdown by Teaching Institution (USD)"
        fig = pie_plot(labels, values, title)
        fig.show()
        fig.write_html('results/fig4_Revenue_by_Teaching_vs_Non_Teach_Inst.html')

        df_teaching_schools[['category_teaching', 'payment_usd']].to_csv('results/Rev_by_teaching_inst.csv', index=False)

    @staticmethod
    def trim_zip(zip):
        return zip[:5]

    @staticmethod
    def list_flatten(input_list):
        # Flatten List of lists
        flat_list = []
        for sublist in input_list:
            for item in sublist:
                flat_list.append(item)
        return flat_list

    def main(self):
        self.get_total_sales()
        self.get_sales_by_month()
        self.get_sales_by_zip()
        teach_hosp_url ='https://www.cms.gov/OpenPayments/Downloads/2018-Reporting-Cycle-Teaching-Hospital-List-pdf.pdf'
        self.get_revenue_by_teaching(teach_hosp_url)


if __name__ == '__main__':
    sales = Sales('Sales.csv.zip')
    sales.main()
