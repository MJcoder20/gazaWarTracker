import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import folium


# nz = gpd.read_file('../data/gaza_240503.gpkg')
# # Read the GeoPackage file
# gdf = gpd.read_file('../data/gaza_240503.gpkg', layer=None)
# layers = gpd.list_layers('../data/gaza_240503.gpkg')
# # Display the first few rows of attributes
# print(gdf.head())
# print(layers)
# # List all attribute column names
# print("Attribute columns:", gdf.columns)
# print(nz.head())
# nz.plot()

# vars = ['Land_area', 'Population', 'Median_income', 'Sex_ratio']
# nz[vars]
# fig, ax = plt.subplots()
# nz.plot(ax=ax, color='none')
# nz.plot(color='green')

# fig, ax = plt.subplots()
# nz.plot(ax=ax, color='none', edgecolor='lightgrey')


# fig, ax = plt.subplots()
# nz.plot(ax=ax, color='lightgrey', edgecolor='grey')
# nz.apply(
#     lambda x: ax.annotate(
#         text=x['Name'],
#         xy=x.geometry.centroid.coords[0],
#         ha='center'
#     ),
#     axis=1
# );

# ctr = nz[['Island', 'geometry']].dissolve(by='Island').reset_index()
# ctr['geometry'] = ctr.centroid
# fig, ax = plt.subplots()
# nz.plot(ax=ax, color='none', edgecolor='lightgrey')
# ctr.apply(
#     lambda x: ax.annotate(
#         text=x['Island'],
#         xy=x.geometry.coords[0],
#         ha='center',
#         weight='bold'
#     ),
#     axis=1
# );
# plt.show()


# read Excel file
df = pd.read_excel("C:/Users/pc/PycharmProjects/mitx_project/data/Book1.xlsx")
# Convert date column
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)


# Line Chart – Martyr count by date
def line_chart():
    plt.figure(figsize=(10, 6))
    sns.lineplot(x="Date", y="Martyr Count", data=df, marker="o")
    plt.title("Martyrs by Date")
    plt.xlabel("Date")
    plt.ylabel("Martyr Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Bar Chart – Most damaged regions
def damaged_regions_bar_chart():
    region_damage = df.groupby("Region")["Damaged Homes Count"].sum().sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=region_damage.values, y=region_damage.index)
    plt.title("Most Damaged Regions")
    plt.xlabel("Number of Damaged Homes")
    plt.ylabel("Region")
    plt.tight_layout()
    plt.show()


# Pie Chart - Attack type distribution
def pie_chart():
    attack_distribution = df["Attack Type"].value_counts()

    plt.figure(figsize=(6, 6))
    plt.pie(attack_distribution, labels=attack_distribution.index, autopct='%1.1f%%', startangle=140)
    plt.title("Attack Type Distribution")
    plt.tight_layout()
    plt.show()


#Bar chart of days with the highest martyr counts.
def martyr_counts_bar_chart():
    top_days = df.sort_values("Martyr Count", ascending=False).head(5)
    plt.figure(figsize=(8, 6))
    sns.barplot(x=top_days["Date"].dt.strftime('%Y-%m-%d'), y=top_days["Martyr Count"])
    plt.title("Top 5 Deadliest Days")
    plt.xlabel("Date")
    plt.ylabel("Martyr Count")
    plt.tight_layout()
    plt.show()


# Heatmap of Damaged Homes by Region and Attack Type
def heatmap():
    pivot_table = df.pivot_table(
        index="Region", columns="Attack Type", values="Damaged Homes Count", aggfunc="sum", fill_value=0
    )

    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_table, annot=True, fmt="d", cmap="Reds")
    plt.title("Damaged Homes by Region and Attack Type")
    plt.tight_layout()
    plt.show()
