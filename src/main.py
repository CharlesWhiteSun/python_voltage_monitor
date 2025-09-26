from services.voltage_service import VoltageService
from utils.config_enum import ConfigName
from utils.config_loader import load_config


def main(reader_class):
    plc_config = load_config(name=ConfigName.PLC)
    print(f"Loaded PLC config: {plc_config}")

    reader = reader_class()  
    service = VoltageService(reader)

    voltage = service.get_voltage(220.5, 221.0, 219.8)
    print("Voltage reading:", voltage)


if __name__ == "__main__":
    from readers.plc_reader import PLCVoltageReader
    main(PLCVoltageReader)
