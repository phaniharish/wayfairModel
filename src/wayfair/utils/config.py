import os
from pathlib import Path


class ConfigHelper:
    def __init__(self):
        self.__content_root = None

    @property
    def content_root(self) -> Path:
        if not self.__content_root:
            self.__content_root = Path(__file__).parent.parent.parent.parent
        return self.__content_root

    @content_root.setter
    def content_root(self, value: Path):
        self.__content_root = value

    @property
    def nginx_config_file(self) -> Path:
        return self.content_root.joinpath('conf/nginx.conf')

    @property
    def model_server_workers(self) -> int:
        return int(os.environ.get('MODEL_SERVER_WORKERS', 1))

    @property
    def service_url(self) -> str:
        return 'http://127.0.0.1:{}/invocations'.format(self.service_port)

    @property
    def ping_url(self) -> str:
        return 'http://127.0.0.1:{}/ping'.format(self.service_port)

    @property
    def service_port(self) -> int:
        return int(os.environ.get('MODEL_SERVER_PORT', 8080))

    @property
    def model_server_timeout(self) -> int:
        return os.environ.get('MODEL_SERVER_TIMEOUT', 60)

    @property
    def order_data_path(self) -> Path:
        return self.content_root.joinpath('data/orders.csv')

    @property
    def payments_data_path(self) -> Path:
        return self.content_root.joinpath('data/payments.csv')

    @property
    def zipcode_data_path(self) -> Path:
        return self.content_root.joinpath('data/zip_codes.csv')

    @property
    def inventory_data_path(self) -> Path:
        return self.content_root.joinpath('data/inventory.csv')

    @property
    def features_data_path(self) -> Path:
        return self.content_root.joinpath('data/features.csv')

    @property
    def result_data_path(self) -> Path:
        return self.content_root.joinpath('results/results.json')

    @property
    def default_time_column(self):
        return "timestamp"

    @property
    def zipcode_time_column(self):
        return "available_from"

    @property
    def app_name(self):
        return "WayfairService"


config = ConfigHelper()
