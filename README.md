# Project_Google_Map

Problem : Locate businesses in any given industry at multiple cities using different search operators and finally creating a single dataframe with named indexes.

First Step :
url_genarator.py - this script takes multiple city names and search keywords as input and exports a csv file containing the list of genarated links.

Second Step:
schedule_map_scrap.sh : This bash script takes the links from first step and synchronously runs map_scraper.py for each url and creates a number of csv files for each link.

Third Step:
numpy_csv_cleanup.py : This script takes all the csv from second step and uses pandas module to cleanup some columns and joins all the csv into a single file. 


[![Video Demo](https://img.youtube.com/vi/E5TUek362fc/0.jpg)](https://www.youtube.com/watch?v=E5TUek362fc)
