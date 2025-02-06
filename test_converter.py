import pytest
from unittest.mock import patch
from main import APIHandler, CurrencyConverter


# Тестирование метода get_rates
class TestAPIHandler:
    @patch("requests.get")
    def test_get_rates_success(self, mock_get):
        """
        Тестирует успешное получение курсов валют через API.
        """
        # Мокируем ответ API
        mock_response = mock_get.return_value
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 75.0},
                "EUR": {"Value": 85.0},
            }
        }
        mock_response.raise_for_status.return_value = None

        api_handler = APIHandler()
        usd_rate, eur_rate = api_handler.get_rates()

        assert usd_rate == 75.0
        assert eur_rate == 85.0

    @patch("requests.get")
    def test_get_rates_failure(self, mock_get):
        """
        Тестирует обработку ошибок при запросе к API.
        """
        # Мокируем ошибку при запросе
        mock_get.side_effect = Exception("API error")

        api_handler = APIHandler()
        usd_rate, eur_rate = api_handler.get_rates()

        assert usd_rate is None
        assert eur_rate is None


# Тестирование метода convert
class TestCurrencyConverter:
    def setup_method(self):
        """
        Создает объект CurrencyConverter с мокированным APIHandler.
        """
        self.api_handler = APIHandler()
        self.converter = CurrencyConverter(self.api_handler)

    @patch.object(APIHandler, "get_rates")
    def test_convert_usd(self, mock_get_rates):
        """
        Тестирует конвертацию рублей в USD.
        """
        mock_get_rates.return_value = (75.0, 85.0)  # Мокируем курсы валют

        result = self.converter.convert(150, "USD")
        assert result == "2.00 USD"

    @patch.object(APIHandler, "get_rates")
    def test_convert_eur(self, mock_get_rates):
        """
        Тестирует конвертацию рублей в EUR.
        """
        mock_get_rates.return_value = (75.0, 85.0)  # Мокируем курсы валют

        result = self.converter.convert(170, "EUR")
        assert result == "2.00 EUR"

    @patch.object(APIHandler, "get_rates")
    def test_convert_cny(self, mock_get_rates):
        """
        Тестирует конвертацию рублей в CNY.
        """
        mock_get_rates.return_value = (75.0, 85.0)  # Мокируем курсы валют
        result = self.converter.convert(10 * (85.0 / 7.5), "CNY")  # Пересчитываем входные данные
        assert result == "10.00 CNY"

    @patch.object(APIHandler, "get_rates")
    def test_convert_invalid_currency(self, mock_get_rates):
        """
        Тестирует обработку некорректной валюты.
        """
        mock_get_rates.return_value = (75.0, 85.0)  # Мокируем курсы валют

        result = self.converter.convert(100, "GBP")
        assert result is None

    @patch.object(APIHandler, "get_rates")
    def test_convert_api_failure(self, mock_get_rates):
        """
        Тестирует обработку ошибки при получении курсов валют.
        """
        mock_get_rates.return_value = (None, None)  # Мокируем ошибку API

        result = self.converter.convert(100, "USD")
        assert result is None
