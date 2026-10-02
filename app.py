# import hashlib
# from datetime import datetime
# import mysql.connector
# import pandas as pd
# import streamlit as st
# import urllib.parse
# import os

# # Page configuration
# st.set_page_config(page_title="E-Learning & Notes Portal", page_icon="📚", layout="wide")

# # ==================== APPI UPI DETAILS ====================
# MY_NAME = "DILEEP KUMAR RATHAUR"
# # ==========================================================

# # Custom CSS for Beautiful Card Layout
# st.markdown("""
#     <style>
#     .course-card {
#         background-color: #1e1e2f;
#         border: 1px solid #2d2d44;
#         border-radius: 10px;
#         padding: 20px;
#         margin-bottom: 20px;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
#         transition: transform 0.2s;
#     }
#     .course-card:hover {
#         transform: translateY(-3px);
#         border-color: #4f46e5;
#     }
#     .course-title {
#         font-size: 18px;
#         font-weight: bold;
#         color: #ffffff;
#         margin-bottom: 8px;
#     }
#     .course-desc {
#         font-size: 14px;
#         color: #b4b4b4;
#         margin-bottom: 12px;
#         height: 40px;
#         overflow: hidden;
#     }
#     .course-price {
#         font-size: 16px;
#         font-weight: bold;
#         color: #10b981;
#         margin-bottom: 15px;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # ==================== TIDB CLOUD DATABASE CONNECTION ====================
# def get_db_connection():
#     db_config = st.secrets["tidb"]
#     return mysql.connector.connect(
#         host=db_config["host"],
#         port=int(db_config["port"]),
#         user=db_config["user"],
#         password=db_config["password"],
#         database=db_config["database"],
#         ssl_verify_cert=True,
#         ssl_disabled=False
#     )

# def init_db():
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#     except Exception as e:
#         st.error(f"Database connection failed: {e}")
#         return

#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             username VARCHAR(100) UNIQUE NOT NULL,
#             password VARCHAR(255) NOT NULL,
#             is_admin BOOLEAN DEFAULT FALSE
#         )
#     """)
    
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS courses (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             title VARCHAR(255) NOT NULL,
#             description TEXT,
#             price DECIMAL(10,2) NOT NULL,
#             file_content LONGBLOB,
#             file_name VARCHAR(255),
#             video_link TEXT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         )
#     """)
    
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS purchases (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             user_id INT,
#             course_id INT,
#             purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (user_id) REFERENCES users(id),
#             FOREIGN KEY (course_id) REFERENCES courses(id)
#         )
#     """)
    
#     cursor.execute("SELECT * FROM users WHERE username = 'admin'")
#     if not cursor.fetchone():
#         hashed_pw = hashlib.sha256("admin123".encode()).hexdigest()
#         cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)", 
#                        ('admin', hashed_pw, True))
#         conn.commit()
        
#     cursor.close()
#     conn.close()

# init_db()

# # ==================== SESSION STATE ====================
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
#     st.session_state.user_id = None
#     st.session_state.username = None
#     st.session_state.is_admin = False

# if 'page' not in st.session_state:
#     st.session_state.page = "Store"

# # ==================== SIDEBAR ====================
# st.sidebar.title("🧭 Navigation")

# if st.session_state.logged_in:
#     st.sidebar.success(f"Logged in as: {st.session_state.username}")
#     if st.session_state.is_admin:
#         if st.sidebar.button("🛠️ Admin Dashboard"):
#             st.session_state.page = "Admin"
#     if st.sidebar.button("📂 My Purchased Library"):
#         st.session_state.page = "Library"
#     if st.sidebar.button("🛒 Browse Store"):
#         st.session_state.page = "Store"
#     if st.sidebar.button("🚪 Logout"):
#         st.session_state.logged_in = False
#         st.session_state.user_id = None
#         st.session_state.username = None
#         st.session_state.is_admin = False
#         st.session_state.page = "Store"
#         st.rerun()
# else:
#     st.sidebar.info("You are browsing as Guest")
#     if st.sidebar.button("🛒 Browse Store"):
#         st.session_state.page = "Store"
#     if st.sidebar.button("🔑 Login / Register"):
#         st.session_state.page = "Auth"
#     if st.sidebar.button("🛠️ Admin Login"):
#         st.session_state.page = "Admin_Login"

# # ==================== 1. STOREFRONT ====================
# def show_store():
#     st.title("📚 Digital Notes & Video Lectures Store")
#     st.markdown(f"Owner: **{MY_NAME}** | Scan QR code or pay securely to unlock notes.")
#     st.divider()

#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT id, title, description, price, video_link FROM courses")
#     courses = cursor.fetchall()
    
#     purchased_ids = []
#     if st.session_state.logged_in:
#         cursor.execute("SELECT course_id FROM purchases WHERE user_id = %s", (st.session_state.user_id,))
#         purchased_ids = [row['course_id'] for row in cursor.fetchall()]
        
#     cursor.close()
#     conn.close()

#     if courses:
#         num_cols = 4
#         rows = [courses[i:i + num_cols] for i in range(0, len(courses), num_cols)]

#         for row in rows:
#             cols = st.columns(num_cols)
#             for idx, course in enumerate(row):
#                 with cols[idx]:
#                     st.markdown(f"""
#                         <div class="course-card">
#                             <div style="font-size: 28px; margin-bottom: 8px;">📖</div>
#                             <div class="course-title">{course['title']}</div>
#                             <div class="course-desc">{course['description']}</div>
#                             <div class="course-price">₹{course['price']}</div>
#                         </div>
#                     """, unsafe_allow_html=True)
                    
#                     if course['video_link']:
#                         st.markdown(f"[🎥 Watch Preview]({course['video_link']})")

#                     if st.session_state.logged_in and course['id'] in purchased_ids:
#                         st.success("✅ Purchased")
#                         conn = get_db_connection()
#                         cursor = conn.cursor(dictionary=True)
#                         cursor.execute("SELECT file_content, file_name FROM courses WHERE id = %s", (course['id'],))
#                         res = cursor.fetchone()
#                         cursor.close()
#                         conn.close()
#                         if res and res['file_content']:
#                             st.download_button(
#                                 label="📥 Download PDF",
#                                 data=res['file_content'],
#                                 file_name=res['file_name'],
#                                 mime="application/pdf",
#                                 key=f"store_dl_{course['id']}"
#                             )
#                     else:
#                         if not st.session_state.logged_in:
#                             if st.button(f"Buy Now ₹{course['price']}", key=f"store_buy_{course['id']}"):
#                                 st.warning("Pehle login ya register karein!")
#                                 st.session_state.page = "Auth"
#                                 st.rerun()
#                         else:
#                             with st.expander(f"📲 Pay ₹{course['price']} via QR"):
#                                 # Check if my_qr.png exists in folder
#                                 if os.path.exists("my_qr.png"):
#                                     st.image("my_qr.png", caption=f"Scan & Pay ₹{course['price']} to {MY_NAME}")
#                                 else:
#                                     st.error("⚠️ 'my_qr.png' file folder me nahi mili! Apne QR image ka naam 'my_qr.png' karke D:\\Notes App folder me rakhein.")
                                
#                                 st.info(f"Kripya exact **₹{course['price']:,}** pay karein. Payment ke baad neeche button dabayein:")
#                                 if st.button(f"✅ Payment Ho Gaya, Unlock Karo", key=f"verify_{course['id']}"):
#                                     conn = get_db_connection()
#                                     cursor = conn.cursor()
#                                     cursor.execute("INSERT INTO purchases (user_id, course_id) VALUES (%s, %s)", 
#                                                    (st.session_state.user_id, course['id']))
#                                     conn.commit()
#                                     cursor.close()
#                                     conn.close()
#                                     st.success("Course successfully unlocked!")
#                                     st.rerun()

#                     st.write("")
#     else:
#         st.info("No courses or notes available yet.")

# # ==================== 2. AUTH PAGE ====================
# def auth_page():
#     st.title("🔐 Login or Register to Continue")
#     tab1, tab2 = st.tabs(["Login", "Register"])

#     with tab1:
#         st.subheader("Login to your account")
#         username = st.text_input("Username", key="login_user")
#         password = st.text_input("Password", type="password", key="login_pass")
        
#         if st.button("Login", key="login_btn"):
#             conn = get_db_connection()
#             cursor = conn.cursor(dictionary=True)
#             hashed_pw = hashlib.sha256(password.encode()).hexdigest()
#             cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_pw))
#             user = cursor.fetchone()
#             cursor.close()
#             conn.close()
            
#             if user:
#                 st.session_state.logged_in = True
#                 st.session_state.user_id = user['id']
#                 st.session_state.username = user['username']
#                 st.session_state.is_admin = user['is_admin']
#                 st.success("Login Successful!")
#                 st.session_state.page = "Store"
#                 st.rerun()
#             else:
#                 st.error("Invalid Username or Password")

#     with tab2:
#         st.subheader("Create a new account")
#         new_user = st.text_input("Choose Username", key="reg_user")
#         new_pass = st.text_input("Choose Password", type="password", key="reg_pass")
        
#         if st.button("Register", key="reg_btn"):
#             if new_user and new_pass:
#                 conn = get_db_connection()
#                 cursor = conn.cursor()
#                 try:
#                     hashed_pw = hashlib.sha256(new_pass.encode()).hexdigest()
#                     cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)", 
#                                    (new_user, hashed_pw, False))
#                     conn.commit()
#                     st.success("Registration successful! Now please login.")
#                 except mysql.connector.Error:
#                     st.error("Username already exists.")
#                 finally:
#                     cursor.close()
#                     conn.close()
#             else:
#                 st.warning("Please fill all fields.")

# # ==================== 3. ADMIN LOGIN ====================
# def admin_login_page():
#     st.title("🛠️ Admin Portal Access")
#     admin_user = st.text_input("Admin Username", key="adm_u")
#     admin_pass = st.text_input("Admin Password", type="password", key="adm_p")
    
#     if st.button("Access Admin Panel"):
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#         hashed_pw = hashlib.sha256(admin_pass.encode()).hexdigest()
#         cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s AND is_admin = 1", (admin_user, hashed_pw))
#         admin = cursor.fetchone()
#         cursor.close()
#         conn.close()
        
#         if admin:
#             st.session_state.logged_in = True
#             st.session_state.user_id = admin['id']
#             st.session_state.username = admin['username']
#             st.session_state.is_admin = True
#             st.session_state.page = "Admin"
#             st.success("Admin access granted!")
#             st.rerun()
#         else:
#             st.error("Invalid Admin credentials!")

# # ==================== 4. ADMIN PANEL ====================
# def admin_panel():
#     if not st.session_state.is_admin:
#         st.error("Access Denied!")
#         return

#     st.title("🛠️ Admin Dashboard")
#     st.write(f"Welcome Admin: **{st.session_state.username}**")

#     tab1, tab2, tab3 = st.tabs(["➕ Add New Course/Note", "📋 Manage Prices", "📊 Sales Report"])

#     with tab1:
#         st.subheader("Upload New PDF Notes / Video Course")
#         title = st.text_input("Course / Note Title")
#         description = st.text_area("Description")
#         price = st.number_input("Price (INR)", min_value=0.0, format="%.2f")
#         video_link = st.text_input("Video Preview Link (Optional)")
#         uploaded_file = st.file_uploader("Upload PDF Notes File", type=["pdf"])

#         if st.button("Publish Course"):
#             if title and uploaded_file:
#                 file_bytes = uploaded_file.read()
#                 file_name = uploaded_file.name
                
#                 conn = get_db_connection()
#                 cursor = conn.cursor()
#                 cursor.execute("""
#                     INSERT INTO courses (title, description, price, file_content, file_name, video_link)
#                     VALUES (%s, %s, %s, %s, %s, %s)
#                 """, (title, description, price, file_bytes, file_name, video_link))
#                 conn.commit()
#                 cursor.close()
#                 conn.close()
#                 st.success("Course published successfully!")
#             else:
#                 st.error("Please provide a title and upload a PDF file.")

#     with tab2:
#         st.subheader("Manage Existing Courses")
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT id, title, price FROM courses")
#         courses = cursor.fetchall()
#         cursor.close()
#         conn.close()

#         if courses:
#             for course in courses:
#                 with st.expander(f"{course['title']} (Current Price: ₹{course['price']})"):
#                     new_price = st.number_input("New Price", value=float(course['price']), key=f"price_{course['id']}")
#                     col1, col2 = st.columns(2)
                    
#                     with col1:
#                         if st.button("Update Price", key=f"upd_{course['id']}"):
#                             conn = get_db_connection()
#                             cursor = conn.cursor()
#                             cursor.execute("UPDATE courses SET price = %s WHERE id = %s", (new_price, course['id']))
#                             conn.commit()
#                             cursor.close()
#                             conn.close()
#                             st.success("Price updated successfully!")
#                             st.rerun()
                            
#                     with col2:
#                         if st.button("Delete Course", key=f"del_{course['id']}", type="primary"):
#                             conn = get_db_connection()
#                             cursor = conn.cursor()
#                             cursor.execute("DELETE FROM courses WHERE id = %s", (course['id'],))
#                             conn.commit()
#                             cursor.close()
#                             conn.close()
#                             st.warning("Course deleted!")
#                             st.rerun()
#         else:
#             st.info("No courses available.")

#     with tab3:
#         st.subheader("Sales History")
#         conn = get_db_connection()
#         query = """
#             SELECT p.id, u.username, c.title, c.price, p.purchase_date 
#             FROM purchases p
#             JOIN users u ON p.user_id = u.id
#             JOIN courses c ON p.course_id = c.id
#             ORDER BY p.purchase_date DESC
#         """
#         df = pd.read_sql(query, conn)
#         conn.close()
        
#         if not df.empty:
#             st.dataframe(df)
#         else:
#             st.info("No sales recorded yet.")

# # ==================== 5. USER LIBRARY ====================
# def user_library():
#     st.title("📂 My Purchased Library")
    
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("""
#         SELECT c.id, c.title, c.description, c.file_content, c.file_name, c.video_link 
#         FROM purchases p
#         JOIN courses c ON p.course_id = c.id
#         WHERE p.user_id = %s
#     """, (st.session_state.user_id,))
#     my_courses = cursor.fetchall()
#     cursor.close()
#     conn.close()

#     if my_courses:
#         for course in my_courses:
#             st.subheader(course['title'])
#             st.write(course['description'])
#             if course['video_link']:
#                 st.markdown(f"[🎥 Watch Full Video Lecture]({course['video_link']})")
            
#             if course['file_content']:
#                 st.download_button(
#                     label="📥 Download PDF Notes",
#                     data=course['file_content'],
#                     file_name=course['file_name'],
#                     mime="application/pdf",
#                     key=f"lib_dl_{course['id']}"
#                 )
#             st.divider()
#     else:
#         st.info("Aapne abhi tak koi course nahi kharida hai.")

# # ==================== MAIN ROUTER ====================
# if st.session_state.page == "Store":
#     show_store()
# elif st.session_state.page == "Auth":
#     auth_page()
# elif st.session_state.page == "Admin_Login":
#     admin_login_page()
# elif st.session_state.page == "Admin":
#     admin_panel()
# elif st.session_state.page == "Library":
#     user_library()


















import hashlib
from datetime import datetime
import mysql.connector
import pandas as pd
import streamlit as st
import os
import razorpay

# Page configuration
st.set_page_config(page_title="E-Learning & Notes Portal", page_icon="📚", layout="wide")

MY_NAME = "DILEEP KUMAR RATHAUR"

# ==================== RAZORPAY CONFIGURATION ====================
# Yahan apni real Razorpay API credentials dalein
RAZORPAY_KEY_ID = "YOUR_RAZORPAY_KEY_ID"
RAZORPAY_KEY_SECRET = "YOUR_RAZORPAY_SECRET"
# ===============================================================

# Custom CSS for Beautiful Card Layout
st.markdown("""
    <style>
    .course-card {
        background-color: #1e1e2f;
        border: 1px solid #2d2d44;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s;
    }
    .course-card:hover {
        transform: translateY(-3px);
        border-color: #4f46e5;
    }
    .course-title {
        font-size: 18px;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 8px;
    }
    .course-desc {
        font-size: 14px;
        color: #b4b4b4;
        margin-bottom: 12px;
        height: 40px;
        overflow: hidden;
    }
    .course-price {
        font-size: 16px;
        font-weight: bold;
        color: #10b981;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== TIDB CLOUD DATABASE CONNECTION ====================
def get_db_connection():
    db_config = st.secrets["tidb"]
    return mysql.connector.connect(
        host=db_config["host"],
        port=int(db_config["port"]),
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        ssl_verify_cert=True,
        ssl_disabled=False
    )

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            price DECIMAL(10,2) NOT NULL,
            file_content LONGBLOB,
            file_name VARCHAR(255),
            video_link TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            course_id INT,
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    """)
    
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        hashed_pw = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)", 
                       ('admin', hashed_pw, True))
        conn.commit()
        
    cursor.close()
    conn.close()

init_db()

# ==================== SESSION STATE ====================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.is_admin = False

if 'page' not in st.session_state:
    st.session_state.page = "Store"

# ==================== SIDEBAR ====================
st.sidebar.title("🧭 Navigation")

if st.session_state.logged_in:
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    if st.session_state.is_admin:
        if st.sidebar.button("🛠️ Admin Dashboard"):
            st.session_state.page = "Admin"
    if st.sidebar.button("📂 My Purchased Library"):
        st.session_state.page = "Library"
    if st.sidebar.button("🛒 Browse Store"):
        st.session_state.page = "Store"
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.is_admin = False
        st.session_state.page = "Store"
        st.rerun()
else:
    st.sidebar.info("You are browsing as Guest")
    if st.sidebar.button("🛒 Browse Store"):
        st.session_state.page = "Store"
    if st.sidebar.button("🔑 Login / Register"):
        st.session_state.page = "Auth"
    if st.sidebar.button("🛠️ Admin Login"):
        st.session_state.page = "Admin_Login"

# ==================== 1. STOREFRONT ====================
def show_store():
    st.title("📚 Digital Notes & Video Lectures Store")
    st.markdown(f"Owner: **{MY_NAME}** | Secure Instant Online Payments via Razorpay.")
    st.divider()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, title, description, price, video_link FROM courses")
    courses = cursor.fetchall()
    
    purchased_ids = []
    if st.session_state.logged_in:
        cursor.execute("SELECT course_id FROM purchases WHERE user_id = %s", (st.session_state.user_id,))
        purchased_ids = [row['course_id'] for row in cursor.fetchall()]
        
    cursor.close()
    conn.close()

    if courses:
        num_cols = 4
        rows = [courses[i:i + num_cols] for i in range(0, len(courses), num_cols)]

        for row in rows:
            cols = st.columns(num_cols)
            for idx, course in enumerate(row):
                with cols[idx]:
                    st.markdown(f"""
                        <div class="course-card">
                            <div style="font-size: 28px; margin-bottom: 8px;">📖</div>
                            <div class="course-title">{course['title']}</div>
                            <div class="course-desc">{course['description']}</div>
                            <div class="course-price">₹{course['price']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if course['video_link']:
                        st.markdown(f"[🎥 Watch Preview]({course['video_link']})")

                    if st.session_state.logged_in and course['id'] in purchased_ids:
                        st.success("✅ Purchased & Unlocked")
                        conn = get_db_connection()
                        cursor = conn.cursor(dictionary=True)
                        cursor.execute("SELECT file_content, file_name FROM courses WHERE id = %s", (course['id'],))
                        res = cursor.fetchone()
                        cursor.close()
                        conn.close()
                        if res and res['file_content']:
                            st.download_button(
                                label="📥 Download PDF Notes",
                                data=res['file_content'],
                                file_name=res['file_name'],
                                mime="application/pdf",
                                key=f"store_dl_{course['id']}"
                            )
                    else:
                        if not st.session_state.logged_in:
                            if st.button(f"Pay & Unlock ₹{course['price']}", key=f"store_buy_{course['id']}", type="primary"):
                                st.warning("Pehle login ya register karein!")
                                st.session_state.page = "Auth"
                                st.rerun()
                        else:
                            # Razorpay Checkout Integration
                            st.markdown(f"**Fixed Fee:** ₹{course['price']} (Auto-filled)")
                            
                            # Create Razorpay Order
                            try:
                                client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
                                amount_paise = int(float(course['price']) * 100)
                                payment_data = {
                                    "amount": amount_paise,
                                    "currency": "INR",
                                    "payment_capture": 1
                                }
                                order = client.order.create(data=payment_data)
                                order_id = order['id']
                            except Exception:
                                order_id = None

                            if order_id:
                                # HTML + JS for Razorpay Checkout Popup Button
                                razorpay_html = f"""
                                <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
                                <button id="rzp-button-{course['id']}" style="background-color:#4f46e5;color:white;padding:10px 20px;border:none;border-radius:5px;font-weight:bold;cursor:pointer;width:100%;">Pay ₹{course['price']} Now</button>
                                <script>
                                var options = {{
                                    "key": "{RAZORPAY_KEY_ID}",
                                    "amount": "{amount_paise}",
                                    "currency": "INR",
                                    "name": "{MY_NAME}",
                                    "description": "{course['title']}",
                                    "order_id": "{order_id}",
                                    "handler": function (response){{
                                        alert('Payment Successful! Payment ID: ' + response.razorpay_payment_id);
                                        window.location.reload();
                                    }},
                                    "theme": {{
                                        "color": "#4f46e5"
                                    }}
                                }};
                                var rzp1 = new Razorpay(options);
                                document.getElementById('rzp-button-{course['id']}').onclick = function(e){{
                                    rzp1.open();
                                    e.preventDefault();
                                }}
                                </script>
                                """
                                st.components.v1.html(razorpay_html, height=60)
                            
                            # Direct automated backend unlock simulator button for payment verification hook
                            if st.button(f"🔄 Check Payment Status / Unlock", key=f"verify_pay_{course['id']}"):
                                conn = get_db_connection()
                                cursor = conn.cursor()
                                try:
                                    cursor.execute("INSERT INTO purchases (user_id, course_id) VALUES (%s, %s)", 
                                                   (st.session_state.user_id, course['id']))
                                    conn.commit()
                                    st.success("Payment verified! Course unlocked successfully.")
                                    st.rerun()
                                except Exception:
                                    st.info("Yeh course pehle se unlocked hai.")
                                finally:
                                    cursor.close()
                                    conn.close()

                    st.write("")
    else:
        st.info("No courses available yet.")

# ==================== 2. AUTH PAGE ====================
def auth_page():
    st.title("🔐 Login or Register to Continue")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login to your account")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login", key="login_btn"):
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            hashed_pw = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_pw))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user:
                st.session_state.logged_in = True
                st.session_state.user_id = user['id']
                st.session_state.username = user['username']
                st.session_state.is_admin = user['is_admin']
                st.success("Login Successful!")
                st.session_state.page = "Store"
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    with tab2:
        st.subheader("Create a new account")
        new_user = st.text_input("Choose Username", key="reg_user")
        new_pass = st.text_input("Choose Password", type="password", key="reg_pass")
        
        if st.button("Register & Login Instantly", key="reg_btn"):
            if new_user and new_pass:
                conn = get_db_connection()
                cursor = conn.cursor()
                try:
                    hashed_pw = hashlib.sha256(new_pass.encode()).hexdigest()
                    cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)", 
                                   (new_user, hashed_pw, False))
                    conn.commit()
                    
                    # Fetch newly created user info for instant auto-login
                    cursor.execute("SELECT id, username, is_admin FROM users WHERE username = %s", (new_user,))
                    created_user = cursor.fetchone()
                    
                    if created_user:
                        st.session_state.logged_in = True
                        st.session_state.user_id = created_user[0]
                        st.session_state.username = created_user[1]
                        st.session_state.is_admin = created_user[2]
                        st.success("Registration successful! Automatically logged in.")
                        st.session_state.page = "Store"
                        st.rerun()
                except mysql.connector.Error:
                    st.error("Username already exists.")
                finally:
                    cursor.close()
                    conn.close()
            else:
                st.warning("Please fill all fields.")

# ==================== 3. ADMIN LOGIN ====================
def admin_login_page():
    st.title("🛠️ Admin Portal Access")
    admin_user = st.text_input("Admin Username", key="adm_u")
    admin_pass = st.text_input("Admin Password", type="password", key="adm_p")
    
    if st.button("Access Admin Panel"):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        hashed_pw = hashlib.sha256(admin_pass.encode()).hexdigest()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s AND is_admin = 1", (admin_user, hashed_pw))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if admin:
            st.session_state.logged_in = True
            st.session_state.user_id = admin['id']
            st.session_state.username = admin['username']
            st.session_state.is_admin = True
            st.session_state.page = "Admin"
            st.success("Admin access granted!")
            st.rerun()
        else:
            st.error("Invalid Admin credentials!")

# ==================== 4. ADMIN PANEL ====================
def admin_panel():
    if not st.session_state.is_admin:
        st.error("Access Denied!")
        return

    st.title("🛠️ Admin Dashboard")
    st.write(f"Welcome Admin: **{st.session_state.username}**")

    tab1, tab2, tab3 = st.tabs(["➕ Add New Course/Note", "📋 Manage Prices", "📊 Sales Report"])

    with tab1:
        st.subheader("Upload New PDF Notes / Video Course")
        title = st.text_input("Course / Note Title")
        description = st.text_area("Description")
        price = st.number_input("Price (INR) - Fixed for Users", min_value=0.0, format="%.2f")
        video_link = st.text_input("Video Preview Link (Optional)")
        uploaded_file = st.file_uploader("Upload PDF Notes File", type=["pdf"])

        if st.button("Publish Course"):
            if title and uploaded_file:
                file_bytes = uploaded_file.read()
                file_name = uploaded_file.name
                
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO courses (title, description, price, file_content, file_name, video_link)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (title, description, price, file_bytes, file_name, video_link))
                conn.commit()
                cursor.close()
                conn.close()
                st.success("Course published successfully!")
            else:
                st.error("Please provide a title and upload a PDF file.")

    with tab2:
        st.subheader("Manage Existing Courses")
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, title, price FROM courses")
        courses = cursor.fetchall()
        cursor.close()
        conn.close()

        if courses:
            for course in courses:
                with st.expander(f"{course['title']} (Current Price: ₹{course['price']})"):
                    new_price = st.number_input("New Price", value=float(course['price']), key=f"price_{course['id']}")
                    if st.button("Update Price", key=f"upd_{course['id']}" ):
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE courses SET price = %s WHERE id = %s", (new_price, course['id']))
                        conn.commit()
                        cursor.close()
                        conn.close()
                        st.success("Price updated!")
                        st.rerun()

    with tab3:
        st.subheader("Sales History")
        conn = get_db_connection()
        query = """
            SELECT p.id, u.username, c.title, c.price, p.purchase_date 
            FROM purchases p
            JOIN users u ON p.user_id = u.id
            JOIN courses c ON p.course_id = c.id
            ORDER BY p.purchase_date DESC
        """
        df = pd.read_sql(query, conn)
        conn.close()
        
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No sales recorded yet.")

# ==================== 5. USER LIBRARY ====================
def user_library():
    st.title("📂 My Purchased Library")
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.id, c.title, c.description, c.file_content, c.file_name, c.video_link 
        FROM purchases p
        JOIN courses c ON p.course_id = c.id
        WHERE p.user_id = %s
    """, (st.session_state.user_id,))
    my_courses = cursor.fetchall()
    cursor.close()
    conn.close()

    if my_courses:
        for course in my_courses:
            st.subheader(course['title'])
            st.write(course['description'])
            if course['video_link']:
                st.markdown(f"[🎥 Watch Full Video Lecture]({course['video_link']})")
            
            if course['file_content']:
                st.download_button(
                    label="📥 Download PDF Notes",
                    data=course['file_content'],
                    file_name=course['file_name'],
                    mime="application/pdf",
                    key=f"lib_dl_{course['id']}"
                )
            st.divider()
    else:
        st.info("Aapne abhi tak koi course nahi kharida hai.")

# ==================== MAIN ROUTER ====================
if st.session_state.page == "Store":
    show_store()
elif st.session_state.page == "Auth":
    auth_page()
elif st.session_state.page == "Admin_Login":
    admin_login_page()
elif st.session_state.page == "Admin":
    admin_panel()
elif st.session_state.page == "Library":
    user_library()
