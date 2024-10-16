# This is a sample Python script.
from converted_data.converted_disfold_dataset_jsonl import converted_disfold_dataset_jsonl
from converted_data.converted_gren_value_today_json import converted_gren_value_today_json
from src.dataset import mediated_schema
from src.dataset.dataset import Dataset
from src.dataset.mapper import Mapper


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mapper = Mapper(mediated_schema=mediated_schema)
    mapper.map(datasets_for_training=[Dataset(
            header=[
                'id',
                'name',
                'official_name',
                'headquarters_country',
                'headquarters_continent',
                'founded',
                'employees',
                'ceo',
                'foreign_market_cap',
                'american_market_cap',
                'tags'
            ]
            ,
            mapping={
                "id": "None",
                "name": "CompanyName",
                "official_name": "CompanyName",
                "headquarters_country": "None",
                "headquarters_continent": "None",
                "founded": "None",
                "employees": "None",
                "ceo": "None",
                "foreign_market_cap": "None",
                "american_market_cap": "MarketCap",
                "tags": "SectorAndIndustry"
            },
            val=converted_disfold_dataset_jsonl)],
        datasets_to_predict=[
            Dataset(
                header=[
                    "name",
                    "annual_revenue_USD",
                    "annual_net_income_USD",
                    "market_capitalization_2022",
                    "employees_number",
                    "CEO",
                    "headquarters_country",
                    "wikipedia_page_url",
                    "twitter_page_url",
                    "facebook_page_url"
                ],
                mapping={
                    "name": "CompanyName",
                    "market_capitalization_2022": "MarketCap",
                    "annual_revenue_USD": "Revenue",
                    "annual_net_income_USD": "NetIncome",
                    "TotalAssets": "None",
                    "TotalLiabilities": "None",
                    "TotalEquity": "None",
                    "SectorAndIndustry": "None",
                    "Sector": "None",
                    "Industry": "None",
                    "employees_number": "None",
                    "CEO": "None",
                    "headquarters_country": "None",
                    "wikipedia_page_url": "None",
                    "twitter_page_url": "None",
                    "facebook_page_url": "None"
                },
                val=converted_gren_value_today_json
            )
        ]
    )
    mapper.print_mapping()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
