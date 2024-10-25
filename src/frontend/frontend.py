# streamlit app basic template with docker 
import os
import streamlit as st
import pandas as pd


def fn_detect_runtime_env():
  # Detect if running in Docker or Kubernetes
  if os.path.exists('/.dockerenv'):
    st.write('Running inside Docker')
    # Print some Docker-specific environment variables
    docker_hostname = os.getenv('HOSTNAME')
    st.write('Docker HOSTNAME: ', docker_hostname)
  elif os.getenv('KUBERNETES_SERVICE_HOST'):
    st.write('Running inside Kubernetes')
    # Print some Kubernetes-specific environment variables
    k8s_namespace = os.getenv('KUBERNETES_NAMESPACE', 'default')
    k8s_pod_name = os.getenv('HOSTNAME')
    st.write('Kubernetes NAMESPACE: ', k8s_namespace)
    st.write('Kubernetes POD_NAME: ', k8s_pod_name)
  else:
    st.write('Running outside of Docker or Kubernetes')
  

def main():
    # print app version
    app_version = os.getenv('APP_VERSION')
    st.write('Welcome to Streamlit in Docker')
    st.write('APP_VERSION = ', app_version)

    fn_detect_runtime_env()


    dataset_1 = [
      {'Symbol': 'AA', 'Description': 'Alcoa Corp', 'Last Price': 55.23},
      {'Symbol': 'AAAP', 'Description': 'Advanced Accelerator Applications S.A.', 'Last Price': 95.45},
      {'Symbol': 'AABA', 'Description': 'Altaba Inc.', 'Last Price': 73.19},
      {'Symbol': 'AAC', 'Description': 'AAC Holdings Inc.', 'Last Price': 8.35},
      {'Symbol': 'AAN', 'Description': 'Aaron\'s Inc.', 'Last Price': 63.45}
    ]

    df_1 = pd.DataFrame(dataset_1)
    print(df_1)


    dataset_2 = [
      {'Symbol': 'AAPL', 'Description': 'Apple Inc.', 'Last Price': 543.21},
      {'Symbol': 'AMZN', 'Description': 'Amazon.com, Inc.', 'Last Price': 513.11},
      {'Symbol': 'CSCO', 'Description': 'Cisco Systems, Inc.', 'Last Price': 514.19},
      {'Symbol': 'FB', 'Description': 'Facebook, Inc. Class A', 'Last Price': 523.45},
      {'Symbol': 'GOOGL', 'Description': 'Alphabet Inc. Class A', 'Last Price': 541.19},
      {'Symbol': 'GOOG', 'Description': 'Alphabet Inc. Class C', 'Last Price': 539.99},
      {'Symbol': 'INTC', 'Description': 'Intel Corporation', 'Last Price': 511.99},
      {'Symbol': 'MSFT', 'Description': 'Microsoft Corporation', 'Last Price': 522.11},
      {'Symbol': 'PEP', 'Description': 'PepsiCo, Inc.', 'Last Price': 521.11},
      {'Symbol': 'V', 'Description': 'Visa Inc. Class A', 'Last Price': 513.99}
    ]


    df_2 = pd.DataFrame(dataset_2)
    print(df_2)

    df_dropdown_list = ["Symbols beginning with AA", "Symbols with prices greater than 500", "option3"]
    sb_dropdown_chosen_option = st.selectbox(
      "My DropDown List",
      df_dropdown_list,
      key="sb_my_dropdown_list",
      index=None,
    )

    st.write("### ", sb_dropdown_chosen_option)
    if sb_dropdown_chosen_option == "Symbols beginning with AA":
      st.write(df_1)
    elif sb_dropdown_chosen_option == "Symbols with prices greater than 500":
      st.write(df_2)

    st.stop()

if __name__ == '__main__':
    main()




