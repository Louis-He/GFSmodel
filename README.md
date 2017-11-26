# GFSmodel
This program is used to download the latest GFS weather model prediction grib2 files and plot weather graphs to help weather forecasters to better analyze the current and future weather.

## Credit and Warning
Credit @MYYD and @Louis-He

This project and program **CANNOT** be distributed or modified by **ANYONE** or **ANY ORGANIZATION** **WITHOUT** the permission of the developer.

## Dependence
This program needs packages as follows:numpy, pygrib(with packages pygrib needs), matplotlib, basemap

## Before Running
1. Clone the whole GFSmodel folder
2. Create folder 'sysreport' under ./GFSmodel
3. Create folder 'product' under ./GFSmodel
4. Create folder 'WTP' under ./GFSmodel/product
5. Create folder 'RAIN' under ./GFSmodel/product
6. Create folder 'WGP' under ./GFSmodel/product

Run in bash before running the program:
```
cd ./GFSmodel
mkdir sysreport
mkdir product
cd product
mkdir WTP
mkdir RAIN
mkdir WGP
```
## Running program
python3 main.py

This is the only thing you need to do to run the whole program. The program will help you download the latest GFS files automatically. However, when you run the program, the system will download the latest file when the future GFS file is avalible. It will draw 10m-wind, 2m-temperature, Mean-sea-level-pressure/ 850m-wind, 850hpa-temperature, 500-hpa-geopotential-height/ 6-hour-accumulated-precipitation(rain/snow/sleet_freezing-rain_mixed) automatically to product/WTP, product/WGP, product/RAIN, respectively.

## Future improvement
1. More plots
2. Add Himawari-8 satellite images
3. Add China ground environment monitoring station network **See [Airchina](https://github.com/Louis-He/airchina) repository**
