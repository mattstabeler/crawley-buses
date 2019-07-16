#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import requests
import dateparser
import json


def main():
  #we use the html parser to parse the url content and store it in a variable.

  page_content = get_page_content()
  busses = get_bus_times(page_content)




  for bus in busses:
    print(bus["bus"], bus["expected"], bus["time"])

  # print (busses)
  # print(json.dumps([time.isoformat() for time in timedata]))

  # In my use case, I want to store the speech data I mentioned earlier.  so in this example, I loop through the paragraphs, and push them into an array so that I can manipulate and do fun stuff with the data.

def handler():
  page_content = get_page_content()
  busses = get_bus_times(page_content)
  print(json.dumps(busses, indent=4, sort_keys=True, default=str))

def get_bus_times(page_content):
  table = page_content.find_all("tr")
  data = []
  for row in table:

    cols = row.find_all('td')
    # print(cols)
    [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])
  # [<td class="body-cell">10</td>, <td align="left" class="body-cell"> </td>, <td class="body-cell">Gatwick Airport</td>, <td class="body-cell"> </td>, <td align="right" class="body-cell">6 Mins</td>, <td class="body-cell"> </td>],

  busses = [{ "bus": bus[0].string, "expected": bus[4].string } for bus in data if len(bus) > 0]

  for bus in busses:
    if bus["expected"][-4:] == 'Mins':
      bus["time"] = dateparser.parse('in ' + bus["expected"])
      # timedata.append(dateparser.parse('in ' + time))
    elif bus["expected"][-4:] == 'Due':
      bus["time"] = dateparser.parse("now")
    else:
      bus["time"] = dateparser.parse(bus["expected"])
      # timedata.append(dateparser.parse(time))

  return busses

def get_page_content():
  page_link = 'http://metrobus.acisconnect.com/text/WebDisplay.aspx?stopRef=4400CY0086&stopName=Fleming+Way+West'

  page_response = requests.get(page_link, timeout=5)
  # here, we fetch the content from the url, using the requests library
  page_content = BeautifulSoup(page_response.content, "html.parser")

  return page_content


if __name__ == "__main__":
    main()
    # handler()