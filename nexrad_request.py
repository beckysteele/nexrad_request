import nexradaws
import pytz
import tempfile
from datetime import datetime
import pyart
import gzip
import io

# Temp location for file io
templocation = tempfile.mkdtemp()

# Establish NEXRAD Level II connection
conn = nexradaws.NexradAwsInterface()

# Preliminary params while I get familiar with the data
eastern_timezone = pytz.timezone('US/Eastern')
radar_id = 'KTLX'
start = eastern_timezone.localize(datetime(2013,5,31,17,0))
end = eastern_timezone.localize (datetime(2013,5,31,19,0))
scans = conn.get_avail_scans_in_range(start, end, radar_id)

print("There are {} scans available between {} and {}\n".format(len(scans), start, end))

# Download scans based on params to temp file
results = conn.download(scans[0:1], templocation)

# Enumerate through results for each scan and evaluate reflectivity
for i,scan in enumerate(results.iter_success(),start=1):
    radar = pyart.io.read_nexrad_archive(scan.filepath)
    refl_grid = radar.get_field(0, 'reflectivity')
    # print(type(refl_grid))
