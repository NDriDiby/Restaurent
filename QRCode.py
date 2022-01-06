import pyqrcode
import png
from pyqrcode import QRCode
  
  
# String which represents the QR code
s = "http://www.novacloudlab.com/texasgrillz/?session=texasgrillz&table=10"
  
# Generate QR code
url = pyqrcode.create(s)
  
# Create and save the svg file naming "myqr.svg"
url.svg("Texas_GrillZ_Table_10.svg", scale = 8)
  
# Create and save the png file naming "myqr.png"
url.png('Texas_GrillZ_Table_10.png', scale = 6)