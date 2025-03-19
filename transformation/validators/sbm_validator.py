import sys
from utils.utils import read_sheet_as_dataframe
import pandas as pd
import mde_wrapper.constants.sbm_constants as sbm_cn
import numpy as np


class SBMValidator:
    def __init__(self, input_xlsx):
        self.input_xlsx = input_xlsx

    def validate_model(self):
        # reading sheets
        df_kennisbronnen = read_sheet_as_dataframe(
            xls_file=self.input_xlsx,
            sheet_name=sbm_cn.KENNISBRONNEN,
            rename_columns=True,
            column_mapping=sbm_cn.KENNISBRONNEN_COLUMN_MAPPING,
        )
        df_begrippen = read_sheet_as_dataframe(
            xls_file=self.input_xlsx,
            sheet_name=sbm_cn.BEGRIPPEN,
            rename_columns=True,
            column_mapping=sbm_cn.BEGRIPPEN_COLUMN_MAPPING,
        )

        # validation per sheet
        self.validate_sheet_algemeen()
        self.validate_sheet(
            df=df_kennisbronnen,
            sheet_name=sbm_cn.KENNISBRONNEN,
            mandatory_columns=sbm_cn.KENNISBRONNEN_MANDATORY_COLUMNS,
            optional_columns=sbm_cn.KENNISBRONNEN_OPTIONAL_COLUMNS,
        )
        self.validate_sheet(
            df=df_begrippen,
            sheet_name=sbm_cn.BEGRIPPEN,
            mandatory_columns=sbm_cn.BEGRIPPEN_MANDATORY_COLUMNS,
            optional_columns=sbm_cn.BEGRIPPEN_OPTIONAL_COLUMNS,
        )

        # reading and validation of "Termvormen"
        if sbm_cn.TERMVORMEN in self.input_xlsx.sheet_names:
            df_termvormen = read_sheet_as_dataframe(
                xls_file=self.input_xlsx,
                sheet_name=sbm_cn.TERMVORMEN,
                rename_columns=True,
                column_mapping=sbm_cn.TERMVORMEN_COLUMN_MAPPING,
            )
            self.validate_sheet(
                df=df_termvormen,
                sheet_name=sbm_cn.TERMVORMEN,
                mandatory_columns=sbm_cn.TERMVORMEN_MANDATORY_COLUMNS,
                optional_columns=sbm_cn.TERMVORMEN_OPTIONAL_COLUMNS,
            )

    def validate_sheet_algemeen(self):
        """Function that reads the sheet "Algemeen" and prints the necessary information from sheet "Algemeen" """
        df = read_sheet_as_dataframe(
            xls_file=self.input_xlsx,
            sheet_name=sbm_cn.ALGEMEEN,
            index_column=0,
            rename_columns=True,
            column_mapping=sbm_cn.ALGEMEEN_COLUMN_MAPPING,
            rename_index=True,
            index_mapping=sbm_cn.ALGEMEEN_FIELD_MAPPING,
        )

        print("\n---------------------------------------------")
        print(f"Validatie resultaten voor tabblad Algemeen:")
        print("---------------------------------------------")
        missing_optional_fields = []
        for mandatory_field in sbm_cn.ALGEMEEN_MANDATORY_FIELDS:
            if mandatory_field.lower() in [field.lower() for field in df.index]:
                print(
                    f"{mandatory_field}: {df.iloc[[field.lower() for field in df.index].index(mandatory_field.lower())][sbm_cn.WAARDEN]}"
                )
            else:
                raise ValueError(
                    f"Verplicht veld [{mandatory_field}] komt niet voor op tabblad Algemeen"
                )

        for optional_field_name in sbm_cn.ALGEMEEN_OPTONAL_FIELDS:
            if optional_field_name.lower() in [field.lower() for field in df.index]:
                print(
                    f"{optional_field_name}: {df.iloc[[field.lower() for field in df.index].index(optional_field_name.lower())][sbm_cn.WAARDEN]}"
                )
            else:
                missing_optional_fields.append(optional_field_name)

        print(
            "---------------------------------------------------------------------------------"
        )
        for missing_optional_field in missing_optional_fields:
            print(
                f"Optioneel veld [{missing_optional_field}] komt niet voor op tabblad Algemeen"
            )

    def validate_sheet(
        self,
        df: pd.DataFrame,
        sheet_name: str,
        mandatory_columns: list,
        optional_columns: list,
    ):
        """Function that prints whether there are missing columns from the respective sheet.

        :param
            df: the respective dataframe
            sheet_name: the respective sheet name
            mandatory_columns: the list containing the column names that have to be in the sheet
            optional_columns: the list containing the columns that are optional in the sheet
        """
        print("\n---------------------------------------------")
        print(f"Validatie resultaten voor tabblad {sheet_name}:")
        print("---------------------------------------------")
        for mandatory_field in mandatory_columns:
            if mandatory_field.lower() not in [field.lower() for field in df.columns]:
                raise ValueError(
                    f"Verplicht veld [{mandatory_field}] komt niet voor op tabblad {sheet_name}"
                )

        for optional_field_name in optional_columns:
            if optional_field_name.lower() not in [
                field.lower() for field in df.columns
            ]:
                print(
                    f"Optioneel veld [{optional_field_name}] komt niet voor op tabblad {sheet_name}"
                )
