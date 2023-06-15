import json as json
from json import loads

def detect(array):
    detect_array = []
    for a in array:
        cX = (a[0]+a[2])/2
        cY = (a[1]+a[3])/2
        detect_array.append([cX, cY, a[4], a[5]])
    return detect_array

def detectOP(array):
    detect_array = []
    for a in array:
        cX = (a[0]+a[2])/2
        cY = (a[1]+a[3])/2
        width = (a[2] - a[0])
        height = (a[3] - a[1])
        detect_array.append([a[0], a[1], width, height, a[4], a[5]])
    return detect_array

labelsOP = [
"Hoek",
"Bord",
"Gebied"
]

labels = [
"1",
"2",
"3",
"4",
"5",
"0",
"%1000",
"mL",
"cm3",
"m3",
"L",
"x1000",
"00",
"000",
"6",
"%10",
"km",
"hm",
"dam",
"m",
"dm",
"x10",
"cm",
"mm",
"%100",
"9",
"comma",
"8",
"x100",
"km2",
"hm2",
"dam2",
"m2",
"dm2",
"mm2",
"cm2",
"7",
"dm3",
"dL",
"cL"]

token_id_list = """{
  "numbers": [
    { "name": "1" },
    { "name": "2" },
    { "name": "3" },
    { "name": "4" },
    { "name": "5" },
    { "name": "6" },
    { "name": "7" },
    { "name": "8" },
    { "name": "9" },
    { "name": "0" },
    { "name": "00" },
    { "name": "000" },
    { "name": "comma" }
  ],
  "multipliers": [
    { "name": "x10" },
    { "name": "%10" },
    { "name": "x100" },
    { "name": "%100" },
    { "name": "x1000" },
    { "name": "%1000" }
  ],
  "length": [
    { "name": "mm" },
    { "name": "cm" },
    { "name": "dm" },
    { "name": "m" },
    { "name": "dam" },
    { "name": "hm" },
    { "name": "km" }
  ],
  "area": [
    { "name": "mm2" },
    { "name": "cm2" },
    { "name": "dm2" },
    { "name": "m2" },
    { "name": "dam2" },
    { "name": "hm2" },
    { "name": "km2" }
  ],
  "volume": [
    { "name": "cm3" },
    { "name": "dm3" },
    { "name": "m3" },
    { "name": "mL" },
    { "name": "cL" },
    { "name": "dL" },
    { "name": "L" }
  ]
}"""

tokens = json.loads(token_id_list)
numbers = tokens.get("numbers")
multi = tokens.get("multipliers")
length = tokens.get("length")
area = tokens.get("area")
volume = tokens.get("volume")
