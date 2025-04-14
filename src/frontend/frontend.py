# streamlit app basic template with docker 
import os
import streamlit as st

def get_environment():
    """Detect the environment where the app is running."""
    if os.path.exists('/.dockerenv'):
        return 'Docker'
    elif os.getenv('KUBERNETES_SERVICE_HOST'):
        return 'Kubernetes'
    else:
        return 'Unknown'

def main():
    app_version = os.getenv('APP_VERSION')
    st.write('Welcome to Streamlit in Docker')
    st.write('APP_VERSION = ', app_version)

    # Detect if running in Docker or Kubernetes
    environment = get_environment()
    st.write(f'Running in environment: {environment}')

    if environment == 'Docker':
        docker_hostname = os.getenv('HOSTNAME')
        st.write('Docker HOSTNAME: ', docker_hostname)
    elif environment == 'Kubernetes':
        k8s_namespace = os.getenv('KUBERNETES_NAMESPACE', 'default')
        k8s_pod_name = os.getenv('HOSTNAME')
        st.write('Kubernetes NAMESPACE: ', k8s_namespace)
        st.write('Kubernetes POD_NAME: ', k8s_pod_name)
    else:
        st.write('Running outside of Docker or Kubernetes')

if __name__ == '__main__':
    main()




