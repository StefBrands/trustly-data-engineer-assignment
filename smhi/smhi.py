import argparse
import requests

from tqdm import tqdm


class SmhiParser:
    """
    Class to handle communication with and extract data from the SMHI Open API.
    """
    BASE_URL = "https://opendata-download-metobs.smhi.se/api/version/1.0"

    def __init__(self, suffix=".json"):
        self.suffix = suffix

    def _make_request(self, path=""):
        r = requests.get(self.BASE_URL+path+self.suffix)
        return r

    def check_connection(self):
        r = self._make_request()
        return r.status_code

    
    def list_parameters(self):
        """Calls the parameter endpoint to list all available parameters."""
        r = self._make_request(path="/parameter").json()
        parameters = sorted(r['resource'], key=lambda d: int(d['key']))
        for parameter in parameters:
            print(f"{parameter['key']}, {parameter['title']} ({parameter['summary']})")

    def temperatures(self):
        """Return print out of stations with highest and lowest tempertaure.
        
        Note: because there is no available StationSet for this parameter we have to call all stations seperatedly."""
        r = self._make_request(path="/parameter/2").json()
        stations = r['station']
        station_keys = [station['key'] for station in stations]
        stations_with_temperatures = []
        for station in tqdm(station_keys[0:50]): # Sliced to spare the SMHI API while developing.
            try:
                r = self._make_request(path=f"/parameter/2/station/{station}/period/latest-day/data").json()
                stations_with_temperatures.append({'station': r['station']['name'], 'value': r['value'][0]['value']})
            except:
                pass
        station_max_temp = max(stations_with_temperatures, key=lambda x:float(x['value']))
        station_min_temp = min(stations_with_temperatures, key=lambda x:float(x['value']))

        print(f"Highest temperature: {station_max_temp['station']}, {station_max_temp['value']} degrees")
        print(f"Lowest temperature: {station_min_temp['station']}, {station_min_temp['value']} degrees")



def main():
    parser = argparse.ArgumentParser(
        description="""Script to extract data from SMHI's Open API"""
    )
    parser.add_argument("--check-connection", action="store_true", help="Check connection to SMHI API")
    parser.add_argument("--parameters", action="store_true", help="List SMHI API parameters")
    parser.add_argument("--temperatures", action="store_true", help="Show stations with the highest and lowest temperature")
    args = parser.parse_args()

    smhi_parser = SmhiParser()

    if args.check_connection:
        status_code = smhi_parser.check_connection()
        print(status_code)
    elif args.parameters:
        smhi_parser.list_parameters()
    elif args.temperatures:
        smhi_parser.temperatures()


if __name__ == "__main__":
    main()


