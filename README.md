# GCP Streamlit football application
### **Project Overview**  

This project involves deploying a Docker-containerized Streamlit application on **Cloud Run**.  

The application retrieves data from a **BigQuery** database and presents interactive visualizations. The overall application structure is kept simple, as the primary goal is to test **BigQuery** and **Cloud Run** services on **Google Cloud Platform (GCP)**.  

You can access the application at [Streamlit](https://gcpstreamlitfootball-711519321063.europe-southwest1.run.app/). The application will be taken down at some moment so you may not be able to see it anymore.

---

### **Pre-requisites**

Before you can run this project, ensure the following requirements are met:

1. Successfully set up **Python** and **Docker** to test the containerized Streamlit application locally.
2. Build the **Docker Image**.
3. Have a **Google Cloud account**.
4. Install the **Google Cloud CLI**.
5. Create a Google Cloud Project and enable the following APIs:
   - **BigQuery API**
   - **Artifact Registry API**
   - **Cloud Run Admin API**
6. In the **IAM & Admin > IAM** section of your project, create a user with the required permissions for BigQuery and Artifact Registry. 
Generate a key for the role and place the key file directory in the code.

---

### **Creating a BigQuery Database**
To set up the back-end database in BigQuery, follow these steps:

1. Navigate to the **BigQuery** service within your created project.
2. Click **Create Dataset** and configure the necessary settings.
3. Within the dataset, click **Create Table**, and select the **Upload** option. Upload the files generated from the code found at `https://github.com/dieGeijo8/Transfermarkt_DB_WSL`.

---

### **Deploying on Cloud Run**
Follow these steps to upload the Docker image to Google Cloud Platform and deploy it on Cloud Run:

1. In the Google Cloud SDK Shell, run the following commands:
   - `gcloud auth activate-service-account --key-file=path_to_key_file.json`
   - `gcloud artifacts repositories create artifact_repo_name --location=europe --repository-format=docker`
   - `docker push artifact_repo_name/docker_image_name:v1`
2. Inside the created project, navigate to the **Cloud Run** service.
3. Click **Deploy Container** > **Service**.
4. Select the container you created from the artifact repository, configure any additional settings, and click **Deploy**.

Your containerized app should now be accessible via a provided URL.
