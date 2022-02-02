from doctest import DocTestFailure
import urllib.parse as pars

string = "https://accounts.google.com/ServiceLogin?continue=https://www.google.com/search%3Fq%3Dpython%2Bfor%2Bbeginners%26lr%3Dlang_en%26hl%3Den%26cr%3DUS&hl=en"
fix_string = pars.unquote(string)

print(fix_string)
