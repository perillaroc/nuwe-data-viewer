# coding: utf-8
from nuwe_data_viewer.plugin.grib_tool.param_db.parameter_database import ParameterDatabase


def main():
    db = ParameterDatabase.create_from_definition()
    print(db)


if __name__ == "__main__":
    main()