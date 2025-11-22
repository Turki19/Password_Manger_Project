import os
import base64
import random
import string

import streamlit as st

# ================== Constants ==================

LOGO_PATH = "logo.png"
MASTER_FILE = "master_password.txt"
PASSWORDS_FILE = "app_passwords.txt"


# ================== Styles ==================

def apply_custom_style() -> None:
    """Inject custom CSS for the app."""
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #ceecec !important;
        }

        .block-container {
            padding-top: 3rem !important;
            padding-bottom: 2rem !important;
        }

        h1, h2, h3, h4, h5, h6, p, label, span {
            color: #369e9e !important;
        }

        [data-testid="stSidebar"] {
            background-color: #bcdada !important;
        }
        [data-testid="stSidebar"] * {
            color: #369e9e !important;
        }

        input[type="text"], input[type="password"] {
            background-color: #b8d4d4 !important;
            color: #06494D !important;
            border-radius: 8px !important;
            border: 1.5px solid #369e9e !important;
            padding: 0.4rem 0.6rem !important;
        }

        input[type="text"]:focus, input[type="password"]:focus {
            border: 1.5px solid #2b7f7f !important;
            box-shadow: none !important;
            outline: none !important;
        }

        div[data-baseweb="input"] {
            box-shadow: none !important;
            border-radius: 8px !important;
        }

        div[data-baseweb="input"]:focus-within {
            box-shadow: 0 0 0 1px #2b7f7f !important;
            border: 1.5px solid #2b7f7f !important;
        }

        [data-testid="stTextInputInstructions"] {
            display: none !important;
        }

        /* Buttons (Login, Add, Save...) */
        .stButton > button, .stButton > button *, button[kind="secondary"] {
            background-color: #369e9e !important;
            color: #ceecec !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 600 !important;
            padding: 0.25rem 1.1rem !important;
            font-size: 0.95rem !important;
        }

        .stButton > button:hover, button[kind="secondary"]:hover {
            opacity: 0.9 !important;
        }

        /* Header container (logo + title) */
        .header-container {
            margin-top: 30px !important;
            margin-bottom: -20px !important;
        }

        .header-container h1 {
            margin-top: -20px !important;
        }

        /* List style in View Passwords */
        .listed-passwords {
            margin-top: -20px !important;
            color: #06494D !important;
            font-size: 1.05rem !important;
        }

        .password-hidden {
            color: #2b7f7f !important;
            font-weight: 600 !important;
            font-size: 1.2rem !important;
            letter-spacing: 3px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ================== Data helpers ==================

def load_passwords() -> dict:
    """Load stored passwords from file into a dictionary."""
    storage = {}
    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, "r") as f:
            for line in f:
                if ":" in line:
                    account, encoded_pw = line.strip().split(":", 1)
                    storage[account] = encoded_pw
    return storage


def save_passwords(storage: dict) -> None:
    """Save passwords dictionary to file."""
    with open(PASSWORDS_FILE, "w") as f:
        for account, encoded_pw in storage.items():
            f.write(f"{account}:{encoded_pw}\n")


def evaluate_password(pw: str) -> dict:
    """Evaluate password and return details + strength."""
    score = 0
    result = {
        "length_ok": False,
        "has_upper": False,
        "has_lower": False,
        "has_digit": False,
        "has_symbol": False,
        "strength": "Weak",
    }

    if len(pw) >= 8:
        result["length_ok"] = True
        score += 20

    if any(char.isupper() for char in pw):
        result["has_upper"] = True
        score += 20

    if any(char.islower() for char in pw):
        result["has_lower"] = True
        score += 20

    if any(char.isdigit() for char in pw):
        result["has_digit"] = True
        score += 20

    symbols = "!@#$%^&*()-_=+[]{};:,.<>/"
    if any(char in symbols for char in pw):
        result["has_symbol"] = True
        score += 20

    if score == 100:
        result["strength"] = "Strong"
    elif 80 >= score >= 50:
        result["strength"] = "Medium"
    else:
        result["strength"] = "Weak"

    return result


def password_generator(length: int, preference: list[str]) -> tuple[str, str]:
    """
    Generate a password of given length.
    preference = [upper?, digits?, symbols?] with values "yes"/"no".
    """
    all_pools = []
    password_chars = []

    # Always include lowercase letters
    lowercase = string.ascii_lowercase
    all_pools.append(lowercase)
    password_chars.append(random.choice(lowercase))

    if preference[0] == "yes":
        uppercase = string.ascii_uppercase
        all_pools.append(uppercase)
        password_chars.append(random.choice(uppercase))

    if preference[1] == "yes":
        digits = string.digits
        all_pools.append(digits)
        password_chars.append(random.choice(digits))

    if preference[2] == "yes":
        symbols = string.punctuation
        all_pools.append(symbols)
        password_chars.append(random.choice(symbols))

    # Complete password to required length
    while len(password_chars) < length:
        pool = random.choice(all_pools)
        password_chars.append(random.choice(pool))

    password = "".join(password_chars[:length])
    eval_results = evaluate_password(password)
    return password, eval_results["strength"]


def get_logo_base64(path: str) -> str | None:
    """Return base64-encoded logo or None."""
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None


# ================== Authentication UI ==================

def create_master_password() -> None:
    """Screen to create the initial master password."""
    st.subheader("Create Master Password")

    new_pw = st.text_input("Enter a new master password", type="password")
    if st.button("Create master password"):
        if not new_pw:
            st.error("Please enter a password.")
            return

        evaluation = evaluate_password(new_pw)
        st.write(f"Password strength: **{evaluation['strength']}**")

        encoded_password = base64.b64encode(new_pw.encode()).decode()
        with open(MASTER_FILE, "w") as f:
            f.write(encoded_password)

        st.success("Master password created successfully. You are now logged in.")
        st.session_state.authenticated = True


def login_screen() -> None:
    """Login screen for master password."""
    if not os.path.exists(MASTER_FILE):
        create_master_password()
        return

    st.subheader("Login")

    pw = st.text_input("Enter master password", type="password", autocomplete="off")
    if st.button("Login"):
        with open(MASTER_FILE, "r") as f:
            stored = f.read().strip()

        encoded_user_password = base64.b64encode(pw.encode()).decode()
        if encoded_user_password == stored:
            st.session_state.authenticated = True
            st.session_state.storage = load_passwords()
            st.success("Logged in successfully.")
            st.rerun()
        else:
            st.error("Wrong password. Try again.")


# ================== Pages / UI functions ==================

def add_password_ui() -> None:
    st.subheader("Add Password")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    account = st.text_input("Account name", key="add_account_name").title()
    password = st.text_input("Password", type="password", key="add_password")

    if st.button("Add", key="add_password_btn"):
        if not account or not password:
            st.error("Please fill in all fields.")
            st.markdown("</div>", unsafe_allow_html=True)
            return

        evaluation = evaluate_password(password)
        st.write(f"Password strength: **{evaluation['strength']}**")

        encoded_password = base64.b64encode(password.encode()).decode()
        st.session_state.storage[account] = encoded_password
        st.success("Password added successfully.")

    st.markdown("</div>", unsafe_allow_html=True)


def update_password_ui() -> None:
    st.subheader("Update Password")

    if not st.session_state.storage:
        st.info("No accounts to update.")
        return

    accounts = sorted(st.session_state.storage.keys())
    selected_account = st.selectbox("Select account to update", accounts)

    with st.form("update_form"):
        new_pw = st.text_input("New password", type="password")
        submitted = st.form_submit_button("Update")

        if submitted:
            if not new_pw:
                st.error("Please enter a password.")
                return

            evaluation = evaluate_password(new_pw)
            st.write(f"Password strength: **{evaluation['strength']}**")

            if evaluation["strength"] == "Weak":
                st.error("Password too weak — update denied.")
                return

            encoded = base64.b64encode(new_pw.encode()).decode()
            st.session_state.storage[selected_account] = encoded
            st.success("Password updated successfully.")


def delete_password_ui() -> None:
    st.subheader("Delete Password")

    if not st.session_state.storage:
        st.info("No accounts to delete.")
        return

    accounts = sorted(st.session_state.storage.keys())
    selected_account = st.selectbox("Select account to delete", accounts)

    if st.button("Delete this account"):
        del st.session_state.storage[selected_account]
        st.success(f"Deleted password for **{selected_account}**.")


def generate_password_ui() -> None:
    st.subheader("Generate Password")

    length = st.number_input(
        "Password length", min_value=4, max_value=64, value=12, step=1
    )
    include_upper = st.checkbox("Include uppercase letters", value=True)
    include_nums = st.checkbox("Include numbers", value=True)
    include_symbols = st.checkbox("Include symbols", value=True)

    if st.button("Generate"):
        prefs = [
            "yes" if include_upper else "no",
            "yes" if include_nums else "no",
            "yes" if include_symbols else "no",
        ]
        pw, strength = password_generator(length, prefs)

        # Color based on strength
        if strength == "Strong":
            bg_color = "#d4f5d4"   # light green
            text_color = "#1b5e20"  # dark green
        elif strength == "Medium":
            bg_color = "#fff6b3"   # light yellow
            text_color = "#8a6d00"  # dark yellow/brown
        else:  # Weak
            bg_color = "#ffd6d6"   # light red
            text_color = "#7d0000"  # dark red

        # Password box
        st.markdown(
            f"""
            <div style="
                background-color: {bg_color};
                padding: 12px;
                border-radius: 8px;
                font-family: monospace;
                font-size: 18px;
                color: {text_color};
                text-align: center;
                margin-top: 10px;
            ">
                {pw}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Strength text
        st.markdown(
            f"""
            <p style="font-weight: bold; color: {text_color}; margin-top: 8px;">
                Strength: {strength}
            </p>
            """,
            unsafe_allow_html=True,
        )


def view_passwords_ui() -> None:
    st.subheader("View Saved Accounts")

    storage = st.session_state.storage
    if not storage:
        st.info("No passwords stored.")
        return

    query = st.text_input("Search by account name (optional)")
    show_passwords = st.checkbox("Show passwords", value=False)

    filtered = {
        acc: pw for acc, pw in storage.items()
        if not query or query.lower() in acc.lower()
    }

    if not filtered:
        st.warning(f"No results found for '{query}'.")
        return

    st.markdown(
        f"<p class='listed-passwords'>Total passwords: <b>{len(filtered)}</b></p>",
        unsafe_allow_html=True,
    )

    for i, (acc, enc_pw) in enumerate(sorted(filtered.items()), start=1):
        if show_passwords:
            password_display = base64.b64decode(enc_pw.encode()).decode()
        else:
            password_display = "<span class='password-hidden'>●●●●●●●●</span>"

        st.markdown(
            f"<p class='listed-passwords'>{i}. <b>{acc}</b> : {password_display}</p>",
            unsafe_allow_html=True,
        )


# ================== Main app ==================

def main() -> None:
    st.set_page_config(page_title="Password Manager")
    apply_custom_style()

    # Small top spacer
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # ----- Header (logo + title) -----
    col_logo, col_title = st.columns([1, 3], gap="small")

    with col_logo:
        if os.path.exists(LOGO_PATH):
            logo_b64 = get_logo_base64(LOGO_PATH)
            if logo_b64:
                st.markdown(
                    f"""
                    <img src="data:image/png;base64,{logo_b64}"
                         style="width:190px; margin-top:10px;">
                    """,
                    unsafe_allow_html=True,
                )

    with col_title:
        st.markdown(
            """
            <h1 style="margin-top:30px; margin-bottom:2px;">
                Password Manager
            </h1>
            <p style="margin-top:-8px; font-size:0.95rem;">
                Securely store, generate, and manage your passwords.
            </p>
            """,
            unsafe_allow_html=True,
        )

    # Divider
    st.markdown(
        "<hr style='margin-top:15px; margin-bottom:15px;'>",
        unsafe_allow_html=True,
    )

    # ----- Session state -----
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "storage" not in st.session_state:
        st.session_state.storage = load_passwords()

    # ----- Login -----
    if not st.session_state.authenticated:
        login_screen()
        return

    # ----- Sidebar -----
    st.sidebar.header("Menu")
    choice = st.sidebar.radio(
        "Choose an action",
        [
            "Add password",
            "Update password",
            "Delete password",
            "Generate password",
            "View passwords",
        ],
    )

    if st.sidebar.button("Save Changes"):
        save_passwords(st.session_state.storage)
        st.sidebar.success("The changes saved!")

    # ----- Main content -----
    if choice == "Add password":
        add_password_ui()
    elif choice == "Update password":
        update_password_ui()
    elif choice == "Delete password":
        delete_password_ui()
    elif choice == "Generate password":
        generate_password_ui()
    elif choice == "View passwords":
        view_passwords_ui()


if __name__ == "__main__":
    main()
