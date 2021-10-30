# easy_fossy
my own version of foss api

Requires python 3.10
as it uses latest structural matching case patterms
and a
config.ini file with below contents is essential & effortless kickstart
```
[test]
url = http://fossology-test.com:8080/repo/api/v1/
uname = 
pwd = 
access = write
bearer_token = Bearer OHNSUFaI6OtoFNz
token_valdity_days = 365
token_expire = 2022-10-29
reports_location = reports/
group_name = fossy

[prod]
url = http://fossology.com:8081/repo/api/v1/
uname = fossy
pwd = fossy
access = write
token_valdity_days = 365
group_name = fossy
```
### License: MIT
```
MIT License

Copyright (c) 2021 Dinesh Ravi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
