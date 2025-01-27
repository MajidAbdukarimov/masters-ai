# FIFA 17 Player Data Analysis

## Objective
To analyze player performance data from the FIFA 17 dataset and verify hypotheses from experts regarding:
1. The age distribution of players born in England and France.
2. The hypothesis that defenders born in Italy have higher averages in all respects compared to those from other countries.

---

## Dataset Information
The dataset contains various attributes for FIFA 17 players, including:
- **Age**: Player's age.
- **Nationality**: Country of origin.
- **Position**: Player's position on the field (e.g., CB, LB, RB).
- **Performance Metrics**: Metrics such as Standing Tackle, Sliding Tackle, Interceptions, Strength, and Aggression.

---

## Analysis 1: Age Distribution of Players from England and France
### Methodology
- Filtered players based on their nationality (England and France).
- Created histograms to compare the age distributions of players born in these countries.

### Results
- **England**: Broader spread of ages, indicating a more diverse age group among players.
- **France**: Concentration of players in a specific age group, showing a peak in their age distribution.

### Visualization
![Age Distribution of Players from England and France](#)

---

## Analysis 2: Performance of Defenders by Country
### Hypothesis
Experts claim that defenders born in Italy have higher averages in all performance metrics compared to defenders from other countries.

### Methodology
1. Filtered defenders based on their positions: CB, LB, RB, LWB, RWB.
2. Calculated average performance metrics for defenders grouped by nationality.
3. Focused on the top 5 countries with the most defenders.
4. Compared Italy's averages against the overall averages of the top 5 countries.

### Results
- Italy's defenders excel in **Strength** and **Standing Tackle**.
- For **Sliding Tackle**, **Interceptions**, and **Aggression**, Italy performs well but does not significantly outperform other top countries.

### Conclusion
The hypothesis is **partially true**: while Italy's defenders are strong in certain metrics, they do not consistently dominate across all metrics.

### Visualization
![Average Performance of Top 5 Defenders by Country](#)

---

## Code Snippets
### Histogram of Player Ages by Nationality
```python
import matplotlib.pyplot as plt

# England and France age data
england_ages = data[data['Nationality'] == 'England']['Age']
france_ages = data[data['Nationality'] == 'France']['Age']

# Plot histograms
plt.figure(figsize=(10, 6))
plt.hist(england_ages, bins=15, alpha=0.7, label='England', color='blue', edgecolor='black')
plt.hist(france_ages, bins=15, alpha=0.7, label='France', color='red', edgecolor='black')
plt.title('Age Distribution of Players from England and France', fontsize=14)
plt.xlabel('Age', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.legend(fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
```

### Average Performance of Defenders by Country
```python
# Average stats for defenders by nationality
defender_positions = ['CB', 'LB', 'RB', 'LWB', 'RWB']
defenders = data[data['Position'].isin(defender_positions)]

defenders.groupby('Nationality').mean(numeric_only=True)

# Top 5 countries with the most defenders
top_5_countries = defenders['Nationality'].value_counts().head(5).index
average_stats_top_5 = average_stats_by_country.loc[top_5_countries]

# Performance metrics comparison
performance_metrics = ['StandingTackle', 'SlidingTackle', 'Interceptions', 'Strength', 'Aggression']
plt.figure(figsize=(12, 6))
average_stats_top_5[performance_metrics].T.plot(kind='bar', alpha=0.8, colormap='viridis', edgecolor='black')
plt.title('Average Performance of Top 5 Defenders by Country', fontsize=14)
plt.ylabel('Average Metric Value', fontsize=12)
plt.xlabel('Performance Metrics', fontsize=12)
plt.xticks(rotation=0, fontsize=10)
plt.legend(title='Country', fontsize=10, loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
```

---

## Conclusion
This analysis highlights insights from the FIFA 17 dataset regarding:
- Age distributions of players by nationality.
- Performance comparison of defenders by nationality, especially Italy.

These insights can help further validate or refine expert hypotheses regarding player performance trends.
