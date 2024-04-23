import pickle
import numpy as np

import firebase_admin
from firebase_admin import credentials, db

from metpy.calc import heat_index
from metpy.units import units


from fastapi import FastAPI,HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from datetime import datetime

# ct = datetime.today().strftime('%Y-%m-%d')
# print("current time:-", ct)



# cred = credentials.Certificate("test-firebase-4d32f-firebase-adminsdk-bmap1-14267c8781.json")
cred = credentials.Certificate("/app/test-firebase-4d32f-firebase-adminsdk-bmap1-14267c8781.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://test-firebase-4d32f-default-rtdb.firebaseio.com/Test/ProjectMMicroClimate/2024-01-21%2018%3A00%3A00'})

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")



origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

def calculate_heat_indices(tc, rh, indoor_temp, indoor_rh):
    temp_outdoor = tc * units.degC
    rel_hum_outdoor = rh / 100
    heat_outdoor = heat_index(temp_outdoor, rel_hum_outdoor, mask_undefined=False)
    outdoor_heat_index = round(float(np.squeeze(heat_outdoor.to(units.degC).magnitude)), 2)

    temp_indoor = indoor_temp * units.degC
    rel_hum_indoor = indoor_rh / 100
    heat_indoor = heat_index(temp_indoor, rel_hum_indoor, mask_undefined=False)
    indoor_heat_index = round(float(np.squeeze(heat_indoor.to(units.degC).magnitude)), 2)

    print(f'Outdoor Heat Index = {outdoor_heat_index}')
    print(f'Indoor Heat Index = {indoor_heat_index}')

    return outdoor_heat_index, indoor_heat_index


async def call_tmd_api():
    try:
        # api_url = "https://data.tmd.go.th/nwpapi/v1/forecast/location/hourly/at?lat=8.641690250193232&lon=99.89738919432612&fields=tc,rh&date={}&minute=5".format(ct)
        # api_url = "https://data.tmd.go.th/nwpapi/v1/forecast/location/hourly/at?lat=8.641690250193232&lon=99.89738919432612&fields=tc,rh&date=2024-03-05&minute=5"
        # headers = {
        #     'accept': 'application/json',
        #     'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImUxZjQzZmVmMmEzNmFmNzRkYmViNDVmYmFiMmUyZjk5YTBmN2E1NzA5M2FmNGYwZDk5NTQ3ZWE0OTk0YTZlZTg0MzBhOGZlZTBjZTE4N2M2In0.eyJhdWQiOiIyIiwianRpIjoiZTFmNDNmZWYyYTM2YWY3NGRiZWI0NWZiYWIyZTJmOTlhMGY3YTU3MDkzYWY0ZjBkOTk1NDdlYTQ5OTRhNmVlODQzMGE4ZmVlMGNlMTg3YzYiLCJpYXQiOjE3MDk4ODgxNzEsIm5iZiI6MTcwOTg4ODE3MSwiZXhwIjoxNzQxNDI0MTcxLCJzdWIiOiIyNjUzIiwic2NvcGVzIjpbXX0.JjFo2Fcnv-uyVsq0gfG7jE3y7624jDWHFdmxEZZMb7yfu0UwZ9w33PY3rHqzE0ziuFk2PQwhTiMcShx7UddTnw10x_yJuSnzyP7ujRv5yo38fJqv3ESGjhR_3i5gyFcTkwor2XjxpwF00q-yTJEk8hqwmwaD8XOpDsGgR95_AkBeTbR1ZutTX5SAUVcCriZGE1pgYPtUrptxe2O7qwD3F-ZZPGqwHbTPweCenLMO6EKk9o8c5U41Kj9mGrJ1rFL_ni6uFOuRz9gj3XNtqPayUUsG5bHIBoOENGTCLQz4T8lMWBwMvMG6TqOnJzEj0HLyjTS5m9trJvENr5D6q1blw8eO_OO0Kly4l_nXNIIW3QP9roRFinGukJfjUPBye1RL7I_yUyTGrsUoIC-mqvvKufO3XQht_ZHtAmXYT_KJqQVbhws91wfUDe2g8r8ELJ9INqlfgakgRTMuYlK6Z5Lj1erJFoVVx6odBhdd1pHHSkMHLf4tTXFBpom47X9Vxx_CeXi7lm5BY9JmESj8DcLEPufBimRAJv1yBnXtsEV2z-9_rRpLiW1d-L0_OS7i9SteFooxyaGA7keOGehh5-Zq-q6ghY-nNq6DLYALUNKnCs0T9C1oL18l2zYFIcFa3WMGt7BNjkDoSxMbqKTs2mBICbVbBAoKX0Xr3Zku2ibSwyo',
        # }

        # async with httpx.AsyncClient() as client:
        #     response = await client.get(api_url, headers=headers)
        #     if response.status_code == 200:
        #         print(response.status_code)
        #         api_data = response.json()
        #         rh, tc = api_data["WeatherForecasts"][0]["forecasts"][0]["data"]["rh"], api_data["WeatherForecasts"][0]["forecasts"][0]["data"]["tc"]
        #         print('Out Humid',rh)
        #         print('Out Temp',tc)

        combined_data = {}
        
        firebase_data = db.reference("/Test/ProjectMMicroClimate").get()
        last_key = list(firebase_data.keys())[-1]

        last_key_ref = db.reference("/Test/ProjectMMicroClimate/" + last_key)
        last_key_data = last_key_ref.get()

        combined_data.update(last_key_data)

        timestamp_data = db.reference("/Test/ProjectMMicroClimate").get()
        latest_timestamp = max(timestamp_data.keys())
        print("Latest timestamp:", latest_timestamp)




        door, window, AC, curtain = 0, 0, 1, 0
        collect = np.array(list(combined_data.values()))
        data = [float(string) for string in collect]
        print(data[0], data[1], door, window, AC, curtain)

        # outdoor_heat_index, indoor_heat_index = calculate_heat_indices(tc, rh, data[1], data[0])
        outdoor_heat_index, indoor_heat_index = calculate_heat_indices(30.89, 57.85, data[1], data[0]) #ใช้ข้อมูลของวันที่ 12/03/2024 เวลา 12.00

        ref_point = 9
        grid_list = [1, 2, 3, 4, 5, 6, 7, 8]
        predictions = {}
        for num in grid_list:
            filename = f"/app/Model/Grid{ref_point}-{num}/[Grid{ref_point}-{num}]knn_model.sav"
            # filename = f"C://Users//NITRO V15//Downloads//TestMicroClimateProject//Model//Grid{ref_point}-{num}/[Grid{ref_point}-{num}]knn_model.sav"

            svr = pickle.load(open(filename, 'rb'))
            x = [[indoor_heat_index, outdoor_heat_index, window, curtain, AC, door, ]]
            y = svr.predict(x)
            rounded_y = round(float(y), 2)
            predictions[f'Grid{ref_point}to{num}'] = rounded_y
            print(f'Grid {ref_point} Predicted {num} = {y}')

        result_dict = {
            'Timestamp': latest_timestamp,
            'GridRef': indoor_heat_index,
            'Grid9to1': predictions['Grid9to1'],
            'Grid9to2': predictions['Grid9to2'],
            'Grid9to3': predictions['Grid9to3'],
            'Grid9to4': predictions['Grid9to4'],
            'Grid9to5': predictions['Grid9to5'],
            'Grid9to6': predictions['Grid9to6'],
            'Grid9to7': predictions['Grid9to7'],
            'Grid9to8': predictions['Grid9to8'],
        }

        return result_dict
    # else:
    #     raise HTTPException(status_code=response.status_code, detail=f"API Error: {response.status_code}")
    except Exception as e:
            print(e)

@app.get("/predict")
async def predict():
    return await call_tmd_api()

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )









