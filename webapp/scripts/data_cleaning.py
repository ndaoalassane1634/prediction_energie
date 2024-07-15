# scripts/data_cleaning.py
import pandas as pd

def clean_data(file_path):
    df = pd.read_csv(file_path)

    supprimer = [
        'Address', 'City', 'Comments', 'ComplianceStatus', 'CouncilDistrictCode', 'DataYear',
        'DefaultData', 'Electricity(kBtu)', 'Electricity(kWh)', 'ENERGYSTARScore',
        'GHGEmissionsIntensity', 'ListOfAllPropertyUseTypes', 'NaturalGas(kBtu)',
        'NaturalGas(therms)',  'OSEBuildingID', 'Outlier', 'PrimaryPropertyType',
        'PropertyGFAParking', 'PropertyGFABuilding(s)', 'PropertyName', 'SiteEnergyUseWN(kBtu)',
        'SiteEUI(kBtu/sf)', 'SiteEUIWN(kBtu/sf)', 'SourceEUI(kBtu/sf)', 'SourceEUIWN(kBtu/sf)',
        'State', 'SteamUse(kBtu)', 'TaxParcelIdentificationNumber',
        'YearsENERGYSTARCertified', 'ZipCode'
    ]
    df.drop(supprimer, axis=1, inplace=True)
    df = df.dropna(subset=['SiteEnergyUse(kBtu)'])
    df = df[df['SiteEnergyUse(kBtu)'] != 0]
    df = df.dropna(subset=['NumberofBuildings'])
    df['BuildingType'].replace(
        {'Nonresidential COS': 'NonResidential', 'Nonresidential WA': 'NonResidential'},
        inplace=True
    )

    columns_to_impute = [
        'LargestPropertyUseTypeGFA', 'SecondLargestPropertyUseTypeGFA', 'ThirdLargestPropertyUseTypeGFA'
    ]
    df[columns_to_impute] = df[columns_to_impute].fillna(0)
    df[['LargestPropertyUseType', 'SecondLargestPropertyUseType', 'ThirdLargestPropertyUseType']] = df[
        ['LargestPropertyUseType', 'SecondLargestPropertyUseType', 'ThirdLargestPropertyUseType']].fillna('0')

    df['GFA_Sum'] = df['LargestPropertyUseTypeGFA'] + df['SecondLargestPropertyUseTypeGFA'] + df['ThirdLargestPropertyUseTypeGFA']

    df.loc[df['PropertyGFATotal'] < df['GFA_Sum'], 'PropertyGFATotal'] = df['GFA_Sum']

    supprimer2 = ['GFA_Sum', 'LargestPropertyUseTypeGFA', 'SecondLargestPropertyUseTypeGFA', 'ThirdLargestPropertyUseTypeGFA']

    df['LargestPropertyUseTypeGFA_Ratio'] = df['LargestPropertyUseTypeGFA'] / df['PropertyGFATotal']
    df['SecondLargestPropertyUseTypeGFA_Ratio'] = df['SecondLargestPropertyUseTypeGFA'] / df['PropertyGFATotal']
    df['ThirdLargestPropertyUseTypeGFA_Ratio'] = df['ThirdLargestPropertyUseTypeGFA'] / df['PropertyGFATotal']

    df.drop(supprimer2, axis=1, inplace=True)

    return df
