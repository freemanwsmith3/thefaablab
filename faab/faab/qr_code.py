import qrcode
import os

# Base URL
BASE_URL = "https://red-ground-011ebaa0f.5.azurestaticapps.net"

# List of all codes
codes = [
    "CODE_1_0ba35e", "CODE_2_ffe976", "CODE_3_6b21bd", "CODE_4_9d1ff9",
    "CODE_5_7d39d6", "CODE_7_95ca6d", "CODE_8_756a98", "CODE_9_aaa123",
    "CODE_10_d38d32", "CODE_11_863f7d", "CODE_12_ef606d", "CODE_13_966d91",
    "CODE_14_4e2c96", "CODE_15_d67894", "CODE_16_a2c09e", "CODE_17_4d60b7",
    "CODE_18_d22a66", "CODE_19_2fe351", "CODE_20_d4d711", "CODE_21_3f8a0c",
    "CODE_22_241c60", "CODE_23_5b7c71", "CODE_24_8b76c9", "CODE_25_69eb11",
    "CODE_26_fbcf46", "CODE_27_c0c739", "CODE_28_f70287", "CODE_29_27d39e",
    "CODE_30_bbd58a", "CODE_31_ed2ae5", "CODE_32_ec6f6d", "CODE_33_099372",
    "CODE_34_a3f2c5", "CODE_35_22d3c9", "CODE_36_971398", "CODE_37_4917d4",
    "CODE_38_874ba6", "CODE_39_c468c0", "CODE_40_de95b2", "CODE_41_a91e20",
    "CODE_42_d55a42", "CODE_43_fff533", "CODE_44_35c2fc", "CODE_45_abbdfb",
    "CODE_46_fcdb36", "CODE_47_ab4c59", "CODE_48_034812", "CODE_49_40af26",
    "CODE_50_135c3d", "CODE_51_64d92e", "CODE_52_de65f4", "CODE_53_a7248c",
    "CODE_54_7f99ce", "CODE_55_295239", "CODE_56_0a97ce", "CODE_57_0ba42f",
    "CODE_58_17e0cf", "CODE_59_a0efda", "CODE_60_11991c", "CODE_61_83caa9",
    "CODE_62_e056f3", "CODE_63_b73950", "CODE_64_20de1e", "CODE_65_7fe0df",
    "CODE_66_9e7e58", "CODE_67_4b9b92", "CODE_68_56e087", "CODE_69_a79257",
    "CODE_70_156c06", "CODE_71_2dd023", "CODE_72_23656d", "CODE_73_7d15ad",
    "CODE_74_2a23b2", "CODE_75_a7aa81", "CODE_76_1695ef", "CODE_77_ec0a31",
    "CODE_78_226d4a", "CODE_79_cc313f", "CODE_80_510af8", "CODE_81_184731",
    "CODE_82_2752c6", "CODE_83_789b96", "CODE_84_add420", "CODE_85_a63eb1",
    "CODE_86_0f4794", "CODE_87_8878af", "CODE_88_19af25", "CODE_89_164bd9",
    "CODE_90_f60ec0", "CODE_91_da70bd", "CODE_92_1534a1", "CODE_93_2a7b7b",
    "CODE_94_aa81c1", "CODE_95_c5bc91", "CODE_96_13acee", "CODE_97_5285fa",
    "CODE_98_b6684b", "CODE_99_839fe5", "test", "CODE_6_046be0", "CODE_0_9005fd"
]

def generate_qr_codes():
    # Create output directory if it doesn't exist
    output_dir = "qr_codes"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # QR code settings
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Generate QR code for each route
    for code in codes:
        # Create the full URL
        url = f"{BASE_URL}/{code}"
        
        # Clear the QR code data
        qr.clear()
        
        # Add the URL to the QR code
        qr.add_data(url)
        qr.make(fit=True)
        
        # Create the QR code image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Save the image
        filename = f"{output_dir}/{code}.png"
        qr_image.save(filename)
        print(f"Generated QR code for {url}")
        
if __name__ == "__main__":
    print("Starting QR code generation...")
    generate_qr_codes()
    print("QR code generation complete!")