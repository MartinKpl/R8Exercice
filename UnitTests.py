import unittest
from unittest.mock import patch, MagicMock
from weather import (
    get_city_coordinates, get_weather_data,
    parse_weather_data, process_city_weather
)

class TestWeatherFunctions(unittest.TestCase):
    @patch('weather.requests.get')
    def test_get_city_coordinates_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"lat": "59.4372155", "lon": "24.7453688"}]
        mock_get.return_value = mock_response

        coords = get_city_coordinates("Tallinn")
        self.assertEqual(coords, ("59.4372155", "24.7453688"))

    @patch('weather.requests.get')
    def test_get_city_coordinates_no_data(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        coords = get_city_coordinates("Tallinn")
        self.assertIsNone(coords)

    @patch('weather.requests.get')
    def test_get_city_coordinates_error_status(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        coords = get_city_coordinates("Tallinn")
        self.assertIsNone(coords)

    @patch('weather.requests.get')
    def test_get_weather_data_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"test": "data"}
        mock_get.return_value = mock_response

        data = get_weather_data(("59.4372155", "24.7453688"))
        self.assertEqual(data, {"test": "data"})

    def test_get_weather_data_invalid_coordinates(self):
        data = get_weather_data((None, None))
        self.assertIsNone(data)

    @patch('weather.requests.get')
    def test_get_weather_data_error_status(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_get.return_value = mock_response

        data = get_weather_data(("59.4372155", "24.7453688"))
        self.assertIsNone(data)

    def test_parse_weather_data(self):
        details = {
            "air_temperature": 20,
            "relative_humidity": 50,
            "wind_speed": 5
        }
        result = parse_weather_data("tallinn", details, "partlycloudy_day")
        self.assertEqual(result, [
            "Tallinn",
            "20°C / 68.00°F",
            "Partlycloudy day",
            "50%",
            "5 m/s"
        ])

    @patch('weather.get_city_coordinates')
    @patch('weather.get_weather_data')
    def test_process_city_weather_success(self, mock_weather, mock_coords):
        mock_coords.return_value = ("59.4372155", "24.7453688")
        mock_weather.return_value = {
            "properties": {
                "timeseries": [
                    {
                        "data": {
                            "instant": {
                                "details": {
                                    "air_temperature": 22,
                                    "relative_humidity": 60,
                                    "wind_speed": 3
                                }
                            },
                            "next_1_hours": {
                                "summary": {
                                    "symbol_code": "clear_sky"
                                }
                            }
                        }
                    }
                ]
            }
        }
        result = process_city_weather("tallinn")
        self.assertEqual(result, [
            "Tallinn",
            "22°C / 71.60°F",
            "Clear sky",
            "60%",
            "3 m/s"
        ])

    @patch('weather.get_city_coordinates')
    def test_process_city_weather_no_coordinates(self, mock_coords):
        mock_coords.return_value = None
        result = process_city_weather("Nonexistent City")
        self.assertIsNone(result)

    @patch('weather.get_city_coordinates')
    @patch('weather.get_weather_data')
    def test_process_city_weather_no_weather_data(self, mock_weather, mock_coords):
        mock_coords.return_value = ("59.4372155", "24.7453688")
        mock_weather.return_value = None
        result = process_city_weather("Tallinn")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
