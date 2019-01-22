import pandas as pd

def saveXLSX(df, filename, sheet_name='Sheet1', index=False, verbose=True):
    """ Save a .xlsx file.
    Params
    ------

    df : DataFrame
      Data frames to be saved in the file.

    filename : str
      Full path and filename with extension .xlsx included.

    sheet_name : str
      Label of the sheet to saved in the excel file.

    index : bool
      Indicates if the index columns is included or not.
    """

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name=sheet_name, index=index)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

    if verbose:
        print("Writing xlsx file: {}.".format(filename))

