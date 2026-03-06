import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image # Needed for image manipulation

# --- SIDEBAR CUSTOMIZATION ---
st.sidebar.title('Customize your QR Code')

fill_color = st.sidebar.color_picker('Pick a QR Code Color', "#0C1CB3") 
back_color = st.sidebar.color_picker('Pick a Background Color', "#FFFFFF") 

# NEW: Logo Uploader
logo_file = st.sidebar.file_uploader("Upload a Logo (Optional)", type=['png', 'jpg', 'jpeg'])

# --- MAIN APP AREA ---
st.title('Custom QR Code Generator :rocket:')

with st.expander("App Description"):
    st.write("""
    This app allows you to generate QR Codes with custom colors and logos.
    POC: Your Name, first.last@nps.edu
    """)

text = st.text_input(label='Enter Text or URL to encode')

if text:
    # 1. Setup the QR Object
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H, # High correction is REQUIRED for logos
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    # 2. Create the base QR image (Convert to RGB so we can paste colors onto it)
    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')

    # 3. IF A LOGO IS UPLOADED, OVERLAY IT
    if logo_file:
        logo = Image.open(logo_file)
        
        # Convert logo to RGBA to ensure it handles transparency correctly
        logo = logo.convert("RGBA")
        
        # Calculate size 
        width, height = qr_img.size
        logo_size = width // 5 
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # Find the center position
        pos = ((width - logo_size) // 2, (height - logo_size) // 2)
        
        # Paste the logo onto the QR code using the logo itself as the mask
        qr_img.paste(logo, pos, logo)

    # 4. Display and Download
    st.write(f'QR Code generated for **{text}**:')
    st.image(qr_img)
    
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="Download Custom QR Code",
        data=byte_im,
        file_name="custom_qrcode.png",
        mime="image/png"

    )
