ArcGIS MXD metadata compiler

mxd-metadata_standalone.py (command line)<br>


This program scans all dataframes and layers in an ArcGIS .mxd file for layer descriptions and produces a CSV of findings.

<b>Requires ArcPy</b><br>

<h3>Usage:</h3> python "\mxd-metadata\mxd-metadata_standalone.py" [mxd_path] [output_csv_dir]
<h3>or:</h3> python "\mxd-metadata\mxd-metadata_standalone.py" [mxd_path]

<h3>Example:</h3>
  python "\mxd-metadata\mxd-metadata_standalone.py" "C:\Users\User\Documents\MyMap.mxd" "C:\Users\User\Desktop"

<h3>Example Output:</h3>
"C:\Users\User\Desktop\MyMap.csv"

<h3>Personalization</h3>
On the second line of the write_output() function, change the "fPath" variable to your desired default output location.
