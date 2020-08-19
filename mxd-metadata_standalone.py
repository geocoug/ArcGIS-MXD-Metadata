# PURPOSE
#   Scan MXD for layer descriptions and place output in CSV.
#
# OUTPUT
#   CSV with the following columns:
    ##    Data_Frame
    ##    Layer_Basename
    ##    Layer_Type
    ##    File_Extension
    ##    Layer_Catalog_Path
    ##    Layer_DefinitionQuery_Supported
    ##    Layer_DefinitionQuery
    ##    Field_Names
    ##    Feature_Type
    ##    Shape_Type
    ##    Has_Z'
    ##    Has_Spatial_Index
    ##    Layer_File
    ##    Layer_Path
    ##    Coordinate_Type
    ##    GCS_Name
    ##    GCS_Code
    ##    PCS_Name
    ##    PCS_Code
    ##    Linear_Unit_Name
    ##    Linear_Unit_Code
    ##    Datum_Name
    ##    Datum_Code
    ##    Spheroid_Name
    ##    Spheroid_Code
    ##    Layer_Description
    ##    Raster_Format
    ##    Raster_Band_Count
    ##    Raster_Compression_Type
    ##    Raster_Size_MB
    ##    Raster_Cell_Width
    ##    Raster_Cell_Height
    ##    Raster_Cell_Min
    ##    Raster_Cell_Max
    ##    Raster_Cell_Mean
    ##    Raster_Extent_JSON
#
# AUTHOR(S)
#   Caleb Grant, Integral Consulting, Inc. (CG)
#
# NOTES
#   1) This script takes 1 argument and 1 optional argument
#       - MXD path
#       - *Output CSV directory
#
# HISTORY
#   Date                Revision
#   ---------------     ----------------------------------------------------------
#   2020-06-26          Created. CG.
#   2020-07-22          Updated conditional check for object attributes (if they exist). CG.
#                       Added multiple new layer attributes to output. CG.
#                       Output sorted by first column in csv (Layer_Name). CG.
#
# ISSUES
#   - Nested layer groups where > 6 nested groups are present
#   - Layers pulled in through a connection
# =========================================================================

import sys
import os
import csv
import datetime
import getpass
import time
from colorama import init, Fore, Style

init(autoreset=True)

OS_USER = getpass.getuser()
USER = ''.join([i for i in OS_USER if not i.isdigit()])
RUN_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %p")

def CLI():
    def CLI_Help():
        print(Style.BRIGHT + Fore.BLUE + '\n========================================================================================')
        print(Style.BRIGHT + Fore.GREEN + '    HELP - ArcGIS MXD metadata compiler')
        print(Style.BRIGHT + Fore.BLUE + '========================================================================================')
        print(Style.BRIGHT + Fore.CYAN + "Usage" + Fore.WHITE + "  python <python_script_path> <mxd_path> <output_csv_path>")
        print(Style.BRIGHT + Fore.CYAN + "   or" + Fore.WHITE + "  python <python_script_path> <mxd_path>\n")
        print(Style.BRIGHT + Fore.CYAN + "Arguments")
        print(Style.BRIGHT + Fore.WHITE + "    python_script_path:  Path to python script. No UNC allowed.")
        print(Style.BRIGHT + Fore.WHITE + '                             Surround path in double quotes ("<path>") if spaces in path.')
        print(Style.BRIGHT + Fore.WHITE + "    mxd_path:            Path to .mxd file. No UNC allowed.")
        print(Style.BRIGHT + Fore.WHITE + '                             Surround path in double quotes ("<path>") if spaces in path.')
        print(Style.BRIGHT + Fore.WHITE + "    output_csv_path:     Path of desired output CSV. No UNC allowed.")
        print(Style.BRIGHT + Fore.WHITE + "                             Only include directory, no file name needed.")
        print(Style.BRIGHT + Fore.WHITE + "                             DEFAULT: H:\ \n")
        print(Style.BRIGHT + Fore.CYAN + "Options:")
        print(Style.BRIGHT + Fore.WHITE + "    -h  : Show this help message and exit\n")
        print(Style.BRIGHT + Fore.CYAN + "Known Issues:")
        print(Style.BRIGHT + Fore.WHITE + "    - Layer groups that are > 6 nested groups deep are not accounted for.\n")
        print(Style.BRIGHT + Fore.CYAN + "Author(s):")
        print(Style.BRIGHT + Fore.WHITE + "    Caleb Grant, Integral Consulting, Inc.")
        print(Style.BRIGHT + Fore.BLUE + '========================================================================================')
        sys.exit()

    def validate_mxd():
        try:
            if os.path.splitext(args[1])[1] == '.mxd':
                if os.path.exists(args[1]):
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

    def validate_csv():
        try:
            if os.path.exists(args[2]):
                return True
            else:
                return False
        except:
            return False

    args = sys.argv
    arg_count = len(args)
    if len(args) == 2 and args[1] == '-h':
        CLI_Help()

    if len(args) < 2:
        print(Style.BRIGHT + Fore.YELLOW + '\nWARNING: No arguments provided')
        CLI_Help()
    elif len(args) == 2:
        valid_mxd = validate_mxd()
        if valid_mxd == True:
            return
        else:
            print(Style.BRIGHT + Fore.RED + '\nERROR: Invalid MXD path')
            CLI_Help()
    elif len(args) == 3:
        valid_mxd = validate_mxd()
        valid_csv = validate_csv()
        if valid_mxd == True and valid_csv == True:
            return
        elif valid_mxd == False and valid_csv == True:
            print(Style.BRIGHT + Fore.RED + '\nERROR: Invalid MXD path')
            CLI_Help()
        elif valid_mxd == True and valid_csv == False:
            print(Style.BRIGHT + Fore.RED + '\nERROR: Invalid output CSV path')
            CLI_Help()
        else:
            print(Style.BRIGHT + Fore.RED + '\nERROR: Invalid MXD path and invalid output CSV path')
            CLI_Help()
    else:
        print(Style.BRIGHT + Fore.RED + "\nERROR: Too many arguments provided.")
        print(Style.BRIGHT + Fore.RED + "Only 3 arguments allowed")
        print(Style.BRIGHT + Fore.RED + "  *Unknown arguments: " + Fore.WHITE + "{}\n\n".format(args[3:]))
        CLI_Help()


def mainFunction(mxd):
    def lyrDescriptions(l):
        try:
            desc = arcpy.Describe(l)
        except:
            try:
                meta.update({str(l.name): {
                    'Data_Frame': frame.name,
                    'Layer_Basename': '',
                    'Layer_Type': '',
                    'File_Extension': '',
                    'Layer_Catalog_Path': '',
                    'Layer_DefinitionQuery_Supported': '',
                    'Layer_DefinitionQuery': '',
                    'Field_Names': '',
                    'Feature_Type': '',
                    'Shape_Type': '',
                    'Has_Z': '',
                    'Has_Spatial_Index': '',
                    'Layer_File': '',
                    'Layer_Path': '',
                    'Coordinate_Type': '',
                    'GCS_Name': '',
                    'GCS_Code': '',
                    'PCS_Name': '',
                    'PCS_Code': '',
                    'Linear_Unit_Name': '',
                    'Linear_Unit_Code': '',
                    'Datum_Name': '',
                    'Datum_Code': '',
                    'Spheroid_Name': '',
                    'Spheroid_Code': '',
                    'Layer_Description': '',
                    'Raster_Format': '',
                    'Raster_Band_Count': '',
                    'Raster_Compression_Type': '',
                    'Raster_Size_MB': '',
                    'Raster_Cell_Width': '',
                    'Raster_Cell_Height': '',
                    'Raster_Cell_Min': '',
                    'Raster_Cell_Max': '',
                    'Raster_Cell_Mean': '',
                    'Raster_Extent_JSON': ''
                    }
                })
                return
            except:
                return
            return


        if hasattr(desc, 'fieldInfo'):
            field_info = desc.fieldInfo
            fieldNames = [str(field_info.getFieldName(index)) for index in range(0, field_info.count)]
            fieldNameStr = ""
            for field in fieldNames:
                if field == fieldNames[-1]:
                    fieldNameStr = fieldNameStr + field
                else:
                    fieldNameStr = fieldNameStr + "{};".format(field)
        else:
            fieldNameStr = ""

        if hasattr(desc, 'featureType'):
            feature_type = desc.featureType
        else:
            feature_type = ""

        if hasattr(desc, 'shapeType'):
            shape_type = desc.shapeType
        else:
            shape_type = ""

        if hasattr(desc, 'hasZ'):
            has_z = desc.hasZ
        else:
            has_z = False

        if hasattr(desc, 'hasSpatialIndex'):
            has_spat_index = desc.hasSpatialIndex
        else:
            has_spat_index = False

        try:
            lyr_name = l.longName
        except:
            lyr_name = desc.nameString

        if hasattr(desc, 'file'):
            lyr_file = desc.file
        else:
            lyr_file = ""

        if hasattr(desc, 'path'):
            lyr_path = desc.path
        else:
            lyr_path = ""

        if hasattr(desc, 'extension'):
            lyr_extension = desc.extension
            if lyr_extension == "":
                lyr_extension = 'gdb'
        else:
            lyr_extension = ""

        if hasattr(desc, 'dataType'):
            lyr_dtype = desc.dataType
        else:
            lyr_dtype = ""

        if hasattr(desc, 'baseName'):
            lyr_basename = desc.baseName
        else:
            lyr_basename = ""

        if hasattr(desc, 'catalogPath'):
            lyr_catpath = desc.catalogPath
        else:
            lyr_catpath = ""

        if lyr.supports("DEFINITIONQUERY"):
            lyrDefSupport = True
            if lyr.definitionQuery == '':
                lyrDef = ''
            else:
                lyrDef = str(lyr.definitionQuery)
        else:
            lyrDefSupport = False
            lyrDef = ''

        if hasattr(desc, 'description'):
            lyr_description = lyr.description
        else:
            lyr_description = ""

        try:
            lyr_coordType = desc.spatialReference.type
        except:
            lyr_coordType = ""

        try:
            lyr_GCSName = desc.spatialReference.GCSName
            if lyr_GCSName == "":
                lyr_GCSCode = ""
            else:
                lyr_GCSCode = desc.spatialReference.GCSCode
        except:
            lyr_GCSName = ""
            lyr_GCSCode = ""

        try:
            lyr_PCSName = desc.spatialReference.PCSName
            if lyr_PCSName == "":
                lyr_PCSCode = ""
            else:
                lyr_PCSCode = desc.spatialReference.PCSCode
        except:
            lyr_PCSName = ""
            lyr_PCSCode = ""

        try:
            lyr_datumName = desc.spatialReference.datumName
            if lyr_datumName == "":
                lyr_datumCode = ""
            else:
                lyr_datumCode = desc.spatialReference.datumCode
        except:
            lyr_datumName = ""
            lyr_datumCode = ""

        try:
            lyr_spheroidName = desc.spatialReference.spheroidName
            if lyr_spheroidName == "":
                lyr_spheroidCode = ""
            else:
                lyr_spheroidCode = desc.spatialReference.spheroidCode
        except:
            lyr_spheroidName = ""
            lyr_spheroidCode = ""

        try:
            lyr_coord_unit = desc.spatialReference.linearUnitName
            if lyr_coord_unit == "":
                lyr_coord_unit_code = ""
            else:
                lyr_coord_unit_code = desc.spatialReference.linearUnitCode
        except:
            lyr_coord_unit = ""
            lyr_coord_unit_code = ""

        if l.isRasterLayer:
            raster = arcpy.Raster(lyr_catpath)
            try:
                raster_format = raster.format
            except:
                raster_format = ""

            try:
                raster_bands = raster.bandCount
            except:
                raster_bannds = ""

            try:
                raster_compression = raster.compressionType
            except:
                raster_compression = ""

            try:
                raster_size = float(raster.uncompressedSize) / 1000000 # Byte --> Megabyte
            except:
                raster_size = ""

            try:
                raster_cell_width = raster.meanCellWidth
            except:
                raster_cell_width = ""

            try:
                raster_cell_height = raster.meanCellHeight
            except:
                raster_cell_height = ""

            try:
                raster_cell_min = raster.minimum
            except:
                raster_cell_min = ""

            try:
                raster_cell_max = raster.maximum
            except:
                raster_cell_max = ""

            try:
                raster_cell_mean = raster.mean
            except:
                raster_cell_mean = ""

            try:
                raster_extent = raster.extent.JSON
            except:
                raster_extent = ""
        else:
            raster_format = ""
            raster_bands = ""
            raster_format = ""
            raster_bands = ""
            raster_compression = ""
            raster_size = ""
            raster_cell_width = ""
            raster_cell_height = ""
            raster_cell_min = ""
            raster_cell_max = ""
            raster_cell_mean = ""
            raster_extent = ""

        meta.update({str(lyr_name): {
            'Data_Frame': frame.name,
            'Layer_Basename': lyr_basename,
            'Layer_Type': lyr_dtype,
            'File_Extension': lyr_extension,
            'Layer_Catalog_Path': lyr_catpath,
            'Layer_DefinitionQuery_Supported': lyrDefSupport,
            'Layer_DefinitionQuery': lyrDef,
            'Field_Names': fieldNameStr,
            'Feature_Type': feature_type,
            'Shape_Type': shape_type,
            'Has_Z': has_z,
            'Has_Spatial_Index': has_spat_index,
            'Layer_File': lyr_file,
            'Layer_Path': lyr_path,
            'Coordinate_Type': lyr_coordType,
            'GCS_Name': lyr_GCSName,
            'GCS_Code': lyr_GCSCode,
            'PCS_Name': lyr_PCSName,
            'PCS_Code': lyr_PCSCode,
            'Linear_Unit_Name': lyr_coord_unit,
            'Linear_Unit_Code': lyr_coord_unit_code,
            'Datum_Name': lyr_datumName,
            'Datum_Code': lyr_datumCode,
            'Spheroid_Name': lyr_spheroidName,
            'Spheroid_Code': lyr_spheroidCode,
            'Layer_Description': lyr_description,
            'Raster_Format': raster_format,
            'Raster_Band_Count': raster_bands,
            'Raster_Compression_Type': raster_compression,
            'Raster_Size_MB': raster_size,
            'Raster_Cell_Width': raster_cell_width,
            'Raster_Cell_Height': raster_cell_height,
            'Raster_Cell_Min': raster_cell_min,
            'Raster_Cell_Max': raster_cell_max,
            'Raster_Cell_Mean': raster_cell_mean,
            'Raster_Extent_JSON': raster_extent
            }
        })


    meta = {}
    cur_mxd = arcpy.mapping.MapDocument(mxd)
    df = arcpy.mapping.ListDataFrames(cur_mxd, "*")
    df_index = 0
    for frame in df:
        print(Style.BRIGHT + Fore.WHITE + 'Scanning layers in dataframe: ' + Style.DIM + '{}'.format(frame.name))
        for lyr in arcpy.mapping.ListLayers(cur_mxd, "", frame):
            if lyr.isBasemapLayer:
                pass
            else:
                if lyr.isGroupLayer:
                    for glyr in lyr:
                        if glyr.isBasemapLayer:
                            pass
                        else:
                            if glyr.isGroupLayer:
                                for g2lyr in glyr:
                                    if g2lyr.isBasemapLayer:
                                        pass
                                    else:
                                        if g2lyr.isGroupLayer:
                                            for g3lyr in g2lyr:
                                                if g3lyr.isBasemapLayer:
                                                    pass
                                                else:
                                                    if g3lyr.isGroupLayer:
                                                        for g4lyr in g3lyr:
                                                            if g4lyr.isBasemapLayer:
                                                                pass
                                                            else:
                                                                if g4lyr.isGroupLayer:
                                                                    for g5lyr in g4lyr:
                                                                        if g5lyr.isBasemapLayer:
                                                                            pass
                                                                        else:
                                                                            if g5lyr.isGroupLayer:
                                                                                for g6lyr in g5lyr:
                                                                                    if g6lyr.isBasemapLayer:
                                                                                        pass
                                                                                    else:
                                                                                        try:
                                                                                            lyrDescriptions(g6lyr)
                                                                                        except:
                                                                                            print('> 6 nested groups present. Skipping those.')
                                                                                            pass
                                                                            else:
                                                                                lyrDescriptions(g5lyr)
                                                                else:
                                                                    lyrDescriptions(g4lyr)
                                                    else:
                                                        lyrDescriptions(g3lyr)
                                        else:
                                            lyrDescriptions(g2lyr)
                            else:
                                lyrDescriptions(glyr)
                else:
                    lyrDescriptions(lyr)
        df_index += 1

    print(Style.BRIGHT + Fore.WHITE + '\nTotal dataframes: ' + Style.DIM + '{}'.format(df_index))
    lyr_count = 0
    for lyr in meta:
        lyr_count += 1
    print(Style.BRIGHT + Fore.WHITE + 'Total layers: ' + Style.DIM + '{}'.format(lyr_count))

    return meta

def write_output(mxdName, mxdMeta, csvPath):
    if csvPath == '':
        fPath = 'H:\{}.csv'.format(mxdName)
    else:
        fPath = os.path.join(csvPath, mxdName + '.csv')

    if os.path.exists(fPath):
        try:
            os.remove(fPath)
        except:
            print(Style.BRIGHT + Fore.RED + 'ERROR: File already exists and cannot remove. Check that the file isnt being used.')
            print(Style.BRIGHT + Fore.WHITE + 'File: ', fPath)
            sys.exit()

    headers = ['Layer_Name', 'Data_Frame', 'Layer_Basename', 'Layer_Type', 'File_Extension', 'Feature_Type', 'Shape_Type', 'Has_Z', 'Has_Spatial_Index', 'Field_Names',
                'Layer_Path', 'Layer_Catalog_Path', 'Layer_DefinitionQuery_Supported', 'Layer_DefinitionQuery', 'Coordinate_Type', 'GCS_Name', 'GCS_Code', 'PCS_Name', 'PCS_Code',
                'Linear_Unit_Name', 'Linear_Unit_Code', 'Datum_Name', 'Datum_Code', 'Spheroid_Name', 'Spheroid_Code',
                'Raster_Format', 'Raster_Band_Count', 'Raster_Compression_Type', 'Raster_Size_MB', 'Raster_Cell_Width', 'Raster_Cell_Height',
                'Raster_Cell_Min', 'Raster_Cell_Max', 'Raster_Cell_Mean', 'Raster_Extent_JSON',
                'Layer_Description', 'Script_User', 'Script_Run_Time']

    try:
        with open(fPath, 'wb') as f:
            f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            f_writer.writerow(headers)
            for lyr in sorted(mxdMeta.keys()):
                row = []
                for header in headers:
                    if header == 'Layer_Name':
                        row.append(lyr)
                    elif header == 'Script_User':
                        row.append(USER)
                    elif header == 'Script_Run_Time':
                        row.append(RUN_TIME)
                    else:
                        row.append(mxdMeta[lyr][header])
                f_writer.writerow(row)
    except:
        print(Style.BRIGHT + Fore.WHITE + 'ERROR: Cannot write to output file. Check that the file isnt being used.')
        sys.exit()
    return fPath

def main():
    CLI()
    print(Style.BRIGHT + Fore.GREEN + "\nRUNNING - ArcGIS MXD metadata compiler\n")
    print(Style.BRIGHT + Fore.WHITE + '\nImporting arcpy.')
    import arcpy
    mxd = sys.argv[1]
    print(Style.BRIGHT + Fore.WHITE + '\nLoading MXD: ' + Style.DIM + '{}\n'.format(mxd))
    mxdMeta = mainFunction(mxd)
    mxdNameExt = os.path.basename(mxd)
    mxdName = os.path.splitext(mxdNameExt)[0]
    if len(sys.argv) == 3:
        csvPath = sys.argv[2]
    else:
        csvPath = ''
    output_file = write_output(mxdName, mxdMeta, csvPath)
    print(Style.BRIGHT + Fore.WHITE + '\nOutput file: ' + Style.DIM + '{}'.format(output_file))
    print(Style.BRIGHT + Fore.GREEN + 'Done.')


if __name__ == '__main__':
    main()
