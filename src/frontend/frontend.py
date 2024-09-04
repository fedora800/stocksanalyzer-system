# streamlit app basic template with docker 
import os
import streamlit as st

def main():
    app_version = os.getenv('APP_VERSION')
    st.write('Welcome to Streamlit in Docker')
    st.write('APP VERSION = ', app_version)

if __name__ == '__main__':
    main()

