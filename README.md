# RoS Positional Analyzer
- [Dataset](#dataset)
- [Sources](#sources)
- [Requirements](#requirements)
- [Dataset Format](#Dataset/Format)
- [Dependancies](#dependancies)
- [Chart A](#chart_a)
- [Chart B](#chart_b)
- [Table Headers](#table/headers)
- [Post-Processing Reports](#post-processing/reports)

## Dataset
The dataset will consist of a locally generated (pre-processed) JSON file aggregated by the following:
- The eligible ESPN Player Universe as defined by Eric Karable in his regularly updated Head-2-Head Player Rankings (HTML)
- Fangraphs RoS Projections (CSV)
- Baseball Savant Expected Stats (CSV)

The output of the dataset will consist of Player Name, Position, ESPN ID, Fangraphs ID, Savant ID, League Specific Stats for the Rest of Season (from Fangraphs), and expected 'quality' metrics (from Savant).

## Sources
- The ESPN Player Universe (HTML)
	- This article is generally resident [here](https://www.espn.com/fantasy/baseball/story/_/id/33208450/fantasy-baseball-rankings-head-head-category-rotiserrie-leagues-2022) or searchable with the terms "Fantasy baseball rankings category-based"
	- The HTML will be parsed by an external script that will extract the player universe; names, positional eligibility, ESPN Player ID, and team only
- Fangraphs RoS Projections (CSV)
	- It is recommended to download the Steamer RoS Projections [here](https://www.fangraphs.com/projections.aspx?pos=all&stats=pit&type=steamerr&team=0&lg=all&players=0) on account of their unique usage of Quality Starts 'QS' metrics
- Baseball Savant Expected Stats (CSV)
	- Hitters [here](https://baseballsavant.mlb.com/leaderboard/expected_statistics)
	- Pitchers [here](https://baseballsavant.mlb.com/leaderboard/expected_statistics?type=pitcher&year=2022&position=&team=&min=1). Important that minimum qualified events is set to = 1 so no relievers are excluded.
	- The expected stats leaderboards contain the pertinent information to analyze the quality of underlying performance by reducing the 'noise' around current results

## Requirements
The dataset will require pre-processing to aggregate 3 sources of data into 1 executable dataset.  This project will not be involved in any pre-processing, rather only interact with the refined dataset. 

## Dataset Format
### JSON
JSON is the preferred format because Hitters and Pitchers exist in the generated database but do not share fields

## Dependancies
- json (python standard library)
- pandas (pip install)
- matplotlib (pip install)

## Chart_a
### Heat Map
#### Hitters: 
The fields will be all relevant stats (6 categories) and xOBP, xSLG, xwOBA.  The chart should be sorted on xwOBA in the left-most column.
#### Pitchers
The fields will be all relevant stats (6 categories) and xERA.  The chart should be sorted on xERA in the left-most column.

## Chart_b
### Scatter Plot
#### Hitters
x-axis will be xOBP & y-axis will be xSLG & the size of the marker will represent xwOBA...alpha set to 0.5
#### Pitchers
x-axis will be K/9, y-axis will be QS or SVHD (dependent) & size of the marker will represent xERA...alpha set to 0.5

## Table Headers
#### Hitters
| **Name** | **fTeam** | **Pos.** | **xwOBA** | **R** | **HR** | **RBI** | **SBN** | **OBP** | **xOBP** | **SLG** | **xSLG** |
|----------|-----------|----------|-----------|-------|--------|---------|---------|---------|----------|---------|----------|
|          |           |          |           |       |        |         |         |         |          |         |          |
#### Pitchers
| **Name** | **fTeam** | **Pos.** | **IP** | **QS** | **SVHD** | **K/9** | **WHIP** | **ERA** | **xERA** |
|----------|-----------|----------|--------|--------|----------|---------|----------|---------|----------|
|          |           |          |        |        |          |         |          |         |          |

## Post-Processing Reports
Report change 1 will process the Hitters' raw projected stats into a z-score format that is dependent on number of 'Above Replacement Level' players in the pool at each postion and the quality of Replacement Level Player at said position.  
Report change 2 will process the Pitchers' raw projected stats into a z-score format that is dependent on number of 'Above Replacement Level' players in the pool at each postion (SP & RP) and the quality of Replacement Level Player at said position.  





