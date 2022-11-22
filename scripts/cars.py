#!/usr/bin/env python3

# "##" = action comment, e.g. comment out local path, uncomment VM path
# "#" = casual comment (no action needed)

import locale
import sys
# https://ru.stackoverflow.com/questions/418982/%D0%9A%D0%BE%D0%BB%D0%B8%D1%87%D0%B5%D1%81%D1%82%D0%B2%D0%BE-%D0%BF%D0%BE%D0%B2%D1%82%D0%BE%D1%80%D1%8F%D1%8E%D1%89%D0%B8%D1%85%D1%81%D1%8F-%D1%8D%D0%BB%D0%B5%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2-%D0%B2-%D1%81%D0%BF%D0%B8%D1%81%D0%BA%D0%B5
from collections import Counter
# CSV files work with (most popular car_year)
## You need to install Pandas for successful work
# pip install pandas
import pandas as pd
from numpy.random import randint
# Creating Python STRING of STRINGS to generate PDF
import json
# Creation PDF from JSON (Python STRING of STRINGS)
import reports
# For sending the E-mail massages
import emails
# For the sender (IP address) to pull up automatically
import os


def load_data(filename):
  """Loads the contents of filename as a JSON file."""
  with open(filename) as json_file:
    data = json.load(json_file)
    # print('---------------')
    # print(" # QA print(data)")
    # print(data)
    # print(filename)
    # print('---------------')
  return data


def format_car(car):
  """Given a car dictionary, returns a nicely formatted name."""
  return "{} {} ({})".format(
      car["car_make"], car["car_model"], car["car_year"])


def process_data(data):
  """Analyzes the data, looking for maximums.

  Returns a list of lines that summarize the information.
  """
  max_revenue = {"revenue": 0}
  for item in data:
    # print('---------------')
    # print(" # QA print(data)")
    # print(item)
    # print('---------------')
    # Calculate the revenue generated by this model (price * total_sales)
    # We need to convert the price from "$1234.56" to 1234.56
    item_price = locale.atof(item["price"].strip("$"))
    # print(item_price)
    item_revenue = item["total_sales"] * item_price
    # print(item_revenue)
    if item_revenue > max_revenue["revenue"]:
      item["revenue"] = item_revenue
      max_revenue = item
      # print(item)
  # TODO: also handle max sales
  max_sales = {"total_sales": 0}
  for item in data:
    item_sales = item["total_sales"]
    if item_sales > max_sales["total_sales"]:
      item["total_sales"] = item_sales
      max_sales = item
      # print(item)

  # TODO: also handle most popular car_year
  local_count_frequency = 'Car_year,Count_frequency,Total_sales' + '\n'

  # print(local_count_frequency)

  # Creating a blank for a CSV file
  for item in data:
    """A CSV file has been created, which contains 
      the statistics data selected for the task 
      (year "car_year", number of sales "total_sales")
      
      Pandas ("import pandas as pd") was used to parse the generated CSV file."""

    local_car = item["car"]
    local_car_year = local_car["car_year"]
    local_car_sales = item["total_sales"]

    # An additional value "1" was assigned to each line (the column "Count_frequency" was added
    # to the CSV file). The logic is that each one sale has one unit. And if you count
    # the number of "Count_frequency" units, then you can understand
    # the most popular sales year (this will be the maximum value of "Count_frequency").
    local_count_frequency += str(local_car_year) + ',' + str(1) + ',' + str(local_car_sales) + '\n'

    # print(local_car_year, local_car_sales)

  # print('--------------------')
  # print(local_count_frequency)
  # print('--------------------')

  # Creating CSV file from a blank "local_count_frequency"
  create_csv_file_car_year_and_sales_not_sorted = open("temp_car_year_file.csv", "w")
  create_csv_file_car_year_and_sales_not_sorted.write(local_count_frequency)
  create_csv_file_car_year_and_sales_not_sorted.close()

  df = pd.read_csv('temp_car_year_file.csv')

  # Statistics requested in the task with correct filtering and sums
  # Pandas hint https://youtu.be/vmEHCJofslg
  statistic_summary_data = df.groupby(['Car_year']).sum().sort_values('Count_frequency', ascending=False)
  result_car_most_popular_year = df.groupby(['Car_year']).sum().sort_values('Count_frequency', ascending=False).index.tolist()[0]
  result_car_most_popular_year_total_sales = df.groupby(['Car_year']).sum().sort_values('Count_frequency', ascending=False).iloc[0,1]

  # test_data_show = statistic_1['Car_year']
  print('--------------------')
  print('# statistic_summary_data')
  print(statistic_summary_data)

  print('--------------------')
  print("# result_car_most_popular_year")
  print(result_car_most_popular_year)
  print('--------------------')
  print('--------------------')
  print("# result_car_most_popular_year_total_sales")
  print(result_car_most_popular_year_total_sales)
  print('--------------------')


  summary = [
    "The {} generated the most revenue: ${}".format(
      format_car(max_revenue["car"]), max_revenue["revenue"]), ''
    "The {} had the most sales: {}".format(
      format_car(max_sales["car"]), max_sales["total_sales"]
    ),
    "The most popular year was {} with {} sales".format(
      result_car_most_popular_year, result_car_most_popular_year_total_sales
    )
  ]

  return summary


def cars_dict_to_table(car_data):
  """Turns the data in car_data into a list of lists."""
  table_data = [["ID", "Car", "Price", "Total Sales"]]
  for item in car_data:
    table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])
  return table_data


def main(argv):
  """Process the JSON data and generate a full report out of it."""
  data = load_data("car_sales.json")
  summary = process_data(data)
  # string_summary = str(summary)
  email_join_summary = '\n'.join(summary)
  pdf_join_summary = '<br/>'.join(summary)
  # splited_summary = join_summary.split("\n")



  print('--------------------')
  print('# "email_join_summary" from "def main"')
  print(email_join_summary)
  print('--------------------')
  # TODO: turn this into a PDF report
  """Using Pandas to open json file"""
  # df = pd.read_json('car_sales.json')
  # print('--------------------')
  # print('# df.to_string()')
  # print(df.to_string())
  # print('--------------------')

  """Using "import json" to open JSON to LIST"""
  # https://www.geeksforgeeks.org/read-json-file-using-python/
  json_file = open('car_sales.json')

  # returns JSON object as a dictionary
  data_of_json_file = json.load(json_file)

  # Creating the foundation for creating a PDF report
  data_for_PDF_report = [['ID','Car','Price','Total Sales']]

  # Iterating through the json list
  for iteration in data_of_json_file:

    # Temporary data for "local_car_make_model_year"
    local_car_make = iteration['car']['car_make']
    local_car_model = iteration['car']['car_model']
    local_car_year = str(iteration['car']['car_year'])

    # Data we need for report and PDF generation
    local_car_id = str(iteration['id'])
    local_car_make_model_year = local_car_make + ' ' + local_car_model + ' (' + local_car_year + ")"
    local_car_price = iteration['price']
    local_car_total_sales = str(iteration['total_sales'])

    # Temporary data for final report
    final_report_string = (local_car_id + "," + local_car_make_model_year + ',' + local_car_price + ',' + local_car_total_sales)
    splited_final_report_string = final_report_string.split(",")

    # QA report data
    # All data of JSON
    # print(iteration)

    # Data for PDF report
    # print(final_report_string)
    data_for_PDF_report += [splited_final_report_string]
  print('------------------------')
  print('------------------------')
  print('# datat_for_PDF_report')
  print(data_for_PDF_report)
  print('------------------------')
  # print(sys.path)
  ## Online version of the path
  reports.generate("/tmp/cars.pdf", "Sales summary for last month", pdf_join_summary, data_for_PDF_report)
  ## Local version of the path
  # reports.generate("/Users/il/PycharmProjects/qwiklabs.com-Automatically-Generate-a-PDF-and-send-it-by-Email-Python/scripts/report.pdf", "Sales summary for last month", pdf_join_summary, data_for_PDF_report)

  # Closing file
  json_file.close()

  # TODO: send the PDF report as an email attachment
  sender = "automation@example.com"
  receiver = "{}@example.com".format(os.environ.get('USER'))
  subject = "Sales summary for last month"
  body = email_join_summary

  ## Online version of the path
  message = emails.generate(sender, receiver, subject, body, "/tmp/cars.pdf")
  ## Local version of the path
  # message = emails.generate(sender, receiver, subject, body, "/Users/il/PycharmProjects/qwiklabs.com-Automatically-Generate-a-PDF-and-send-it-by-Email-Python/scripts/report.pdf")
  emails.send(message)

print('---------------')
print(" # main(sys.argv)")
print(main(sys.argv))
print(sys.argv)
print('---------------')

if __name__ == "__main__":
  main(sys.argv)
