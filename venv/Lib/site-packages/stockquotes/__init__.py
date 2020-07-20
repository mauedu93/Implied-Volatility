#!/usr/bin/env python3
# stockquotes - Python module to pull stock quotes from Yahoo! Finance
# Copyright 2020 ScoopGracie. All rights reversed.
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from bs4 import BeautifulSoup as bs
import requests
import datetime


class StockDoesNotExistError(Exception):
    pass


class NetworkError(Exception):
    pass


class Stock:
    def __init__(self, ticker):
        try:
            r = requests.get(
                "https://finance.yahoo.com/quote/{}/history".format(ticker),
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36"
                },
            )
        except:
            raise NetworkError()
        if r.status_code is 302:
            raise StockDoesNotExistError(ticker)
        try:
            soup = bs(r.text, features="lxml")
            self.symbol = soup.h1.string.split("(")[1].split(")")[0]
            self.name = soup.h1.string.split("(")[0].strip()
            rows = soup.table.tbody.find_all("tr")
            self.historical = []
            for i in rows:
                row = i.find_all("td")
                try:
                    parsed = {
                        "date": datetime.datetime.strptime(
                            row[0].span.string, "%b %d, %Y"
                        ),
                        "open": float(row[1].span.string.replace(",", "")),
                        "high": float(row[2].span.string.replace(",", "")),
                        "low": float(row[3].span.string.replace(",", "")),
                        "close": float(row[4].span.string.replace(",", "")),
                        "adjusted_close": float(
                            row[5].span.string.replace(",", "")
                        ),
                        "volume": int(row[6].span.string.replace(",", "")),
                    }
                except:
                    continue

                self.historical.append(parsed)
            top_data = soup.find(id="quote-header-info")
            try:
                self.current_price = float(
                    top_data.findAll("span")[11].string.replace(",", "")
                )
                raw_change = top_data.findAll("span")[12].string
            except IndexError:
                self.current_price = float(
                    top_data.findAll("span")[3].string.replace(",", "")
                )
                raw_change = top_data.findAll("span")[4].string

            self.increase_dollars = float(
                raw_change.split(" ")[0].replace(",", "")
            )
            self.increase_percent = float(
                raw_change.split(" ")[1]
                .replace(",", "")
                .replace("(", "")
                .replace(")", "")
                .replace("%", "")
            )
        except AttributeError as error:
            raise StockDoesNotExistError(ticker) from error
