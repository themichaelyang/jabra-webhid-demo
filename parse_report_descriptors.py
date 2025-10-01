import hid
import hid_parser
import warnings

# - Jabra protocol: https://web.archive.org/web/20210728082514/https://developer.jabra.com/site/global/sdks/web/documentation/index.gsp
# - HID report descriptors: https://docs.kernel.org/hid/hidintro.html
# - Online parser + annotations: https://eleccelerator.com/usbdescreqparser/

# > All recent Jabra devices have two USB HID Telephony interfaces, a standard USB Telephony interface defined by the USB Implementers Forum (www.usb.org) and a proprietary telephony interface defined by Jabra and understood only by Jabra applications and SDKs. Softphone applications with built-in HID telephony support, such as Microsoft Lync, use the standard telephony interface.

# Jabra Speak 410
vendor_id = 0x0B0E
product_id = 0x0412

with hid.Device(vendor_id, product_id) as h:
    print(f'Device manufacturer: {h.manufacturer}')
    print(f'Product: {h.product}')
    print(f'Serial Number: {h.serial}')
    # print(h.get_report_descriptor())
    with warnings.catch_warnings(action="ignore"):
        print(h.get_report_descriptor())
        print(" ".join(f"{b:02x}" for b in h.get_report_descriptor()))
        rdesc = hid_parser.ReportDescriptor(h.get_report_descriptor())

        print(rdesc.feature_report_ids)
        print(rdesc.input_report_ids)
        print(rdesc.output_report_ids)

        # Input reports: from device -> computer
        for rid in rdesc.input_report_ids:
            print()
            print(f"========= In Report ID: {rid} ========")
            for item in rdesc.get_input_items(rid):
                print(item)

        # Out reports: from computer -> device
        for rid in rdesc.output_report_ids:
            print()
            print(f"========= Out Report ID: {rid} ========")
            for item in rdesc.get_output_items(rid):
                print(item)
