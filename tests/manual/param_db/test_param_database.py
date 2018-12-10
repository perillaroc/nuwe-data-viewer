# coding: utf-8
from nuwe_data_viewer.plugin.grib_tool.param_db.grib2_table_database import Grib2TableDatabase


def main():
    db = Grib2TableDatabase()
    db.read_definition()
    print(db)


if __name__ == "__main__":
    main()