from itskenpo.reservation import Reservation
from pdf_writer import PdfWriter

writer = PdfWriter(input_path="src/itskenpo/input.pdf")
reservation = Reservation.from_config_yaml()
insert_properties = reservation.to_insert_properties()
writer.execute(insert_properties)
